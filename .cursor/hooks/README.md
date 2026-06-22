# Cursor lifecycle hooks

Deterministic **Python 3** scripts — **stdlib only**, no pip dependencies. They communicate via **stdin JSON / stdout JSON** as required by Cursor.

**Active entrypoints:** `.cursor/hooks.json` invokes the scripts under `scripts/`:

| Script | Event (see `hooks.json`) | Role |
|--------|--------------------------|------|
| `scripts/user-prompt-submit.py` | `beforeSubmitPrompt` | Agent scoring, learned-pattern injection (`systemMessage`); stdout informational. |
| `scripts/shell-guard.py` | `beforeShellExecution` | Shell guard — **only** hook that may **deny** execution. |
| `scripts/post-edit.py` | `afterFileEdit` | Log edits; diagnostic `ruff check` / `tsc` (never `--fix`). |
| `scripts/stop.py` | `stop` | Session outcome (4-gate), recap, durable outbox write. |

**Shared (`lib/`):** `_common.py` (paths, logging, `~/.omnicursor/events.jsonl`, session JSON helpers), `agent_scoring.py`, `pattern_loader.py`, `prompt_pattern_selection.py`, `emit_client.py` (Unix socket, `OMNICURSOR_EMIT_SOCKET`), and `pattern_sync.py` (optional omniintelligence HTTP pull — runs only when `OMNICURSOR_PATTERN_SYNC_HTTP=1`; default off). DoD/dispatch-claim regexes live under repo `config/`.

**Constraints:** stdlib only in hook processes; always exit 0 (failures are logged, not propagated); only `shell-guard` may deny. See [docs/ARCHITECTURE.md §4](../../docs/ARCHITECTURE.md#4-hooks). Tests live under `tests/test_hooks_*.py` and `tests/test_suite_event*.py`.
