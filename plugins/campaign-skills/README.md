# `campaign-skills` – Campagne Skills

Advertentie- en socialcampagnes van A tot Z: van positionering tot rollout-kalender, met visuals en video's die volledig in webtechnologie gemaakt worden. Alles in het Nederlands; advertentiecopy altijd in het Nederlands én het Engels, en de agent vraagt in welke taal er gepubliceerd wordt.

| Skill | Wat het doet | Denker | Output |
| --- | --- | --- | --- |
| `/campaign-discovery` | Positionering, category entry points, doelgroepen, aanbod, tone of voice, publicatietalen | April Dunford, Byron Sharp & Jenni Romaniuk | `CAMPAIGN_BRIEF.md` |
| `/campaign-grill` | Stelt kanalen, doelgroepen en budget voor; pre-mortem op meten, AVG, Reclame Code, rechten, operatie | Gary Klein, Les Binet & Peter Field | `CAMPAIGN_DECISIONS.md` |
| `/campaign-measure` | Meetplan, livegang-checklist, UTM-naamgeving — de poort | Avinash Kaushik | `MEASUREMENT_PLAN.md`, `utm.csv` |
| `/campaign-copy` | Hooks en copy per bewustzijnsniveau, NL + EN | Eugene Schwartz | `COPY.md`, `copy.csv` |
| `/campaign-visuals` | Statics en video's in HTML/GSAP via HyperFrames, gridtypografie op tokens | Josef Müller-Brockmann, Brad Frost | `creatives/` |
| `/campaign-rollout` | Terugrekenen vanaf harde data, fasen, budget per week, agenda | Les Binet & Peter Field | `CAMPAIGN_CALENDAR.md/.csv`, `campagne.ics` |
| `/campaign-review` | Schone-context eindcontrole met alle checks en poorten | – | `CAMPAIGN_REVIEW.md` + Campaign Score |

Alle campagnebestanden komen in `campagnes/<campagne-slug>/` in je eigen project. De analyse ná livegang hoort bij een aparte agent; deze skills zorgen dat de data daarvoor compleet is.

## Mechanisch vs. oordeel

Wat te berekenen is, controleert een script (Python 3 zonder dependencies, plus één Node-script met Playwright):

```bash
# UTM-links: naamgeving, uniek, https, geen hardgecodeerde klik-ID's
python3 skills/campaign-measure/scripts/lint_utm.py utm.csv --domein voorbeeld.nl

# Copy: tekenlimieten per kanaal, NL + EN compleet, claims die onderbouwing nodig hebben
python3 skills/campaign-copy/scripts/lint_copy.py copy.csv --talen nl,en

# Exports: verhouding, afmetingen, duur, codec, bestandsgrootte (ffprobe)
python3 skills/campaign-visuals/scripts/lint_creative.py creatives.csv

# HTML-composities: tekst buiten de safe zones en groot genoeg, op meerdere tijdstippen
node skills/campaign-visuals/scripts/check_safe_zones.mjs compositie.html --placement meta_reels_9x16 --op 0,1500,4000

# Laatste besteldag (werkdagen, NL-feestdagen) en kalender naar .ics
python3 skills/campaign-rollout/scripts/plan.py deadline --levering 2026-12-24 --productie 10 --verzending 3
python3 skills/campaign-rollout/scripts/plan.py ics CAMPAIGN_CALENDAR.csv --uit campagne.ics
```

Tekenlimieten, formaten en safe zones staan in `assets/*.json` en zijn richtlijnen: platforms wijzigen ze. Pas die bestanden aan als de specs veranderen.

## Afhankelijkheden

- `campaign-visuals` gebruikt [HyperFrames](https://github.com/heygen-com/hyperframes) (`npx skills add heygen-com/hyperframes`, Node.js 22+, FFmpeg) en de token-linter uit `ui-skills`. Installeer `ui-skills` dus ook.
- `check_safe_zones.mjs` vraagt Playwright met Chromium.

Werkt in elke agent die `SKILL.md`-skills laadt; zie de [root-README](../../README.md#installation) voor installatie.
