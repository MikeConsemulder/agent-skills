# Agent Skills by Mike Consemulder (`agent-skills`)

> Production-grade agent skills for Product Owners and UI designers. Problem first, every state designed, mechanical checks enforced by scripts.

Every skill is a plain `SKILL.md` (Markdown with `name`/`description` frontmatter), the open Agent Skills format. They are not tied to one tool: use them in any AI agent that loads `SKILL.md` skills, or paste a skill's contents into any other agent as instructions. Helper scripts are dependency-free Python 3.

Built in the spirit of **Matt Pocock**'s agent skills for developers – progressive disclosure, isolated review contexts, zero fluff – and translated to product management and UI design.

## Skill packs

| Pack | For | Skills |
| --- | --- | --- |
| [`po-skills`](plugins/po-skills) | Product Owners | `po-discovery` → `po-grill` → `po-draft` → `po-review` |
| [`ui-skills`](plugins/ui-skills) | UI/UX designers & design engineers | `design-tokens` → `ui-discovery` → `ui-grill` → `ui-draft` → `ui-review` |

The two chain together: `po-skills` produces `DISCOVERY.md` and `PRD.md`/`STORIES.md`, which `ui-discovery` reads as input. All state lives in plain Markdown/JSON files in your project, so you can switch agents mid-flow.

## Installation

### Any agent that supports `SKILL.md`

Copy the skill folders into the skills directory your agent reads (see its docs), keeping each folder intact:

```bash
git clone https://github.com/MikeConsemulder/agent-skills.git
cp -r agent-skills/plugins/po-skills/skills/* <your-agent-skills-dir>/
cp -r agent-skills/plugins/ui-skills/skills/* <your-agent-skills-dir>/
```

Copy the `ui-skills` folders together: `ui-draft` and `ui-review` call the linter in `design-tokens`.

### Agents without skill support

Paste the body of a `SKILL.md` into the agent as its instructions, and run the scripts in `scripts/` yourself.

### Claude Code (plugin marketplace)

This repo also ships `.claude-plugin` manifests, so Claude Code can install the packs as plugins:

```bash
claude plugin marketplace add MikeConsemulder/agent-skills
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
plugins/
  po-skills/skills/<skill>/SKILL.md          the skills (tool-agnostic)
  ui-skills/skills/<skill>/SKILL.md (+ scripts/, assets/)
  */.claude-plugin/plugin.json               Claude Code adapter
.claude-plugin/marketplace.json              Claude Code adapter
```

## License

MIT – see [LICENSE](LICENSE).
