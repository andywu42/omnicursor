# OmniCursor — Current State

This document describes what the repo contains, what works, and what is in progress as of May 2026.

---

## What OmniCursor is

OmniCursor is a Cursor IDE plugin that brings OmniNode-style intelligence to Cursor sessions. It does three things:

1. **Routes every prompt** to the best-fit agent using a three-strategy scoring engine
2. **Injects learned patterns** into each prompt's system message so the model benefits from past session outcomes
3. **Emits structured events** to the OmniNode event bus so session data feeds back into the intelligence pipeline

It is built entirely on Cursor's hook system — four Python scripts that fire at lifecycle events. The hooks use stdlib only (no pip dependencies) so they are fast and portable.

---

## Repo structure

```
OmniCursor/
├── .cursor/
│   ├── hooks.json          — registers the 4 hook entry points
│   ├── hooks/scripts/      — the 4 hook scripts
│   ├── hooks/lib/          — shared hook libraries
│   ├── agents/             — 18 agent JSON configs
│   ├── rules/              — 13 Cursor rules (.mdc)
│   └── skills/             — 16 skill directories (mirrored from skills/)
├── skills/                 — 16 skill markdown definitions
├── src/omnicursor/         — Python library (tests, CI, automation)
├── tests/                  — 24 test files, 691 tests
├── eval/                   — routing evaluation scripts + labeled data
├── docs/                   — documentation
├── compose.yaml            — local Docker stack (Redpanda, Postgres, intelligence services)
└── scripts/                — utility scripts
```

---

## The 4 hooks

| Hook | Fires when | What it does |
|---|---|---|
| `user-prompt-submit.py` | User submits a prompt | Classifies prompt → selects agent → injects patterns + agent persona into system message |
| `shell-guard.py` | Before a shell command runs | Blocks 9 dangerous patterns, warns on 11 risky ones |
| `post-edit.py` | After a file is edited | Runs `ruff check` and `tsc --noEmit` diagnostically (never modifies files) |
| `stop.py` | Session ends | Classifies outcome (success/failed/abandoned/unknown), writes outbox record, emits events to sidecar socket |

---

## Agent routing

Every prompt is scored against 18 agents using three strategies in order:

1. **Exact match** on explicit trigger phrases → 0.95 confidence
2. **Fuzzy match** via SequenceMatcher → 0.70–0.80 confidence
3. **Keyword overlap** on activation keywords → 0.55–0.85 confidence

`HARD_FLOOR = 0.55` — anything below this falls back to `polymorphic-agent`. The scoring logic is shared between the hook (`user-prompt-submit.py`) and the Python library (`src/omnicursor/scoring.py`) — single source of truth.

---

## The 16 skills

Skills are Markdown files that teach Claude how to run a structured workflow. They activate when the user types `/skill-name` in Cursor.

| Skill | What it does |
|---|---|
| `systematic-debugging` | Structured root-cause debugging |
| `brainstorming` | Structured ideation |
| `writing-plans` | Write implementation plans |
| `plan-ticket` | Generate YAML contract + create Linear ticket |
| `plan-to-tickets` | Batch ticket creation from a plan file |
| `execute-plan` | Full pipeline: plan review → tickets → implement → PR |
| `pr-review` | Structured pull request review |
| `pr-polish` | Final PR cleanup before merge |
| `hostile-reviewer` | Multi-model adversarial review (v4.0, with gate mode) |
| `defense-in-depth` | Security review methodology |
| `merge-planner` | Plan a complex merge |
| `insights-to-plan` | Convert observations into an implementation plan |
| `handoff` | Structure a session handoff |
| `using-git-worktrees` | Worktree-based parallel development |
| `recap` | Summarise the current session |
| `plan-review` | Adversarially review a plan before execution |

---

## Pattern learning (Option A)

When a session ends successfully and patterns were injected, `stop.py` writes back to `~/.omnicursor/learned_patterns.json` — updating injection counts and utilization scores. Patterns that perform well get higher weights; patterns that decay below threshold are evicted.

On the next session, `user-prompt-submit.py` loads these patterns and injects the most relevant ones (filtered by domain and keyword overlap) into the prompt's system message.

**What works:** full local learning loop — inject → outcome → write-back → re-inject next session.

---

## Pattern sync (Option B)

`lib/pattern_sync.py` in the hooks calls `GET /api/v1/patterns` on the omniintelligence HTTP API at session start to pull remotely-learned patterns. Local patterns always take priority — remote patterns are appended only if not already present locally (merge-local-priority).

