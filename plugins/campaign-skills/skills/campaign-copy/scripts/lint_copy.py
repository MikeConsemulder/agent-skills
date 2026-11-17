#!/usr/bin/env python3
"""Controleert advertentiecopy mechanisch: tekenlimieten, talen en claims.

Invoer: een CSV met de kolommen `id`, `kanaal`, `veld`, `taal`, `tekst`
(zie assets/copy.voorbeeld.csv). Gecontroleerd wordt:
  - harde tekenlimiet per kanaal + veld (fout) en zichtbare limiet (waarschuwing)
  - elke combinatie id + kanaal + veld bestaat in elke gevraagde taal (--talen)
  - lege teksten, te veel uitroeptekens, te veel HOOFDLETTERS
  - claims die onderbouwing nodig hebben (Reclame Code, ACM): waarschuwing

Exitcode 0 = schoon, 1 = fouten, 2 = invoer- of gebruiksfout.

Gebruik:
  lint_copy.py copy.csv
  lint_copy.py copy.csv --talen nl,en --regels copy_regels.json
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RULES = os.path.join(HERE, "..", "assets", "copy_regels.json")


def claim_hits(text, claims):
    low = text.lower()
    hits = []
    for claim in claims:
        pattern = r"(?<![\w])" + re.escape(claim.lower()) + r"(?![\w])"
        if re.search(pattern, low):
            hits.append(claim)
    return hits


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="CSV met id, kanaal, veld, taal, tekst")
    ap.add_argument("--talen", default="nl,en", help="talen die voor elke tekst moeten bestaan (standaard nl,en)")
    ap.add_argument("--regels", default=DEFAULT_RULES, help="JSON met limieten en claims")
    args = ap.parse_args()

    try:
        with open(args.regels, encoding="utf-8") as fh:
            rules = json.load(fh)
        with open(args.csv, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"fout: {exc}", file=sys.stderr)
        return 2
    needed = {"id", "kanaal", "veld", "taal", "tekst"}
    if not rows or needed - set(rows[0].keys()):
        print(f"fout: {args.csv} mist kolommen: {', '.join(sorted(needed - set(rows[0].keys() if rows else [])))}", file=sys.stderr)
        return 2

    talen = [t.strip().lower() for t in args.talen.split(",") if t.strip()]
    limits = rules.get("limieten", {})
    errors, warnings = [], []
    langs_per_item = defaultdict(set)

    for line, row in enumerate(rows, start=2):
        kanaal, veld, taal = row["kanaal"].strip().lower(), row["veld"].strip().lower(), row["taal"].strip().lower()
        tekst = row["tekst"].strip()
        where = f"{row['id']} {kanaal}.{veld} [{taal}] (regel {line})"
        langs_per_item[(row["id"].strip(), kanaal, veld)].add(taal)

        if not tekst:
            errors.append(f"{where}: tekst is leeg")
            continue
        n = len(tekst)
        limit = limits.get(kanaal, {}).get(veld)
        if limit is None:
            warnings.append(f"{where}: geen limiet bekend voor {kanaal}.{veld}; voeg die toe aan de regels")
        else:
            if "max" in limit and n > limit["max"]:
                errors.append(f"{where}: {n} tekens, maximaal {limit['max']}")
            elif "advies" in limit and n > limit["advies"]:
                warnings.append(f"{where}: {n} tekens; na {limit['advies']} wordt afgekapt achter 'meer'")
        if tekst.count("!") > rules.get("max_uitroeptekens", 1):
            warnings.append(f"{where}: {tekst.count('!')} uitroeptekens")
        letters = [c for c in tekst if c.isalpha()]
        if len(letters) >= 12:
            caps = sum(c.isupper() for c in letters) / len(letters)
            if caps > rules.get("max_hoofdletter_aandeel", 0.3):
                warnings.append(f"{where}: {caps:.0%} hoofdletters; leest als schreeuwen")
        hits = claim_hits(tekst, rules.get("claims", {}).get(taal, []))
        if hits:
            warnings.append(f"{where}: claim(s) {', '.join(hits)}; alleen gebruiken als het aantoonbaar waar is (Reclame Code)")

    for (item, kanaal, veld), found in sorted(langs_per_item.items()):
        for taal in talen:
            if taal not in found:
                errors.append(f"{item} {kanaal}.{veld}: versie in taal '{taal}' ontbreekt")

    print(f"{len(rows)} tekst(en) gecontroleerd in {args.csv} (talen: {', '.join(talen)})")
    for w in warnings:
        print(f"  waarschuwing: {w}")
    if errors:
        print(f"\n{len(errors)} fout(en):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("Geen fouten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
