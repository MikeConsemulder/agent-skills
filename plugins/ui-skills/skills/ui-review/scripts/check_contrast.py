#!/usr/bin/env python3
"""WCAG 2.1 contrast check for one or more foreground/background pairs.

Usage:
  check_contrast.py FG BG [--use text|large-text|ui]
  check_contrast.py "#6B7280" "#FFFFFF"
  check_contrast.py "#FFFFFF" "#1D4ED8" --use ui

Thresholds (AA): text 4.5:1, large-text (>=24px, or >=18.66px bold) 3:1,
ui (borders, icons, focus rings) 3:1. Exit code 0 = pass, 1 = fail.
"""
import argparse
import re
import sys

MIN_RATIO = {"text": 4.5, "large-text": 3.0, "ui": 3.0}
HEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def hex_to_rgb(value):
    m = HEX.match(value.strip())
    if not m:
        raise ValueError(f"not a hex colour: {value}")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(rgb):
    def chan(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    l1, l2 = sorted((luminance(hex_to_rgb(fg)), luminance(hex_to_rgb(bg))), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fg")
    ap.add_argument("bg")
    ap.add_argument("--use", choices=MIN_RATIO, default="text")
    args = ap.parse_args()
    try:
        ratio = contrast(args.fg, args.bg)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    need = MIN_RATIO[args.use]
    ok = ratio >= need
    print(f"{'PASS' if ok else 'FAIL'} {ratio:.2f}:1 (AA needs {need}:1 for {args.use})  {args.fg} on {args.bg}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
