#!/usr/bin/env python3
"""Controleert de geëxporteerde creatives (PNG/JPG/WEBP/MP4/MOV) tegen de placement-specs.

Invoer: een CSV met de kolommen `bestand` en `placement` (zie assets/creatives.voorbeeld.csv);
paden in de CSV zijn relatief aan de map van de CSV. Gecontroleerd wordt:
  - bestand bestaat
  - beeldverhouding gelijk aan de placement (fout), exacte afmetingen (waarschuwing)
  - bestandsgrootte onder het maximum
  - video: duur binnen de grenzen, H.264/H.265-codec, audio aanwezig (waarschuwing als stil)

Gebruikt ffprobe (onderdeel van FFmpeg; HyperFrames heeft het ook nodig).
Safe zones en lettergrootte controleer je op de HTML-bron met check_safe_zones.mjs.
Exitcode 0 = schoon, 1 = fouten, 2 = invoer- of gebruiksfout.

Gebruik:
  lint_creative.py creatives.csv
  lint_creative.py creatives.csv --specs creative_specs.json
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SPECS = os.path.join(HERE, "..", "assets", "creative_specs.json")
VIDEO_EXT = {".mp4", ".mov", ".webm", ".m4v"}


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,width,height:format=duration",
         "-of", "json", path],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    audio = any(s.get("codec_type") == "audio" for s in data.get("streams", []))
    duration = float(data.get("format", {}).get("duration") or 0)
    return video, audio, duration


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="CSV met bestand, placement")
    ap.add_argument("--specs", default=DEFAULT_SPECS, help="JSON met placement-specs")
    args = ap.parse_args()

    if not shutil.which("ffprobe"):
        print("fout: ffprobe niet gevonden; installeer FFmpeg", file=sys.stderr)
        return 2
    try:
        with open(args.specs, encoding="utf-8") as fh:
            specs = json.load(fh)["placements"]
        with open(args.csv, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"fout: {exc}", file=sys.stderr)
        return 2

    base = os.path.dirname(os.path.abspath(args.csv))
    errors, warnings = [], []
    for line, row in enumerate(rows, start=2):
        rel, placement = row.get("bestand", "").strip(), row.get("placement", "").strip()
        where = f"{rel} [{placement}] (regel {line})"
        spec = specs.get(placement)
        if not spec:
            errors.append(f"{where}: onbekende placement; kies uit {', '.join(sorted(specs))}")
            continue
        path = os.path.join(base, rel)
        if not os.path.isfile(path):
            errors.append(f"{where}: bestand bestaat niet")
            continue
        try:
            video, audio, duration = probe(path)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            errors.append(f"{where}: ffprobe kan het bestand niet lezen")
            continue
        if not video:
            errors.append(f"{where}: geen beeld gevonden")
            continue

        w, h = int(video["width"]), int(video["height"])
        want_w, want_h = spec["breedte"], spec["hoogte"]
        if abs(w / h - want_w / want_h) > 0.01:
            errors.append(f"{where}: {w}x{h} heeft niet de verhouding van {want_w}x{want_h}")
        elif (w, h) != (want_w, want_h):
            warnings.append(f"{where}: {w}x{h}, aanbevolen {want_w}x{want_h}")

        mb = os.path.getsize(path) / (1024 * 1024)
        if mb > spec.get("max_mb", float("inf")):
            errors.append(f"{where}: {mb:.1f} MB, maximaal {spec['max_mb']} MB")

        if os.path.splitext(path)[1].lower() in VIDEO_EXT:
            lo, hi = spec.get("video_duur_s", [0, float("inf")])
            if not lo <= duration <= hi:
                errors.append(f"{where}: video duurt {duration:.1f}s, toegestaan {lo}-{hi}s")
            if video.get("codec_name") not in {"h264", "hevc"}:
                errors.append(f"{where}: codec {video.get('codec_name')}, gebruik H.264 (of H.265)")
            if not audio:
                warnings.append(f"{where}: geen audiospoor; prima als het bewust stil is, maar Reels/TikTok belonen geluid")

    print(f"{len(rows)} creative(s) gecontroleerd in {args.csv}")
    for wmsg in warnings:
        print(f"  waarschuwing: {wmsg}")
    if errors:
        print(f"\n{len(errors)} fout(en):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Geen fouten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
