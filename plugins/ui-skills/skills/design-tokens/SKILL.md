---
name: design-tokens
description: Create, extend and lint DESIGN_TOKENS.json (Brad Frost / Atomic Design) so every colour, spacing, type and radius value in the UI comes from one locked-in source. Use before drafting UI, when adding a colour or spacing value, or when asked to check tokens or contrast.
---

# Design Tokens Skill

Je bent de beheerder van het design system (geïnspireerd door Brad Frost en Atomic Design).
Doel: de AI verzint géén losse CSS-waarden. Alles komt uit `DESIGN_TOKENS.json`, en wat mechanisch te controleren is, controleert een script, niet een prompt.

`<skill-dir>` is de map van deze skill; Claude Code toont die bij het laden als "Base directory for this skill". Draai de scripts vanuit de projectroot.

## Werkwijze
1. Zoek `DESIGN_TOKENS.json` in de projectroot.
   - Bestaat het niet? Kopieer `<skill-dir>/assets/DESIGN_TOKENS.template.json` naar `DESIGN_TOKENS.json` en vraag de gebruiker naar merkkleuren, lettertype en grid (4px of 8px). Pas alleen de waarden aan, niet de structuur.
2. Wijzigingen aan tokens:
   - Een nieuwe waarde wordt alleen een token als ze op minstens twee plekken nodig is. Anders: hergebruik een bestaand token.
   - Spatiëring staat altijd op het grid (`grid.base`). Nooit `17px`.
   - Elke nieuwe kleur die als tekst, rand, icoon of focus-ring wordt gebruikt, krijgt een regel in `$extensions.a11y.contrastPairs` met de achtergrond waarop ze staat (`use`: `text`, `large-text` of `ui`).
   - Noem tokens naar hun rol (`color.feedback.error`), niet naar hun uiterlijk (`color.red`).
3. Draai na elke wijziging de linter en los elke overtreding op voordat je verdergaat:
   ```bash
   python3 <skill-dir>/scripts/lint_tokens.py DESIGN_TOKENS.json
   ```
   Om bestaande UI-code te controleren op losse kleuren, off-grid px-waarden en Tailwind arbitrary values (`p-[17px]`):
   ```bash
   python3 <skill-dir>/scripts/lint_tokens.py DESIGN_TOKENS.json --scan src/
   ```
4. Tailwind-project? Laat `tailwind.config` (of het `@theme`-blok in Tailwind v4) uit `DESIGN_TOKENS.json` lezen of genereer het eruit, zodat alleen token-classes bestaan.

## Regels
- Het script beslist over contrast en grid. Jij redeneert niet over "lijkt leesbaar genoeg".
- Een falende contrast-pair los je op in de token-waarde, niet met een uitzondering.
