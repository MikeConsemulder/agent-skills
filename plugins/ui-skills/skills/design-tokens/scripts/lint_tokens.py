#!/usr/bin/env python3
"""Deterministic linter for DESIGN_TOKENS.json and the UI code built on it.

Checks the token file itself:
  - every spacing token sits on the grid (grid.base, default 4px)
  - every contrast pair in $extensions.a11y.contrastPairs meets WCAG 2.1 AA
    (text: 4.5:1, large-text / ui: 3:1)

With --scan, also checks source files (HTML, CSS, JSX/TSX, Vue, Svelte ...):
  - hex colours that are not a colour token
  - px values in spacing/sizing properties that are off the grid
  - Tailwind arbitrary values such as p-[17px] or text-[#123456]

Exit code 0 = clean, 1 = violations found, 2 = usage / file error.
Usage:
  lint_tokens.py DESIGN_TOKENS.json
  lint_tokens.py DESIGN_TOKENS.json --scan src/ index.html
"""
import argparse
import json
import os
import re
import sys

REF = re.compile(r"^\{([^}]+)\}$")
HEX = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b")
PX_PROP = re.compile(
    r"\b(margin|padding|gap|row-gap|column-gap|top|right|bottom|left|inset)"
    r"(?:-[a-z]+)?\s*:\s*([^;}\n]+)"
)
PX = re.compile(r"(-?\d+(?:\.\d+)?)px")
TW_ARBITRARY = re.compile(r"\b[a-z][a-z0-9-]*-\[[^\]\s]+\]")
SCAN_EXT = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro"}
MIN_RATIO = {"text": 4.5, "large-text": 3.0, "ui": 3.0}


def flatten(node, prefix=""):
    out = {}
    if isinstance(node, dict):
        if "$value" in node:
            out[prefix] = node["$value"]
            return out
        for key, child in node.items():
            if key.startswith("$"):
                continue
            out.update(flatten(child, f"{prefix}.{key}" if prefix else key))
    return out


def resolve(value, tokens, seen=()):
    m = REF.match(value) if isinstance(value, str) else None
    if not m:
        return value
    path = m.group(1)
    if path in seen or path not in tokens:
        raise KeyError(path)
    return resolve(tokens[path], tokens, seen + (path,))


def hex_to_rgb(value):
    h = value.lstrip("#")
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


def px(value):
    m = re.fullmatch(r"(-?\d+(?:\.\d+)?)px", str(value).strip())
    return float(m.group(1)) if m else None


def lint_tokens(raw, tokens, grid, errors):
    for path, value in tokens.items():
        if path.startswith("spacing."):
            n = px(resolve(value, tokens))
            if n is None or n % grid:
                errors.append(f"tokens: {path} = {value} is not on the {grid:g}px grid")
    pairs = raw.get("$extensions", {}).get("a11y", {}).get("contrastPairs", [])
    if not pairs:
        errors.append("tokens: no $extensions.a11y.contrastPairs defined; contrast is unchecked")
    for pair in pairs:
        use = pair.get("use", "text")
        try:
            fg, bg = resolve(pair["fg"], tokens), resolve(pair["bg"], tokens)
        except KeyError as missing:
            errors.append(f"tokens: contrast pair references unknown token {missing}")
            continue
        ratio = contrast(fg, bg)
        need = MIN_RATIO.get(use, 4.5)
        status = "ok  " if ratio >= need else "FAIL"
        print(f"  {status} {ratio:5.2f}:1 (need {need}:1, {use})  {pair['fg']} on {pair['bg']}")
        if ratio < need:
            errors.append(f"tokens: {pair['fg']} on {pair['bg']} is {ratio:.2f}:1, needs {need}:1 ({use})")


def iter_files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", "dist", "build"}]
                for f in files:
                    if os.path.splitext(f)[1] in SCAN_EXT:
                        yield os.path.join(root, f)
        elif os.path.isfile(p):
            yield p


def scan(paths, tokens, grid, errors):
    colours = {str(v).lower() for k, v in tokens.items() if k.startswith("color.") and str(v).startswith("#")}
    for path in iter_files(paths):
        with open(path, encoding="utf-8", errors="replace") as fh:
            for no, line in enumerate(fh, 1):
                where = f"{path}:{no}"
                for h in HEX.findall(line):
                    if h.lower() not in colours:
                        errors.append(f"{where}: colour {h} is not a token")
                for prop, val in PX_PROP.findall(line):
                    for n in PX.findall(val):
                        if float(n) % grid:
                            errors.append(f"{where}: {prop}: {n}px is off the {grid:g}px grid")
                for arb in TW_ARBITRARY.findall(line):
                    errors.append(f"{where}: Tailwind arbitrary value {arb}; use a token class")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tokens", help="path to DESIGN_TOKENS.json")
    ap.add_argument("--scan", nargs="+", metavar="PATH", help="files or folders to check against the tokens")
    args = ap.parse_args()
    try:
        with open(args.tokens, encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read {args.tokens}: {exc}", file=sys.stderr)
        return 2
    tokens = flatten(raw)
    grid = px(resolve(tokens.get("grid.base", "4px"), tokens)) or 4.0
    errors = []
    print(f"Token file: {args.tokens} ({len(tokens)} tokens, grid {grid:g}px)")
    lint_tokens(raw, tokens, grid, errors)
    if args.scan:
        scan(args.scan, tokens, grid, errors)
    if errors:
        print(f"\n{len(errors)} violation(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nNo violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
