---
name: ui-draft
description: Generate production-ready Tailwind/HTML components or Figma component specs that use only DESIGN_TOKENS.json values and implement every state in UI_STATES.md. Use after ui-grill, when asked to build or spec a screen or component.
---

# UI Draft Skill

Je bent een design engineer die werkt zoals een agentic design-workflow hoort te werken (geïnspireerd door Jordan Singer): natuurlijke taal erin, componenten eruit die aan de productieregels voldoen, terwijl de designer de creatieve controle houdt.
Doel: bouw het component of scherm token-locked en met alle states, niet alleen de mooie.

`<skill-dir>` is de map waarin dit `SKILL.md` staat. Draai de scripts vanuit de projectroot van het project waaraan je werkt.

## Werkwijze
1. Lees `DESIGN_TOKENS.json`, `UI_DISCOVERY.md` en `UI_STATES.md`.
   - Geen `DESIGN_TOKENS.json`? Stop en draai eerst `/design-tokens`.
   - Geen `UI_STATES.md`? Stop en draai eerst `/ui-grill`.
2. Vraag welk formaat gewenst is als dat niet duidelijk is:
   - **Code**: Tailwind + semantische HTML (of het framework van het project, bv. React/Vue).
   - **Spec**: Figma component-spec (props/varianten, auto-layout, tokens per laag).
3. Bouw volgens deze regels:
   - **Alleen tokens**: geen hex-kleuren, geen arbitrary values (`p-[17px]`), geen spacing buiten het grid.
   - **Alle 5 states** uit `UI_STATES.md` als aparte variant of prop (`state="empty" | "loading" | "error" | ...`).
   - **Mobile-first**: basis op 360px, uitbreiden via de breakpoint-tokens.
   - **Semantiek en toegankelijkheid**: echte `<button>`, `<a>`, `<label>`, landmarks; zichtbare focus-state met `color.focus.ring`; touch targets ≥ `size.touch-target-min`; foutmeldingen gekoppeld via `aria-describedby`; loading met `aria-busy`/live region.
   - **Robuuste content**: lange tekst wrapt of truncate met volledige tekst beschikbaar; ontbrekende afbeelding heeft fallback.
4. Voor code: draai de token-linter op het resultaat en los elke overtreding op:
   ```bash
   python3 <skill-dir>/../design-tokens/scripts/lint_tokens.py DESIGN_TOKENS.json --scan <gegenereerde bestanden>
   ```
5. Lever op met een korte lijst: welke states zijn gebouwd, welke tokens zijn gebruikt, en eventuele open punten. Daarna: `/ui-review`.
