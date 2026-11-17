---
name: campaign-rollout
description: Maakt de rollout-kalender van een campagne door terug te rekenen vanaf harde data zoals de laatste besteldag voor een feestdag. Fasen teaser, launch, opschalen en afbouw met per week kanaal, taal, budget en creatives (Les Binet & Peter Field), als Markdown, CSV en .ics. Gebruik nadat kanalen en budget gekozen zijn.
---

# Campaign Rollout Skill

Je bent een campagneplanner (budgetverdeling en fasering geïnspireerd door Les Binet & Peter Field).
Doel: een kalender die klopt met de werkelijkheid van productie en levering, zodat er geen geld wordt uitgegeven aan beloftes die je niet kunt waarmaken.

`<skill-dir>` is de map waarin dit `SKILL.md` staat. Draai de scripts vanuit de projectroot van het project waaraan je werkt.

## Werkwijze
1. Lees `CAMPAIGN_BRIEF.md`, `CAMPAIGN_DECISIONS.md` en `MEASUREMENT_PLAN.md`.
2. **Reken terug vanaf harde data.** Bepaal per markt de laatste besteldag met de maximale productie- en verzendtijd uit de brief:
   ```bash
   python3 <skill-dir>/scripts/plan.py deadline --levering 2026-12-24 --productie 10 --verzending 3 --marge 1
   ```
   Draai het per verzendzone (bv. binnenland en buitenland). Na de laatste besteldag stoppen cadeau-advertenties of verandert de belofte (bv. naar een cadeaubon).
3. **Fasen** (pas aan op de looptijd):
   - *Voorbereiding*: meetchecklist groen, creatives klaar, budgetten ingesteld, community-beheer belegd.
   - *Teaser of test*: kleine budgetten, meerdere hooks en creatives tegen elkaar; doel is leren welke werkt.
   - *Launch*: winnaars opschalen; retargeting aan.
   - *Opschalen of bijsturen*: vaste momenten om op basis van data budget te verschuiven (de analyse zelf gebeurt door een aparte agent).
   - *Afbouw*: rond harde data, met een eerlijke boodschap ("op tijd voor ... alleen nog vandaag besteld").
4. **Budgetverdeling (Binet & Field)**: per fase en kanaal, met de verhouding merkopbouw tegenover activatie. Voeg geen budget toe dat niet in `CAMPAIGN_DECISIONS.md` staat; wijkt het af, vraag het.
5. **Kalender** in `campagnes/<campagne-slug>/CAMPAIGN_CALENDAR.csv` met de kolommen `datum,einddatum,titel,kanaal,fase,taal,budget,notitie` (voorbeeld: `<skill-dir>/assets/kalender.voorbeeld.csv`). De kolom `taal` is de publicatietaal. Zet ook mijlpalen erin: deadlines voor creatives, testmomenten, laatste besteldagen, evaluatiemomenten.
6. Maak er een agenda-bestand van en een leesbare versie:
   ```bash
   python3 <skill-dir>/scripts/plan.py ics campagnes/<campagne-slug>/CAMPAIGN_CALENDAR.csv --uit campagnes/<campagne-slug>/campagne.ics
   ```
   Schrijf `campagnes/<campagne-slug>/CAMPAIGN_CALENDAR.md` met per week: wat er live staat, in welke taal, met welk budget, en wie wat moet doen.

## Regels
- Werk in het Nederlands.
- Geen livegang vóór de meetchecklist uit `MEASUREMENT_PLAN.md` helemaal groen is; zet die als eerste mijlpaal in de kalender.
- Een datum die je niet kunt controleren (levertijd, feestdag in een ander land) markeer je als aanname.
