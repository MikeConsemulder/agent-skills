# Product Owner Skills for Claude Code (`po-skills`)

> Production-grade agent skills for modern Product Owners. Stop the feature factory: Discovery, Grilling, PRD Drafting, and DoR Linting.

## Philosophy & Inspirations
- **Architectural Mechanics:** Inspired by **Matt Pocock** (AI Hero / Total TypeScript) – focusing on progressive disclosure, isolated review contexts, and zero fluff.
- **Product Discovery:** Driven by **Teresa Torres** (*Continuous Discovery Habits*) and **Marty Cagan** (*Inspired* / *Empowered*).
- **Execution & Grilling:** Channeling **Claire Vo** (ChatPRD) for adversarial edge-case analysis.

## Skills Included
- `/po-discovery`: Problem space triage & 4-risk analysis.
- `/po-grill`: Adversarial interviewing on assumptions & non-goals.
- `/po-draft`: Clean, INVEST-compliant story/PRD authoring.
- `/po-review`: Sub-agent linter for Definition of Ready & Ambiguity.

## Recommended flow

```
/po-discovery  →  DISCOVERY.md
/po-grill      →  DECISIONS.md (+ GLOSSARY.md)
/po-draft      →  PRD.md / STORIES.md
/po-review     →  Ambiguity Score + fixes
```

## Installation

Add this repository as a marketplace in Claude Code:

```bash
claude plugin marketplace add MikeConsemulder/po-skills
```

Install the plugin:

```bash
claude plugin install po-skills@mikeconsemulder-marketplace
```

## License

MIT – see [LICENSE](LICENSE).
