# Tests

`pytest` is configured in [pyproject.toml](../pyproject.toml) (`pythonpath = src`, `testpaths = tests`).

| Area | Files |
|------|--------|
| MCP / agents | `test_agents.py`, `test_server.py`, … |
| Hooks | `test_hooks_prompt.py`, `test_hooks_shell.py`, `test_hooks_edit.py`, `test_hooks_stop.py` |
| Prompts & rubrics | [`prompts/`](./prompts/), [`rubrics/`](./rubrics/) — manual / rubric-driven rule evaluation |

**Run:** `pytest tests/ -v` (see [CLAUDE.md](../CLAUDE.md)).
