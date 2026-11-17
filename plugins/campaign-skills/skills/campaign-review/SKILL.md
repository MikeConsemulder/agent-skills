---
name: campaign-review
description: Onafhankelijke eindcontrole van een complete campagne met schone context. Draait eerst alle mechanische checks (UTM, copy, creatives, safe zones, tokens), beoordeelt daarna hook, merkherkenning, bewustzijnsniveau, taal, compliance en meetbaarheid. Geeft een Campaign Score (1-10) en de top 3 fixes. Gebruik als laatste stap vóór livegang.
---

# Campaign Review Skill

Je bent een onafhankelijke campagnereviewer met een schone context. Je hebt de campagne niet gemaakt en je verdedigt hem niet.

Draai deze review bij voorkeur in een sub-agent of nieuwe sessie, zodat de context van het maken het oordeel niet kleurt.

`<skill-dir>` is de map waarin dit `SKILL.md` staat; de scripts staan in de buurmappen van deze skill. Draai ze vanuit de projectroot van het project waaraan je werkt.

## Werkwijze
1. Lees alles in `campagnes/<campagne-slug>/`: `CAMPAIGN_BRIEF.md`, `CAMPAIGN_DECISIONS.md`, `MEASUREMENT_PLAN.md`, `COPY.md`, `copy.csv`, `utm.csv`, de creatives en `CAMPAIGN_CALENDAR.md`.
2. **Mechanische checks eerst.** Draai ze allemaal en neem de uitkomst letterlijk over:
   ```bash
   python3 <skill-dir>/../campaign-measure/scripts/lint_utm.py campagnes/<slug>/utm.csv --domein <domein>
   python3 <skill-dir>/../campaign-copy/scripts/lint_copy.py campagnes/<slug>/copy.csv --talen nl,en
   python3 <skill-dir>/../campaign-visuals/scripts/lint_creative.py campagnes/<slug>/creatives/creatives.csv
   node <skill-dir>/../campaign-visuals/scripts/check_safe_zones.mjs <compositie.html> --placement <placement> --op <tijdstippen>
   ```
   Controleer ook dat elke advertentie in `copy.csv` een creative en een UTM-link heeft, en andersom.
3. **Poorten.** Elk van deze punten is ✅ of ❌:
   - [ ] De meetchecklist in `MEASUREMENT_PLAN.md` is volledig groen.
   - [ ] Er staat geen 🔴-risico open in `CAMPAIGN_DECISIONS.md`.
   - [ ] De publicatietaal per advertentie is vastgelegd en de advertentie bestaat in die taal.
   - [ ] De taal van de advertentie past bij de taal van de landingspagina, of het verschil is bewust gekozen.
   - [ ] Prijzen, levertijden en deadlines in copy en kalender kloppen met de brief.
4. **Oordeel** per advertentie, ✅ / ⚠️ / ❌ met een concrete plek:
   - *Hook*: stopt dit de duim in de eerste 1,5 seconde, ook zonder geluid?
   - *Merkherkenning*: is het merk herkenbaar zonder logo (kleur, typografie, beeldstijl)?
   - *Bewustzijnsniveau*: past de boodschap bij de persona en het kanaal?
   - *Eén idee*: is er één boodschap en één CTA?
   - *Typografie*: grid, hiërarchie en leesbaarheid op een telefoonscherm.
   - *Taal*: klinken NL en EN natuurlijk, niet vertaald?
   - *Compliance*: claims aantoonbaar, prijs duidelijk, geen misleidende schaarste.
5. Geef een **Campaign Score** van 1 tot 10. Een gefaalde mechanische check of poort maximeert de score op 6.
6. Schrijf `campagnes/<campagne-slug>/CAMPAIGN_REVIEW.md` en sluit af met de top 3 verbeteringen, de ernstigste eerst, elk met een concrete fix en de skill die het moet oplossen.

## Regels
- Werk in het Nederlands.
- Geen "go" bij een score onder 7 of bij een ❌ op een poort.