`user-prompt-submit.py` also calls the API at every prompt submission (900ms timeout, falls back to local cache if unavailable).

**What works:** HTTP read sync runs when `OMNICURSOR_PATTERN_SYNC_HTTP=1` is set. Per-prompt API injection runs automatically if `INTELLIGENCE_SERVICE_URL` resolves (default `localhost:8053`).

---

## Event pipeline (Option C)

Option C adds a sidecar daemon that connects OmniCursor to the OmniNode event bus.

### How it works

```
Cursor session ends
  └─► stop.py
        ├─► ~/.omnicursor/outbox.jsonl    (durable record)
        └─► ~/.omnicursor/emit.sock       (live signal)
              └─► sidecar drain_loop (2s tick)
                    └─► Kafka/Redpanda → omniintelligence
```

### Components

| Component | File | Status |
|---|---|---|
| Outbox writer | `src/omnicursor/session_outbox.py` | Working |
| Socket listener | `src/omnicursor/sidecar/socket_listener.py` | Working |
| Drain loop | `src/omnicursor/drainer/loop.py` | Working |
| Kafka publisher | `src/omnicursor/drainer/kafka_publisher.py` | Working (requires confluent-kafka + Redpanda) |
| Noop publisher | `src/omnicursor/drainer/publisher.py` | Working (for testing) |
| Daemon CLI | `src/omnicursor/sidecar/daemon.py` | Working |
| Launcher | `scripts/run_sidecar.sh` | Working |
| Outbox watcher | `scripts/watch_outbox.py` | Working (colorized terminal monitor) |
| Smoke test | `scripts/smoke_test.py` | Working |

### Running the sidecar

```bash
bash scripts/run_sidecar.sh --publisher noop     # testing
bash scripts/run_sidecar.sh --publisher kafka    # production (needs Redpanda)
```

**What works:** full socket → outbox → drain → publish pipeline. Tested end-to-end with Cursor sessions. Kafka publisher works when Redpanda is running via `docker compose up redpanda -d`.

---

## Infrastructure (Docker Compose)

`compose.yaml` defines the full local OmniNode stack:

| Service | Port | What it is |
|---|---|---|
| `postgres` | 5436 | Database for intelligence services |
| `redpanda` | 19092 | Kafka-compatible message broker |
| `valkey` | 16379 | Redis-compatible cache |
| `intelligence-reducer` | 18091 | omniintelligence reducer (pattern storage + scoring) |
| `intelligence-orchestrator` | 18092 | omniintelligence orchestrator |
| `quality-scoring-compute` | 18093 | Quality scoring node |

Start the full stack: `docker compose up -d`  
Start just Redpanda: `docker compose up redpanda -d`

---

## MCP integrations

| Server | Config location | What it does |
|---|---|---|
| `linear` | `~/.cursor/mcp.json` | Linear ticket operations (`tracker.*` tools) |
| `omnicursor-omnimarket` | `.cursor/mcp.json` (gitignored, set locally) | Omnimarket node bridge |

`.cursor/mcp.json` is gitignored — each developer sets their own local paths.

---

## Test suite

```bash
source .venv/bin/activate
pytest tests/ -q          # 691 tests
ruff check src/ tests/ .cursor/hooks/   # lint
```

All 691 tests pass on `main` and `intelligence/option-c`. The pre-commit hook runs both automatically.

---

## Branches

| Branch | What it contains |
|---|---|
| `main` | Stable base — hooks, routing, pattern learning (Option A), pattern sync (Option B) |
| `intelligence/option-b` | Option B work — same as main, PR open |
| `intelligence/option-c` | Everything in main + Option C sidecar daemon + Kafka publisher + demo scripts. PR open against main. |

---

## What is NOT yet in main

Everything in `intelligence/option-c` that isn't in `main` yet:

- `src/omnicursor/drainer/` — full drainer module
- `src/omnicursor/sidecar/` — socket listener + daemon
- `src/omnicursor/session_outbox.py` — outbox writer
- `scripts/run_sidecar.sh`, `scripts/smoke_test.py`, `scripts/watch_outbox.py`
- `config/event_registry/omnicursor.yaml` — topic registry
- Per-prompt omniintelligence API injection in `user-prompt-submit.py`
- `tests/test_sidecar.py` — 16 sidecar tests

These land in main once the `intelligence/option-c` PR is merged.
