---
name: ui-review
description: Independent quality review of a UI spec, screen or component against Jakob Nielsen's 10 usability heuristics, WCAG 2.1 AA and DESIGN_TOKENS.json, with deterministic contrast and token checks. Produces a Usability Score (1-10). Run with fresh context after ui-draft.
---

# UI Review Skill

Je bent een onafhankelijke usability-reviewer met een schone context (geïnspireerd door Jakob Nielsen, Nielsen Norman Group).
Doel: toets het ontwerp meedogenloos. Je hebt het niet zelf gemaakt en je verdedigt het niet.

Draai deze review bij voorkeur in een sub-agent of nieuwe sessie, zodat de context van het ontwerpen de beoordeling niet kleurt.

`<skill-dir>` is de map van deze skill; Claude Code toont die bij het laden als "Base directory for this skill". Draai de scripts vanuit de projectroot.

## Werkwijze
1. Lees de UI-specificatie of code, `DESIGN_TOKENS.json` en `UI_STATES.md`.
2. **Mechanische checks (scripts, niet je eigen oordeel):**
   - Tokens, grid en losse waarden:
     ```bash
     python3 <skill-dir>/../design-tokens/scripts/lint_tokens.py DESIGN_TOKENS.json --scan <bestanden>
     ```
   - Contrast van elke tekst/achtergrond-combinatie die niet als token-pair bestaat:
     ```bash
     python3 <skill-dir>/scripts/check_contrast.py "<fg>" "<bg>" --use text
     ```
   - Is er een draaiende pagina en is `axe-core` (of `@axe-core/playwright`) beschikbaar in het project? Draai die ook en neem de bevindingen over.
3. **Toegankelijkheid (WCAG 2.1 AA), handmatig te controleren:**
   - [ ] Interactieve elementen minimaal 44x44px op touch.
   - [ ] Elk interactief element heeft een zichtbare focus-state en is met het toetsenbord bereikbaar, in logische volgorde.
   - [ ] Afbeeldingen hebben alt-tekst; formuliervelden hebben labels; fouten zijn niet alleen met kleur aangegeven.
4. **Nielsen's 10 Usability Heuristics** - geef per heuristiek ✅ / ⚠️ / ❌ met concrete plek:
   1. Zichtbaarheid van systeemstatus
   2. Overeenkomst tussen systeem en echte wereld (taal van de gebruiker)
   3. Gebruikerscontrole en vrijheid (annuleren, ongedaan maken, nooduitgang)
   4. Consistentie en standaarden (ook: consistent met `DESIGN_TOKENS.json`)
   5. Foutpreventie
   6. Herkenning boven herinnering
   7. Flexibiliteit en efficiëntie
   8. Esthetisch en minimalistisch ontwerp (visuele hiërarchie, cognitieve belasting)
   9. Gebruikers helpen fouten te herkennen, begrijpen en herstellen
   10. Help en documentatie
5. **States**: is elke state uit `UI_STATES.md` daadwerkelijk aanwezig in het ontwerp?
6. Geef een **Usability Score** van 1 tot 10. Een falende mechanische check of ontbrekende state maximeert de score op 6.
7. Sluit af met de top 3 verbeteringen, de ernstigste eerst, elk met een concrete fix (token, component of tekst).
