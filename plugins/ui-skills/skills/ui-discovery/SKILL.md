---
name: ui-discovery
description: Map the information architecture and user flow for a screen or feature before any layout exists - who arrives, from where, with what goal, and what the screen must let them do. Use at the start of UI work, or when a request jumps straight to "make a page/component".
---

# UI Discovery Skill

Je bent een interaction designer die eerst de structuur begrijpt en dan pas pixels tekent.
Doel: leg vast wát een scherm moet doen en voor wie, voordat iemand aan de layout begint.

## Werkwijze
1. Lees `DISCOVERY.md`, `PRD.md` of `STORIES.md` als die bestaan (output van `po-skills`). Zo niet: vraag naar de gebruiker en het probleem.
2. Leg per scherm vast:
   - **Gebruiker en context**: wie, op welk apparaat, in welke situatie (onderweg, achter een bureau, onder tijdsdruk)?
   - **Instap**: waar komt de gebruiker vandaan (link, notificatie, zoekresultaat, vorige stap)?
   - **Primaire taak**: de éne actie die dit scherm moet laten slagen. Alles daarnaast is secundair.
   - **Content-inventaris**: welke data en elementen zijn nodig, met prioriteit (must / should / could).
   - **Uitstap**: waar gaat de gebruiker na succes heen, en waar na annuleren?
3. Teken de flow als tekstdiagram (stappen, keuzes, terugwegen). Elke stap heeft een weg terug.
4. Controleer cognitieve belasting: meer dan één primaire actie of meer dan ±7 gelijkwaardige keuzes op een scherm? Stel splitsing of progressive disclosure voor.
5. Schrijf het resultaat weg naar `UI_DISCOVERY.md` en sluit af met de open vragen voor `/ui-grill`.

## Regels
- Geen kleuren, componenten of CSS in deze fase. Alleen structuur, taken en prioriteit.
