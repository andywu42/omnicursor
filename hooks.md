# Hooks in OmniCursor

## What Hooks Are

Hooks are lifecycle scripts that fire at defined points in an AI coding session. Both Claude Code (OmniClaude) and Cursor support hooks, but their surfaces are different. A hook receives a JSON payload via stdin, does work (classifies, guards, logs, enriches), and writes a JSON response to stdout. The hook process exits 0 — the response payload, not the exit code, controls behavior.

The key distinction: **some hooks are informational** (the IDE ignores stdout, the hook just logs) and **some are decisional** (the hook's response actively changes what happens next). In Cursor, only `beforeShellExecution` is decisional. Everything else is informational.

---

## How Events Work in OmniClaude

OmniClaude registers hooks in `plugins/onex/hooks/hooks.json`. It has 9 event types. Multiple scripts can fire per event, and `PreToolUse`/`PostToolUse` support regex tool matchers so a script only runs for specific tools.

| Event | Scripts | What Fires |
|---|---|---|
| `SessionStart` | `session-start.sh` | Starts the Kafka emit daemon (Unix socket background process), initializes session state in `~/.onex_state/`. Idempotent — may fire on reconnect. |
| `SessionEnd` | `session-end.sh` | Tears down session state, emits `session-ended` to Kafka. |
| `UserPromptSubmit` | `user-prompt-submit.sh`<br>`user-prompt-delegation-rule.sh`<br>`user_prompt_structured_handoff_nudge.sh` | Three scripts fire per prompt. Routing classifies the prompt and injects agent context. Delegation rule injects a hard behavioral constraint. Nudge fires once per session for complex unstructured prompts. Output: `{"hookSpecificOutput": {"additionalContext": "..."}}`. |
| `PreToolUse` | 13+ scripts with tool matchers | Fires before every tool call (`Edit`, `Write`, `Bash`, MCP tools, etc.). Scripts enforce authorization, pipeline gates, scope gates, convention injection, changeset guards, DoD completion checks, model routing. Can block by exiting non-zero. |
| `PostToolUse` | 13+ scripts with tool matchers | Fires after every tool call. Quality checks, ruff on edits, TSC on TS files, test reminders, auto-checkpoints, auto-hostile-review, delegation counting, git state verification, Kafka emission. |
| `Stop` | `stop.sh` | Session outcome classification, final Kafka emission. |
| `PreCompact` | `pre-compact.sh` | Fires before context window compaction. Emits a probe event. |
| `SubagentStart` | `subagent-start.sh` | Fires when a subagent is spawned. Records the delegation and sets up correlation context. |

OmniClaude's event output format is `{"hookSpecificOutput": {"additionalContext": "..."}}` — Claude Code accumulates `additionalContext` from all scripts that fire for the same event. Cursor's format is `{"systemMessage": "..."}` — these are different protocols and not interchangeable.

---

## What Cursor Exposes

Cursor supports exactly 4 hook events, registered in `.cursor/hooks.json`:

| Event | Analog |
|---|---|
| `beforeSubmitPrompt` | `UserPromptSubmit` |
| `beforeShellExecution` | `PreToolUse` (Bash matcher only) |
| `afterFileEdit` | `PostToolUse` (Edit/Write matchers) |
| `stop` | `Stop` |

`SessionStart`, `SessionEnd`, `PreCompact`, `SubagentStart`, and the full `PreToolUse`/`PostToolUse` surface (with per-tool matchers) have no Cursor equivalent. This is a platform constraint, not a gap that can be worked around in scripts.

---

## Events 1 and 2 — What Was Ported and How Far

### Event 1 — `beforeSubmitPrompt` → `user-prompt-submit.py`

OmniClaude fires three separate scripts for `UserPromptSubmit`. Cursor fires one and uses only the last `systemMessage` if multiple scripts fire, so all three concerns were merged into a single script.

**What was ported in full:**

- **Agent routing** — three-strategy scoring (exact substring → fuzzy SequenceMatcher → keyword overlap), `HARD_FLOOR = 0.55`, fallback to `polymorphic-agent`. 17 agent configs loaded from `.cursor/agents/*.json`.
- **Delegation rule** — fires on every prompt. When the prompt is estimated to be multi-step (≥80 chars + complex verb + connective, or ≥2 complex verbs), the rule is injected with imperative **MUST** language. Otherwise advisory framing. Mirrors `user-prompt-delegation-rule.sh`.
- **Handoff nudge** — fires exactly once per session when a complex (≥50 chars), unstructured prompt is detected. Suppressed for structured prompts (Task:/Scope: fields) and `/skill` invocations. Per-session `handoff_nudge_fired` flag prevents repeat. Mirrors `user_prompt_structured_handoff_nudge.sh`.
- **Agent persona depth** — injects the full agent config: `description`, `instructions` list, `recommended_skill`. The model receives enough context to behave like the selected agent.
- **Relevance-filtered pattern injection** — patterns scored by domain match (1.0/0.6/0.3 base) + keyword overlap boost (up to +0.4). Only patterns scoring ≥0.7 are injected, ranked by score, capped at 5. Irrelevant patterns excluded rather than injected as noise.

**What was added beyond what OmniClaude does:**

- **Fake SessionStart** — `_init_session()` runs on the first prompt of each conversation. Writes `~/.omnicursor/sessions/current.json` with `conversation_id` and `started_at`. Touches a `session_initialized` flag so subsequent calls are no-ops. This is OmniCursor's substitute for `SessionStart`.
- **Correlation ID threading** — `_generate_correlation_id()` produces a 12-char hex UUID per prompt. Written into `current.json` as `latest_correlation_id` on every prompt so Events 2–4 can read it and link their log entries back to the triggering prompt.
- **HTML comment header** — machine-readable metadata block at the top of every `systemMessage`: `agent=`, `confidence=`, `patterns= injected domain=`, `delegation=`, `correlation=`. Parseable by tests without touching the visible Markdown body.
- **Typed event log** — every call writes `event`, `conversation_id`, `correlation_id`, `generation_id`, `matched_agent`, `score`, `reason`, `patterns_injected`, `delegation_required`, `prompt_snippet` (≤100 chars), `hook_duration_ms` to `events.jsonl`.
- **Per-turn state reset** — clears `write_count`, `read_count`, `delegated` flag at the start of each prompt.

**What couldn't be ported:** The three-script separation (routing / delegation / nudge are one merged script in OmniCursor). No Kafka emission — local JSONL only.

---

### Event 2 — `beforeShellExecution` → `shell-guard.py`

OmniClaude's closest analog is `pre_tool_use_bash_guard.sh` under `PreToolUse`. In Cursor, `beforeShellExecution` is the only hook that can actually block execution.

**What was ported:**

- **Two-tier guard** — HARD_BLOCK (9 patterns, `"permission": "deny"`) and SOFT_WARN (11 patterns, `"permission": "allow"` + `agentMessage`). HARD_BLOCK always takes priority.
- **Pattern parity** — identical regex patterns to `on_shell.py`, covering: `rm -rf /`, `rm -rf ~/`, `rm -rf /*`, `mkfs`, `dd if=...of=/dev/`, fork bomb, `--no-verify`, `>/dev/sda`, `base64 --decode | sh` (hard block); `git push --force`, `git reset --hard`, `DROP TABLE/DATABASE`, `TRUNCATE`, `curl|wget ... | sh`, `kill -9`, `chmod 777`, `sudo rm`, `eval` (soft warn).
- **Correlation threading** — reads `latest_correlation_id` from `current.json` (written by Event 1) so shell guard log entries share the prompt's correlation ID.
- **Typed event log** — `event`, `conversation_id`, `correlation_id`, `command` (≤500 chars), `decision`, `reason`, `hook_duration_ms`.

**What couldn't be ported:** OmniClaude's bash guard is one of 13+ `PreToolUse` scripts. The other 12 (authorization shims, pipeline gates, scope gates, convention injectors, changeset guards, DoD guards, model router) have no Cursor equivalent — there is no `PreToolUse` surface, and Cursor's `beforeShellExecution` only fires for shell commands, not for file edits or MCP tool calls.

---

## Implementation

### Files Added

| File | Purpose |
|---|---|
| `.cursor/hooks.json` | Hook registration. Updated `beforeSubmitPrompt` → `scripts/user-prompt-submit.py`, `beforeShellExecution` → `scripts/shell-guard.py`. |
| `.cursor/hooks/lib/_common.py` | Shared library for all hook scripts. Path resolution, `read_stdin`, `write_stdout`, `write_context`, `log_event`, `load_agent_configs`, `read_session_context`. Stdlib only. |
| `.cursor/hooks/lib/pattern_loader.py` | Thread-safe in-memory pattern cache keyed by domain. `warm_from_json`, `is_stale` (10-min threshold), module-level singleton. |
| `.cursor/hooks/scripts/user-prompt-submit.py` | Event 1 implementation. Full agent routing, session identity, correlation ID, relevance-filtered patterns, complexity estimator, delegation enforcement, agent persona, HTML header, handoff nudge, typed event log. |
| `.cursor/hooks/scripts/shell-guard.py` | Event 2 implementation. HARD_BLOCK + SOFT_WARN guard, correlation threading, typed event log. |

### Files Edited

| File | What Changed |
|---|---|
| `.cursor/hooks/lib/_common.py` | Added `read_session_context()` — reads `current.json` for Events 2–4 to retrieve `latest_correlation_id`. |
| `.cursor/hooks/scripts/user-prompt-submit.py` | Added `_update_session_correlation()`, `_init_session()`, `_generate_correlation_id()`, `_estimate_complexity()`, `_score_pattern_relevance()`, `_filter_patterns_by_relevance()`, `_update_session_correlation()`. Updated `build_context()` with `agent_config`, `correlation_id`, `delegation_required` params, HTML comment header, agent persona section, hard vs advisory delegation framing. Updated `main()` to wire all new logic and emit typed events. |

### Architecture

All hook scripts follow the same pattern:

```
Cursor → stdin JSON → script → stdout JSON → Cursor
                         ↓
                  ~/.omnicursor/events.jsonl  (append)
                  ~/.omnicursor/sessions/     (state files)
```

The shared lib (`_common.py`, `pattern_loader.py`) lives at `.cursor/hooks/lib/` and is added to `sys.path` at the top of each script via:
```python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
```

Session state is file-based under `~/.omnicursor/sessions/<conversation_id>/`:

```
session_initialized      — flag: first prompt has run (fake SessionStart)
handoff_nudge_fired      — flag: nudge has fired this session
write_count              — per-turn counter reset each prompt
read_count               — per-turn counter reset each prompt
delegated                — flag cleared each prompt
```

`current.json` at `~/.omnicursor/sessions/current.json` is the cross-event bridge:
```json
{
  "conversation_id": "abc-123",
  "started_at": "2026-04-14T00:00:00+00:00",
  "latest_correlation_id": "a3f9c2d14e8b"
}
```
Event 1 writes this. Events 2–4 read it via `read_session_context()` to link their log entries to the triggering prompt.

### Tests Added

All tests live in `tests/` and run with `pytest tests/ -v -s`. Total: **271 passed, 22 skipped** (skipped = Events 3 and 4 stubs).

**Event 1 tests** — `tests/test_suite_event1_prompt.py` — **115 tests**, 10 classes:

| Class | Tests | What it covers |
|---|---|---|
| `TestClassifyPrompt` | 8 | Three-strategy scoring, fallback, case-insensitivity, highest score wins |
| `TestIsComplexUnstructured` | 11 | Length boundary (49/50), structure markers, skill prefix suppression |
| `TestNudgeState` | 5 | Fresh session nudges, idempotent after fire, session isolation |
| `TestResetTurnState` | 5 | write/read count reset, delegated flag removal |
| `TestBuildContext` | 14 | Routing section, agent name, confidence, delegation threshold, patterns, nudge firing logic |
| `TestFullPipeline` | 6 | stdin → stdout JSON round-trip, systemMessage shape, routing and delegation in output |
| `TestSessionIdentity` | 7 | `_init_session` flag creation, `current.json` written, idempotency, multi-session isolation |
| `TestCorrelationId` | 5 | 12-char hex format, uniqueness, header injection, absent when empty, logged by main |
| `TestPatternRelevance` | 10 | Domain scoring (1.0/0.6/0.3), keyword boost, ≥0.7 filter, ranking, cap at 5, empty input |
| `TestComplexityEstimator` | 8 | Length gate, complex verb + connective, two verbs, no verbs, single verb edge cases |
| `TestAgentPersona` | 6 | Description, instructions, recommended skill in output; no config graceful |
| `TestHtmlCommentHeader` | 8 | agent=, confidence=, patterns=, delegation=advisory/required, correlation=, header before body |
| `TestDelegationRequired` | 7 | MUST keyword, advisory framing, threshold reference, main wires complexity to delegation |
| `TestTypedEventSchema` | 10 | All required fields present and typed correctly, snippet truncation |
| `TestSessionCorrelationUpdate` | 6 | Writes to `current.json`, creates if missing, overwrites, preserves `started_at`, main wires it |

**Event 2 tests** — `tests/test_suite_event2_shell.py` — **36 tests**, 5 classes:

| Class | Tests | What it covers |
|---|---|---|
| `TestHardBlock` | 9 | All 9 HARD_BLOCK patterns deny, userMessage present, priority over SOFT_WARN |
| `TestSoftWarn` | 8 | All 8 representative SOFT_WARN patterns allow with agentMessage |
| `TestSafeAndMisc` | 3 | Safe commands allow without agentMessage, empty command allows, event logged |
| `TestCorrelationThreading` | 6 | ID read from session context, missing context uses empty string, ID present on all decision types |
| `TestTypedEventSchema` | 10 | All fields present and typed, command truncation, all three decision values logged correctly |
