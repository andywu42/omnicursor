# Cursor lifecycle hooks

Deterministic **Python 3** scripts — **stdlib only**, no pip dependencies. They communicate via **stdin JSON / stdout JSON** as required by Cursor.

| Script | Event (see `hooks.json`) | Role |
|--------|--------------------------|------|
| `on_prompt.py` | `beforeSubmitPrompt` | Classify prompt; log (stdout is informational only). |
| `on_shell.py` | `beforeShellExecution` | Shell guard — **only** hook that may **deny** execution. |
| `on_edit.py` | `afterFileEdit` | Log edits; diagnostic `ruff check` on Python (never `--fix`). |
| `on_stop.py` | `stop` | Session metrics under `~/.omnicursor/sessions/`. |

**Shared:** `_common.py` — paths, logging helpers, event append to `~/.omnicursor/events.jsonl`.

**Constraints:** Summarized in [CLAUDE.md](../../CLAUDE.md). Tests live under `tests/test_hooks_*.py`.
