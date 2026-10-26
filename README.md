# Claude Skills by Mike Consemulder (`claude-skills`)

> Production-grade agent skills for Product Owners and UI designers in Claude Code. Problem first, every state designed, mechanical checks enforced by scripts.

Built in the spirit of **Matt Pocock**'s agent skills for developers – progressive disclosure, isolated review contexts, zero fluff – and translated to product management and UI design.

## Plugins

| Plugin | For | Skills |
| --- | --- | --- |
| [`po-skills`](plugins/po-skills) | Product Owners | `/po-discovery` → `/po-grill` → `/po-draft` → `/po-review` |
| [`ui-skills`](plugins/ui-skills) | UI/UX designers & design engineers | `/design-tokens` → `/ui-discovery` → `/ui-grill` → `/ui-draft` → `/ui-review` |

The two chain together: `po-skills` produces `DISCOVERY.md` and `PRD.md`/`STORIES.md`, which `/ui-discovery` reads as input.

## Installation

Add this repository as a marketplace in Claude Code:

```bash
claude plugin marketplace add MikeConsemulder/claude-skills
```

Install one or both plugins:

```bash
claude plugin install po-skills@mikeconsemulder-marketplace
claude plugin install ui-skills@mikeconsemulder-marketplace
```

## Credits & Inspirations

- **Matt Pocock** (AI Hero / Total TypeScript) – architectural mechanics: progressive disclosure, sub-agent reviews with clean context, deterministic checks over prompts.
- **Marty Cagan** (*Inspired* / *Empowered*) and **Teresa Torres** (*Continuous Discovery Habits*) – product discovery.
- **Claire Vo** (ChatPRD) – adversarial grilling of requirements.
- **Brad Frost** (*Atomic Design*) – design systems and design tokens.
- **Jakob Nielsen** (Nielsen Norman Group) – 10 Usability Heuristics.
- **Scott Hurff** (*Designing Products People Love*) – the 5 UI states.
- **Jordan Singer** (Diagram / Figma AI) – agentic design workflows.

## Repository layout

```
.claude-plugin/marketplace.json   marketplace listing both plugins
plugins/
  po-skills/                      .claude-plugin/plugin.json + skills/
  ui-skills/                      .claude-plugin/plugin.json + skills/
```

## License

MIT – see [LICENSE](LICENSE).
