# `omnicursor` package

FastMCP backend for Cursor: **three tools**, shared models with hooks where applicable.

| Module | Responsibility |
|--------|----------------|
| [`server.py`](./server.py) | FastMCP app; registers `get_agent_context`, `invoke_skill`, `check_compliance`. |
| [`agents.py`](./agents.py) | Merge hardcoded categories + `.cursor/agents/*.json`; `match_agent()`, `get_agent_context()`. |
| [`skills.py`](./skills.py) | Load Markdown from repo `skills/`. |
| [`compliance.py`](./compliance.py) | Keyword-style checks per skill. |
| [`schemas.py`](./schemas.py) | Pydantic v2 models (`AgentContext`, `SkillDocument`, `ComplianceResult`, …). |
| [`db.py`](./db.py) | `REPO_ROOT`, `SKILLS_DIR`, `RULES_DIR`; placeholder `InMemoryDatabase` / health shape. |
| [`patterns.py`](./patterns.py) | Lists preserved rule paths as a small “pattern catalog” for APIs/tests. |
| [`__init__.py`](./__init__.py) | Package version. |

**Run:** `omnicursor-server` (after editable install). **Tests:** `pytest tests/` from repo root.
