# OmniCursor Execution Plan

## Current Slice

This first vertical slice delivers:

- repo-root Cursor rules preserved and reusable
- a minimal MCP server
- `get_agent_context`
- `invoke_skill`
- the first real local skill: `systematic-debugging`
- the first MCP-aware rule: `10-systematic-debugging`

## Build Order

1. Preserve and root the starter-kit rules, docs, prompts, and rubrics
2. Add the MCP package skeleton under `src/omnicursor/`
3. Implement routing context and skill loading
4. Add the debugging skill and its rule
5. Verify basic imports, tests, and run docs

## Next Tasks

1. Add `check_compliance` as the next real MCP tool
2. Add a small pattern storage path behind `patterns.py`
3. Port the preserved brainstorming, writing-plans, and plan-ticket behavior into reusable `skills/*.md`
4. Decide whether the preserved starter-kit docs should be rewritten or versioned as "legacy starter-pack" docs
5. Add a demo-oriented Cursor MCP config example after the local Python baseline is settled

