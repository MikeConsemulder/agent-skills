#!/usr/bin/env python3
"""Controleert de UTM-links van een campagne tegen een vaste naamgeving.

Invoer: een CSV met minimaal de kolommen `advertentie_id`, `kanaal` en `url`
(zie assets/utm.voorbeeld.csv). Per regel wordt gecontroleerd:
  - https, en optioneel het juiste domein (--domein)
  - utm_source, utm_medium, utm_campaign en utm_content aanwezig
  - waarden in kleine letters, alleen a-z, 0-9, '-' en '_'
  - utm_medium uit de toegestane lijst
  - utm_campaign volgens het naampatroon (standaard JJJJ-MM_naam)
  - geen klik-ID's (fbclid, gclid, ttclid, ...) hardgecodeerd in de link
  - elke url en elke utm_content per campagne uniek

Regels zijn te overschrijven met --config regels.json (zelfde sleutels als DEFAULTS).
Exitcode 0 = schoon, 1 = fouten, 2 = invoer- of gebruiksfout.

Gebruik:
  lint_utm.py utm.csv
  lint_utm.py utm.csv --domein voorbeeld.nl --config utm_regels.json
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from urllib.parse import parse_qs, urlparse

DEFAULTS = {
    "verplicht": ["utm_source", "utm_medium", "utm_campaign", "utm_content"],
    "waarde_patroon": r"^[a-z0-9][a-z0-9_-]*$",
    "campagne_patroon": r"^\d{4}-\d{2}_[a-z0-9-]+$",
    "media": ["paid_social", "organic_social", "cpc", "display", "email",
              "affiliate", "referral", "influencer", "qr", "video"],
    "bron_aliassen": {"fb": "facebook", "ig": "instagram", "insta": "instagram",
                      "tt": "tiktok", "li": "linkedin", "yt": "youtube", "pin": "pinterest"},
    "klik_ids": ["fbclid", "gclid", "gbraid", "wbraid", "ttclid", "msclkid", "li_fat_id", "epik"],
}


def load_rules(path):
    rules = dict(DEFAULTS)
    if path:
        with open(path, encoding="utf-8") as fh:
            rules.update(json.load(fh))
    return rules


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", help="CSV met advertentie_id, kanaal, url")
    ap.add_argument("--domein", help="verwacht domein van de landingspagina, bv. voorbeeld.nl")
    ap.add_argument("--config", help="JSON-bestand dat de standaardregels overschrijft")
    args = ap.parse_args()

    try:
        rules = load_rules(args.config)
        with open(args.csv, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"fout: {exc}", file=sys.stderr)
        return 2
    missing_cols = {"advertentie_id", "kanaal", "url"} - set(rows[0].keys() if rows else [])
    if missing_cols:
        print(f"fout: kolommen ontbreken in {args.csv}: {', '.join(sorted(missing_cols))}", file=sys.stderr)
        return 2

    value_re = re.compile(rules["waarde_patroon"])
    campaign_re = re.compile(rules["campagne_patroon"])
    errors, warnings = [], []
    seen_urls = {}
    content_per_campaign = defaultdict(dict)

    for line, row in enumerate(rows, start=2):
        ad = row["advertentie_id"].strip() or f"regel {line}"
        where = f"{ad} (regel {line})"
        url = row["url"].strip()
        parsed = urlparse(url)
        if parsed.scheme != "https":
            errors.append(f"{where}: link is geen https")
        host = parsed.hostname or ""
        if args.domein and not (host == args.domein or host.endswith("." + args.domein)):
            errors.append(f"{where}: domein {host} is niet {args.domein}")
        params = {k: v[0] for k, v in parse_qs(parsed.query, keep_blank_values=True).items()}

        for key in rules["verplicht"]:
            if not params.get(key):
                errors.append(f"{where}: {key} ontbreekt")
        for key, val in params.items():
            if key.startswith("utm_") and val and not value_re.match(val):
                errors.append(f"{where}: {key}='{val}' bevat hoofdletters, spaties of tekens buiten a-z0-9_-")
            if key in rules["klik_ids"]:
                errors.append(f"{where}: klik-ID {key} hoort niet in de link; het platform voegt die zelf toe")

        medium = params.get("utm_medium", "")
        if medium and medium not in rules["media"]:
            errors.append(f"{where}: utm_medium='{medium}' staat niet in de lijst ({', '.join(rules['media'])})")
        source = params.get("utm_source", "")
        if source in rules["bron_aliassen"]:
            errors.append(f"{where}: utm_source='{source}', gebruik '{rules['bron_aliassen'][source]}'")
        campaign = params.get("utm_campaign", "")
        if campaign and not campaign_re.match(campaign):
            errors.append(f"{where}: utm_campaign='{campaign}' volgt het patroon {rules['campagne_patroon']} niet")

        if url in seen_urls:
            errors.append(f"{where}: dezelfde link als {seen_urls[url]}; dan kun je ze niet uit elkaar houden")
        seen_urls.setdefault(url, where)
        content = params.get("utm_content", "")
        if content and campaign:
            other = content_per_campaign[campaign].get(content)
            if other and other != ad:
                errors.append(f"{where}: utm_content='{content}' wordt in {campaign} ook gebruikt door {other}")
            content_per_campaign[campaign].setdefault(content, ad)
        if row.get("kanaal", "").strip() and source and row["kanaal"].strip().lower() not in source:
            warnings.append(f"{where}: kanaal '{row['kanaal']}' en utm_source '{source}' lijken niet bij elkaar te passen")

    print(f"{len(rows)} link(s) gecontroleerd in {args.csv}")
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
