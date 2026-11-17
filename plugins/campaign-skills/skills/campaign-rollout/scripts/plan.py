#!/usr/bin/env python3
"""Rekent een campagne terug vanaf een harde datum en zet een kalender om naar .ics.

Subcommando's:

  deadline   Laatste besteldag waarop een bestelling nog vóór een datum binnen is.
             Telt werkdagen terug (zonder weekenden en, met --land nl, Nederlandse
             feestdagen) voor productie + verzending + marge.
               plan.py deadline --levering 2026-12-24 --productie 10 --verzending 3
               plan.py deadline --levering 2026-12-24 --productie 10 --verzending 7 --marge 2

  ics        Zet een kalender-CSV om naar een .ics-bestand dat elke agenda kan openen.
             Kolommen: datum, einddatum (optioneel), titel, kanaal, fase, taal, budget, notitie.
               plan.py ics CAMPAIGN_CALENDAR.csv --uit campagne.ics

Exitcode 0 = ok, 2 = invoer- of gebruiksfout.
"""
import argparse
import csv
import sys
from datetime import date, datetime, timedelta, timezone


def easter(year):
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return date(year, month, day + 1)


def holidays_nl(year):
    e = easter(year)
    kingsday = date(year, 4, 27)
    if kingsday.weekday() == 6:
        kingsday = date(year, 4, 26)
    days = {
        date(year, 1, 1): "Nieuwjaarsdag",
        e + timedelta(days=1): "Tweede paasdag",
        kingsday: "Koningsdag",
        e + timedelta(days=39): "Hemelvaartsdag",
        e + timedelta(days=50): "Tweede pinksterdag",
        date(year, 12, 25): "Eerste kerstdag",
        date(year, 12, 26): "Tweede kerstdag",
    }
    if year % 5 == 0:
        days[date(year, 5, 5)] = "Bevrijdingsdag"
    return days


DAGEN = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]
MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli",
           "augustus", "september", "oktober", "november", "december"]


def nl_date(d):
    return f"{DAGEN[d.weekday()]} {d.day} {MAANDEN[d.month - 1]} {d.year}"


def is_workday(d, land):
    if d.weekday() >= 5:
        return False
    return not (land == "nl" and d in holidays_nl(d.year))


def back_workdays(d, n, land):
    while n > 0:
        d -= timedelta(days=1)
        if is_workday(d, land):
            n -= 1
    return d


def cmd_deadline(args):
    try:
        target = date.fromisoformat(args.levering)
    except ValueError:
        print("fout: --levering moet JJJJ-MM-DD zijn", file=sys.stderr)
        return 2
    total = args.productie + args.verzending + args.marge
    last = back_workdays(target, total, args.land)
    skipped = sorted(
        (d, n) for y in {last.year, target.year} for d, n in holidays_nl(y).items()
        if last <= d <= target and d.weekday() < 5
    ) if args.land == "nl" else []
    print(f"Levering uiterlijk:   {nl_date(target)}")
    print(f"Werkdagen terug:      {total} (productie {args.productie} + verzending {args.verzending} + marge {args.marge})")
    if skipped:
        print("Feestdagen overgeslagen: " + ", ".join(f"{n} ({d:%d-%m})" for d, n in skipped))
    print(f"Laatste besteldag:    {nl_date(last)}")
    print("Zet de laatste besteldag als harde fase in de kalender en stop daarna met cadeau-advertenties of verander de belofte.")
    return 0


def ics_escape(text):
    for old, new in (("\\", "\\\\"), (";", r"\;"), (",", r"\,"), ("\n", r"\n")):
        text = text.replace(old, new)
    return text


def cmd_ics(args):
    try:
        with open(args.csv, encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.DictReader(fh))
    except OSError as exc:
        print(f"fout: {exc}", file=sys.stderr)
        return 2
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//agent-skills//campaign-rollout//NL", "CALSCALE:GREGORIAN"]
    for i, row in enumerate(rows, start=2):
        try:
            start = date.fromisoformat(row["datum"].strip())
            end_raw = (row.get("einddatum") or "").strip()
            end = date.fromisoformat(end_raw) if end_raw else start
        except (KeyError, ValueError):
            print(f"fout: regel {i} heeft geen geldige datum/einddatum (JJJJ-MM-DD)", file=sys.stderr)
            return 2
        title = row.get("titel", "").strip() or "Campagne-item"
        prefix = " · ".join(x for x in (row.get("fase", "").strip(), row.get("kanaal", "").strip(), row.get("taal", "").strip().upper()) if x)
        summary = f"[{prefix}] {title}" if prefix else title
        desc = "\n".join(f"{k}: {v.strip()}" for k, v in row.items() if k in ("budget", "notitie") and v and v.strip())
        lines += [
            "BEGIN:VEVENT",
            f"UID:campagne-{i}-{start:%Y%m%d}@agent-skills",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{start:%Y%m%d}",
            f"DTEND;VALUE=DATE:{end + timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{ics_escape(summary)}",
        ]
        if desc:
            lines.append(f"DESCRIPTION:{ics_escape(desc)}")
        lines.append("END:VEVENT")
    lines.append("END:VCALENDAR")
    with open(args.uit, "w", encoding="utf-8", newline="") as fh:
        fh.write("\r\n".join(lines) + "\r\n")
    print(f"{len(rows)} item(s) geschreven naar {args.uit}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("deadline", help="laatste besteldag berekenen")
    d.add_argument("--levering", required=True, help="datum waarop het uiterlijk binnen moet zijn (JJJJ-MM-DD)")
    d.add_argument("--productie", type=int, required=True, help="maximale productietijd in werkdagen")
    d.add_argument("--verzending", type=int, required=True, help="maximale verzendtijd in werkdagen")
    d.add_argument("--marge", type=int, default=1, help="extra werkdagen buffer (standaard 1)")
    d.add_argument("--land", default="nl", choices=["nl", "geen"], help="feestdagen van dit land overslaan")
    i = sub.add_parser("ics", help="kalender-CSV omzetten naar .ics")
    i.add_argument("csv")
    i.add_argument("--uit", default="campagne.ics")
    args = ap.parse_args()
    return cmd_deadline(args) if args.cmd == "deadline" else cmd_ics(args)


if __name__ == "__main__":
    sys.exit(main())
