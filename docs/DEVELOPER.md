# OmniCursor Developer Notes

## Preserved Starter-Kit Inputs

These existing files were reviewed and intentionally preserved as the architectural base:

- [`.cursor/rules/00-omninode-concepts.mdc`](../.cursor/rules/00-omninode-concepts.mdc): always-on vocabulary, pipeline stages, bucket boundaries
- [`.cursor/rules/01-codebase-research.mdc`](../.cursor/rules/01-codebase-research.mdc): bounded file-research guard
- [`.cursor/rules/10-brainstorming.mdc`](../.cursor/rules/10-brainstorming.mdc): idea-to-design methodology
- [`.cursor/rules/11-writing-plans.mdc`](../.cursor/rules/11-writing-plans.mdc): design-to-plan methodology
- [`.cursor/rules/12-plan-ticket.mdc`](../.cursor/rules/12-plan-ticket.mdc): bounded repo detection and YAML ticket template generation
- [`.cursor/rules/20-adapter-stub.mdc`](../.cursor/rules/20-adapter-stub.mdc): Bucket 3 dry-run and fail-soft pattern
- [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md): frozen adapter contract and bucket rules
- [`docs/STUDENT_GUIDE.md`](./STUDENT_GUIDE.md): execution and grading flow
- [`docs/SKILL_TRANSLATION_TEMPLATE.md`](./SKILL_TRANSLATION_TEMPLATE.md): rule-porting template
- [`tests/prompts`](../tests/prompts): prompt fixtures for rule behavior
- [`tests/rubrics`](../tests/rubrics): pass/fail criteria for the preserved rules
- [`HOW_TO_RUN_IN_CURSOR.md`](../HOW_TO_RUN_IN_CURSOR.md): original starter-pack setup instructions
- [`OMNICLAUDE_SKILLS.md`](../OMNICLAUDE_SKILLS.md): skill inventory to mine for future ports
- [`OmniCursor_Architecture_Visual_Guide55.pages`](../OmniCursor_Architecture_Visual_Guide55.pages): visual blueprint for the repo direction

## Architectural Mapping

The preserved rules stay as the top-level behavior layer inside Cursor.
The new MCP backend adds structured services underneath them:

- Routing remains rule-driven and is approximated through self-classification plus `get_agent_context`
- Skill loading is handled by `invoke_skill`
- Compliance and pattern storage are left as placeholders so the package shape matches the architecture without pretending those features are done

This means OmniCursor extends the existing starter kit instead of bypassing it.

## New Python Modules

- [`src/omnicursor/server.py`](../src/omnicursor/server.py): FastMCP server and tool registration
- [`src/omnicursor/agents.py`](../src/omnicursor/agents.py): category-to-agent context mapping
- [`src/omnicursor/skills.py`](../src/omnicursor/skills.py): local Markdown skill loader
- [`src/omnicursor/schemas.py`](../src/omnicursor/schemas.py): Pydantic response models
- [`src/omnicursor/compliance.py`](../src/omnicursor/compliance.py): minimal placeholder for the next slice
- [`src/omnicursor/patterns.py`](../src/omnicursor/patterns.py): preserved-rule pattern registry placeholder
- [`src/omnicursor/db.py`](../src/omnicursor/db.py): repo paths and in-memory storage placeholder

## How `get_agent_context` Integrates With Existing Rules

`get_agent_context` is not a second routing system.
It is a small MCP helper that a rule can call after self-classifying the request.

For example:

- `10-systematic-debugging.mdc` classifies a debugging request as `debugging`
- it calls `get_agent_context("debugging")`
- it then calls `invoke_skill("systematic-debugging")`
- the always-on preserved rules still provide vocabulary and bounded research constraints

For non-debug flows, the preserved rules continue to be the primary execution layer.
