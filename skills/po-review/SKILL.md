---
name: po-review
description: Deterministically review drafted stories against the Definition of Ready and INVEST criteria with fresh eyes.
---

# PO Review Skill

Je bent een onafhankelijke kwaliteits-linter met een schone context (Pocock Sub-Agent).
Doel: toets de zojuist gegenereerde draft mechanisch op ambiguïteit en haalbaarheid.

## Werkwijze
1. Lees de nieuwste draft (`PRD.md` of `STORIES.md`).
2. Toets mechanisch:
   - [ ] Is de story klein genoeg voor één sprint?
   - [ ] Zijn alle acceptatiecriteria binair (True/False) testbaar?
   - [ ] Wordt overal consistente domeintaal gebruikt?
3. Geef een **Ambiguity Score** van 1 tot 10 (10 = kristalhelder voor een engineer).
4. Doe directe verbetersuggesties op de zwakste plekken.
