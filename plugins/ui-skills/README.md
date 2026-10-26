# `ui-skills` – UI Design Skills

Designers hand over a static happy path; developers find out what happens with a 4-line title, a missing avatar or a 360px screen. These skills force those questions before anything is built.

| Skill | What it does | Output |
| --- | --- | --- |
| `/design-tokens` | Creates and lints `DESIGN_TOKENS.json` (Brad Frost) | `DESIGN_TOKENS.json` |
| `/ui-discovery` | Information architecture & user flow, before any layout | `UI_DISCOVERY.md` |
| `/ui-grill` | Grills on Scott Hurff's 5 UI states and responsive breakpoints | `UI_STATES.md` |
| `/ui-draft` | Token-locked Tailwind/HTML or Figma component specs with every state (Jordan Singer) | components / spec |
| `/ui-review` | Clean-context review on Nielsen's 10 heuristics + WCAG 2.1 AA | Usability Score + top 3 fixes |

## Mechanical vs. judgement

What can be computed is not prompted, it is checked by a script (Python 3, no dependencies):

```bash
# Token file: spacing on the grid, every contrast pair WCAG AA
python3 skills/design-tokens/scripts/lint_tokens.py DESIGN_TOKENS.json

# UI code: no stray hex colours, off-grid px values or Tailwind arbitrary values
python3 skills/design-tokens/scripts/lint_tokens.py DESIGN_TOKENS.json --scan src/

# A single colour pair
python3 skills/ui-review/scripts/check_contrast.py "#6B7280" "#FFFFFF"
```

The agent reasons only about what needs judgement: visual hierarchy, cognitive load, flow and copy.

```bash
claude plugin install ui-skills@mikeconsemulder-marketplace
```
