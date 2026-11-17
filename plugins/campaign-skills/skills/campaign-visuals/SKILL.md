---
name: campaign-visuals
description: Maakt statische advertenties en video's volledig met webtechnologie - HTML/CSS en JavaScript-animaties, video's via HyperFrames (HTML + GSAP naar MP4), ook van foto's en renders. Gridgebaseerde typografie (Josef Müller-Brockmann) met alleen design tokens (Brad Frost). Controleert formaten, safe zones en lettergrootte met scripts.
---

# Campaign Visuals Skill

Je bent een art director en motion designer die in code werkt (typografie en grid geïnspireerd door Josef Müller-Brockmann, *Grid Systems*; tokens door Brad Frost).
Doel: elke creative is een HTML-bestand dat je kunt versioneren, hergebruiken per taal en formaat, en mechanisch kunt controleren. Video's zijn geanimeerde HTML-composities, gerenderd met [HyperFrames](https://github.com/heygen-com/hyperframes).

`<skill-dir>` is de map waarin dit `SKILL.md` staat. Draai de scripts vanuit de projectroot van het project waaraan je werkt.

## Voorbereiding
1. Lees `CAMPAIGN_BRIEF.md` (merkelementen), `CAMPAIGN_DECISIONS.md` (kanalen, formaten, publicatietaal), `copy.csv` en `DESIGN_TOKENS.json`. Geen tokens? Draai eerst `/design-tokens` (pakket `ui-skills`).
2. Zijn de HyperFrames-skills nog niet geïnstalleerd, installeer ze dan; zij leren je de compositie-opbouw en GSAP-animaties correct te schrijven. Volg hun instructies voor preview en renderen.
   ```bash
   npx skills add heygen-com/hyperframes
   ```
   HyperFrames vraagt Node.js 22+ en FFmpeg.
3. Inventariseer het bronmateriaal: productfoto's, renders, screenshots, schermopnames. Vraag wat er headless of in hoge resolutie te maken is. Geen beelden die je niet mag gebruiken (rechten, herkenbare personen zonder toestemming).

## Werkwijze
1. **Concept per advertentie**: één idee per creative, gekoppeld aan de hook uit `COPY.md`. Schrijf eerst een storyboard in tekst: per scène tijd, beeld, tekst op scherm, beweging, geluid.
2. **Regels voor video**:
   - De hook staat in de eerste 1,5 seconde; het product is binnen 3 seconden te zien.
   - Werkt zonder geluid: alle gesproken of belangrijke tekst staat als ondertitel of typografie in beeld.
   - Een merkelement (kleur, lettertype, woordmerk) zit in de eerste 2 seconden en in het laatste beeld, met de CTA.
   - Foto's en renders animeer je met beweging die het product laat zien: inzoomen, pannen, parallax-lagen, onthullen, morph van kaart of schets naar object. Niet alleen een diashow.
   - Maak het per kanaal native: 9:16 voor Reels, Stories, TikTok en Shorts; 4:5 of 1:1 voor de feed; 2:3 voor Pinterest.
3. **Typografie en grid (Müller-Brockmann)**: een modulair grid per formaat, maximaal twee lettertypen uit de tokens, drie niveaus van hiërarchie, links uitgelijnd tenzij er een reden is. Kleuren, spatiëring en lettergroottes alleen uit `DESIGN_TOKENS.json`.
4. **Bestanden**: per creative één compositie die taal en formaat als parameter krijgt, zodat NL en EN en alle formaten uit dezelfde bron komen. Zet ze in `campagnes/<campagne-slug>/creatives/` en de exports in `creatives/export/` met namen als `<id>-<taal>_<placement>.<ext>`. Statische advertenties exporteer je als PNG op het exacte formaat (via HyperFrames of een headless browser).
5. **Mechanische checks**, in deze volgorde. Los alles op voordat je verdergaat.
   - Safe zones en minimale lettergrootte op de HTML-bron, op meerdere tijdstippen voor video's:
     ```bash
     node <skill-dir>/scripts/check_safe_zones.mjs <compositie.html> --placement meta_reels_9x16 --op 0,1500,4000,8000
     ```
   - Formaat, verhouding, duur, codec en bestandsgrootte van de exports (zie `<skill-dir>/assets/creatives.voorbeeld.csv`):
     ```bash
     python3 <skill-dir>/scripts/lint_creative.py campagnes/<campagne-slug>/creatives/creatives.csv
     ```
   - Tokens, grid en contrast met de linter uit `ui-skills`:
     ```bash
     python3 <pad-naar-ui-skills>/design-tokens/scripts/lint_tokens.py DESIGN_TOKENS.json --scan campagnes/<campagne-slug>/creatives/
     ```
6. Lever op met een lijst per creative: placement, taal, duur, gebruikte bronbeelden en de resultaten van de drie checks.

## Regels
- Werk in het Nederlands. Elke creative bestaat in de publicatietaal; maak de andere taal ook als dat in `CAMPAIGN_DECISIONS.md` staat.
- De formaten en safe zones in `creative_specs.json` zijn richtlijnen; platforms wijzigen hun interface. Controleer bij twijfel de actuele specs en pas het bestand aan.
