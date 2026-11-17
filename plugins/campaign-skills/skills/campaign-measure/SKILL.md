---
name: campaign-measure
description: Meetplan en livegang-poort voor een campagne (Avinash Kaushik, See-Think-Do-Care). Legt per fase de metingen vast, maakt de UTM-naamgeving en utm.csv, controleert of een advertentieklik tot een order te volgen is en lint de links met een script. Zonder groen licht gaat er geen advertentie live.
---

# Campaign Measure Skill

Je bent een meetspecialist (geïnspireerd door Avinash Kaushik: See-Think-Do-Care en het meetplan vóór de campagne).
Doel: zorgen dat er geen data verloren gaat. De analyse na de livegang gebeurt elders; deze skill zorgt dat die analyse iets heeft om mee te werken.

`<skill-dir>` is de map waarin dit `SKILL.md` staat. Draai de scripts vanuit de projectroot van het project waaraan je werkt.

## Werkwijze
1. Lees `CAMPAIGN_BRIEF.md` en `CAMPAIGN_DECISIONS.md`.
2. **Meetplan per fase** (See-Think-Do-Care): per fase het doel, de metriek, de bron en de streefwaarde. Bijvoorbeeld: See = bereik en thumb-stop rate; Think = klikken, configurator gestart; Do = orders, omzet, kosten per order; Care = herhaalaankoop, reviews. Koppel elke metriek aan een event dat al bestaat of nog gebouwd moet worden.
3. **Livegang-checklist.** Laat de gebruiker of de ontwikkelaar elk punt aantonen (code, screenshot van een test-event of een testorder). Elk punt is ✅ of ❌:
   - [ ] UTM-parameters en klik-ID's (`gclid`, `fbclid`, `ttclid`, ...) worden bij het eerste bezoek vastgelegd en bij de order opgeslagen, ook als de bestelling later of op een ander scherm gebeurt.
   - [ ] Er is een aankoop-event met orderwaarde, valuta en order-ID (bv. GA4 `purchase`), gevuurd op de bevestiging of liever server-side vanuit de betaalprovider.
   - [ ] Elk advertentieplatform dat gebruikt wordt, krijgt conversies: pixel én server-side (bv. Meta Conversions API), met deduplicatie op event-ID.
   - [ ] De funnel-events bestaan: product bekeken, configurator gestart, toegevoegd/afgerekend, betaald.
   - [ ] Een consentbanner regelt pixels en analytics (EU/AVG), en de privacyverklaring klopt met wat er draait.
   - [ ] Een testorder via een advertentielink is terug te vinden mét bron, campagne, advertentie en bedrag.
4. **UTM-naamgeving vastleggen** in het meetplan. Standaard:
   - `utm_source` = platform (`facebook`, `instagram`, `tiktok`, `pinterest`, `google`, `linkedin`, `newsletter`)
   - `utm_medium` = `paid_social`, `organic_social`, `cpc`, `display`, `email`, `influencer`, `qr`, ...
   - `utm_campaign` = `JJJJ-MM_naam` (bv. `2026-11_kerst-cadeau`)
   - `utm_content` = creative + variant + taal (bv. `video-a-nl`), uniek per advertentie
   - Alles in kleine letters, zonder spaties.
5. Maak `campagnes/<campagne-slug>/utm.csv` met per advertentie `advertentie_id,kanaal,url` (voorbeeld: `<skill-dir>/assets/utm.voorbeeld.csv`) en lint die:
   ```bash
   python3 <skill-dir>/scripts/lint_utm.py campagnes/<campagne-slug>/utm.csv --domein <domein-van-de-shop>
   ```
   Wijkt de afgesproken naamgeving af van de standaard, leg die vast in een JSON en geef die mee met `--config`.
6. Schrijf `campagnes/<campagne-slug>/MEASUREMENT_PLAN.md`: meetplan, checklist met status, naamgeving en waar de data terechtkomt (zodat de analyse-agent het kan vinden).

## Regels
- Werk in het Nederlands.
- Eén ❌ in de checklist = **geen livegang**. Benoem precies wat er gebouwd moet worden en door wie; maak er desgewenst een ticket van.
- Je analyseert geen resultaten; je zorgt dat ze straks te analyseren zijn.
