# OmniCursor

Cursor-native MCP integration layer for OmniNode.

OmniCursor is the Cursor equivalent of `omniclaude`: a thin integration layer that combines Cursor rules with MCP tools so Cursor can approximate OmniNode's routing, skill invocation, and compliance workflow without Claude Code lifecycle hooks.

## Current Status

**Phase 2 complete.** The repository now has:

- 7 Cursor rules under [`.cursor/rules/`](./.cursor/rules/) (5 with MCP integration, 2 always-on foundation rules)
- 3 MCP tools: `get_agent_context`, `invoke_skill`, `check_compliance`
- 5 local skills: systematic-debugging, brainstorming, writing-plans, plan-ticket, adapter-stub
- Compliance registry with keyword-based output validation for all 5 skills
- Agent routing system with 5 categories + generalist fallback

Not implemented yet:

- Kafka pipeline
- Qdrant or production pattern storage
- Full Linear integration
- Full ONEX runtime parity

## Architecture

OmniCursor has two layers:

1. **Cursor rules** as the behavior and routing surface
2. **MCP tools** as the structured backend interface

The preserved rules are the primary interaction model. The MCP backend complements them with structured routing, skill loading, and compliance validation.

### MCP Tools

| Tool | Purpose |
|------|---------|
| `get_agent_context(category)` | Returns routing context for a rule-selected category |
| `invoke_skill(skill_name)` | Loads a Markdown skill from the `skills/` directory |
| `check_compliance(skill_name, response_summary)` | Validates model output against a skill's expected pattern |

### Skills

| Skill | Purpose |
|-------|---------|
| `systematic-debugging` | Reproduce, hypothesize, verify, fix |
| `brainstorming` | Refine ideas into design docs through collaborative dialogue |
| `writing-plans` | Convert designs into TDD implementation plans |
| `plan-ticket` | Generate YAML ticket contract templates with repo detection |
| `adapter-stub` | Bucket 3 dry-run stubs with fail-soft behavior |

### Routing Categories

| Category | Agent | Rule |
|----------|-------|------|
| `debugging` | systematic-debugger | 10-systematic-debugging.mdc |
| `brainstorming` | brainstorming-guide | 10-brainstorming.mdc |
| `planning` | plan-writer | 11-writing-plans.mdc |
| `ticketing` | ticket-planner | 12-plan-ticket.mdc |
| `adapter` | adapter-guide | 20-adapter-stub.mdc |

## Quick Start

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
omnicursor-server
```

See [`docs/QUICKSTART.md`](./docs/QUICKSTART.md) for full setup instructions.

## Repository Layout

```text
OmniCursor/
├── .cursor/rules/          # 7 Cursor rules
├── docs/                   # Architecture, quickstart, guides
├── skills/                 # 5 Markdown skill files
├── src/omnicursor/         # Python MCP backend
├── tests/                  # Unit tests + prompts + rubrics
├── pyproject.toml          # Package config
└── OMNICLAUDE_SKILLS.md    # Read-only skill reference
```

## Documentation

- [`docs/QUICKSTART.md`](./docs/QUICKSTART.md) — Setup and end-to-end flow
- [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) — Bucket model and frozen adapter contract
- [`docs/DEVELOPER.md`](./docs/DEVELOPER.md) — Mapping from starter kit to backend
- [`docs/STUDENT_GUIDE.md`](./docs/STUDENT_GUIDE.md) — Capstone project roadmap
- [`HOW_TO_RUN_IN_CURSOR.md`](./HOW_TO_RUN_IN_CURSOR.md) — Original starter-pack guide

## Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```
