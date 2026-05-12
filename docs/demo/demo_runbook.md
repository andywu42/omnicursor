# OmniCursor Demo Runbook — Options B+C (Full Intelligence Stack)

Two-act demo. Total time: ~15 minutes.

- **Act 1** — Ticket-to-code pipeline: type a task description, OmniCursor creates
  a Linear ticket, implements the code autonomously, and opens a PR.
- **Act 2** — B+C observability: the session from Act 1 appears as a live event
  stream, events flow into omniintelligence via Kafka, and updated patterns are
  injected at the next prompt — closing the learning loop end-to-end.

Set this once before starting:

```bash
export OMNICURSOR_ROOT=<absolute path to OmniCursor repo>
```

---

## Prerequisites

These only need to be done once.

### 1. Python venv

```bash
cd "$OMNICURSOR_ROOT"
python3.12 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Docker

Verify Docker is running:

```bash
docker info >/dev/null 2>&1 && echo "Docker OK"
```

The first `docker compose up` builds the omniintelligence images from source — allow
**5–10 minutes** on first run. Subsequent starts are instant (images cached).

### 3. Linear MCP

Verify Linear MCP is configured in `~/.cursor/mcp.json` with a `linear` entry.

Quick check — open Cursor and run `/plan-ticket test`. If it calls `tracker.list_teams`
without erroring, Linear MCP is live.

### 4. Sidecar directory

```bash
mkdir -p ~/.omnicursor
```

---

## Day-of setup (do this before the audience arrives)

Open **3 terminals** and leave them running.

### Terminal 1 — Full B+C stack (compose + sidecar)

```bash
cd "$OMNICURSOR_ROOT"
source .venv/bin/activate
bash scripts/run_bc_stack.sh
```

This starts Redpanda, Postgres, Valkey, and the omniintelligence services, waits for
the reducer to be healthy, then launches the sidecar connected to Kafka.

Expected output (after services are healthy):

```
Starting compose stack...
intelligence-reducer is healthy.

Starting OmniCursor sidecar (publisher=kafka)...
  INTELLIGENCE_SERVICE_URL=http://localhost:18091
  OMNICURSOR_PATTERN_SYNC_HTTP=1

sidecar starting | publisher=kafka outbox=~/.omnicursor/outbox.jsonl socket=~/.omnicursor/emit.sock interval=2.0s
socket listener bound to ~/.omnicursor/emit.sock
```

Leave it running. It polls every 2 seconds.

### Terminal 2 — Outbox watcher + preflight smoke test

Start the outbox watcher — leave it running for the whole demo:

```bash
cd "$OMNICURSOR_ROOT"
python3 scripts/watch_outbox.py
```

Then in a **separate shell** run the smoke test to confirm the full pipe is live:

```bash
cd "$OMNICURSOR_ROOT"
python3 scripts/smoke_test.py
```

Expected: `{"status": "queued", "event_id": "..."}` from the smoke test, and a
color-coded `SESSION OUTCOME` block in Terminal 2 within 2 seconds.

### Terminal 3 — Cursor (your working IDE)

Open Cursor pointed at `$OMNICURSOR_ROOT`. The hooks and skills are already configured.

---

## Act 1 — Ticket-to-code pipeline (~8 min)

### Step 1 — Create a ticket from a task description

In Cursor's composer, type:

```
Add a prompt_length field to the session outbox schema so we can track
how long each prompt was. /plan-ticket
```

OmniCursor will automatically:
1. Read the codebase to understand `session_outbox.py`
2. Generate a YAML ticket contract
3. Call `tracker.create_issue` → creates a Linear ticket (e.g. `OMN-XX`)
4. Report the ticket URL

**Narrate:** "OmniCursor read the repo, determined what the task requires,
and registered it in Linear — no manual ticket writing."

### Step 2 — Execute the ticket autonomously

Still in Cursor's composer, type:

```
/execute-plan — implement OMN-XX
```

(Replace `OMN-XX` with the ticket ID from Step 1.)

OmniCursor drives the full pipeline unattended:
1. Reads the Linear ticket via MCP
2. Identifies files to change (`session_outbox.py`, relevant tests)
3. Implements the change
4. Runs `pytest tests/ -q`
5. Opens a PR via `gh pr create`
6. Updates the Linear ticket to Done

**Step away from the keyboard after typing the command.** This is the key
moment — the audience should see the pipeline running with no human input.

**Narrate while it runs:** "One command. OmniCursor reads the ticket contract,
writes the code, runs the test suite, opens the PR, and closes the ticket —
fully unattended."

### Step 3 — Show the result

When the pipeline finishes, show:
- The PR URL in the Cursor output
- The Linear ticket status: Done
- The diff: `src/omnicursor/session_outbox.py` has the new field

**Narrate:** "From a one-line description to a merged-ready PR. The ticket is
the contract; the implementation follows the contract."

---

## Act 2 — B+C: the learning loop (~5 min)

### Step 1 — Show the outbox watcher (Terminal 2)

Switch to Terminal 2. It shows the Act 1 session formatted in color:

```
── SESSION OUTCOME  conv=437b7ae7…
  outcome  : SUCCESS
  agent    : documentation-architect  conf=0.73
  prompts  : 1   files edited: 9   patterns injected: 0
  reason   : files edited + completion marker

── SOCKET EVENT  utilization.scoring.requested  session=437b7ae7…
  patterns : auto-5f38e3a94eac
```

Point out: agent matched, confidence score, files edited, which patterns were injected.

**Narrate:** "Every session produces a structured record. That record just flowed
over a Unix socket into the sidecar, which published it to Kafka."

### Step 2 — Show the sidecar terminal (Terminal 1)

Switch to Terminal 1. Show the drain log lines:

```
drainer: kafka.publish session.outcome → onex.evt.omnicursor.session-outcome.v1
drainer: kafka.publish utilization.scoring.requested → onex.cmd.omniintelligence.utilization-scoring.v1
```

**Narrate:** "These events landed in Redpanda. omniintelligence is consuming them
right now — updating pattern weights in Postgres based on what worked in that session."

### Step 3 — Show the loop closing

Submit another prompt in Cursor (anything in the same domain). Then show Terminal 1:

```
drainer: pattern sync — pulled 3 updated patterns from http://localhost:18091
```

**Narrate:** "On the next prompt, OmniCursor fetched the updated patterns from
omniintelligence and injected them into the system message. The model is now
working with context shaped by the previous session's outcome."

### Step 4 — Show the architecture (optional)

```
Cursor IDE
  └─ user-prompt-submit.py
       └─► GET /api/v1/patterns ←─────────────────────────┐
  └─ stop.py                                               │
       └─► emit.sock → sidecar → Kafka (Redpanda)          │
                                    └─► omniintelligence   │
                                          └─► pattern weights updated
                                                └──────────┘
```

**Narrate:** "Option B is the read path — patterns fetched from omniintelligence
on every prompt. Option C is the write path — session outcomes published to Kafka.
Together they close the loop: every session makes the next one smarter."

---

## Stopping the stack

```bash
bash scripts/run_bc_stack.sh --down
```

---

## Troubleshooting

### Terminal 2 shows no events after a session ends

1. Check Terminal 1 — sidecar should show drain log lines. If not, the stop hook didn't fire. Make sure Cursor is opened on `$OMNICURSOR_ROOT`.
2. Check the outbox directly:
   ```bash
   tail -5 ~/.omnicursor/outbox.jsonl
   ```
   If empty, the stop hook didn't write anything.

### Sidecar socket error on start

The sidecar cleans up stale sockets automatically. If it still fails:
```bash
rm -f ~/.omnicursor/emit.sock
cd "$OMNICURSOR_ROOT" && bash scripts/run_bc_stack.sh
```

### intelligence-reducer not healthy

```bash
docker compose logs intelligence-reducer --tail=30
```

First-time build takes 5–10 minutes. If it fails after building, check Postgres is healthy:
```bash
docker compose ps
```

### Pattern sync not showing in Terminal 1

Confirm `OMNICURSOR_PATTERN_SYNC_HTTP=1` is set — `run_bc_stack.sh` sets it automatically.
Check the reducer is reachable:
```bash
curl http://localhost:18091/health
```

### Linear MCP not responding

Restart Cursor. MCP servers start per IDE session. If still failing, check
`~/.cursor/mcp.json` has the `linear` entry and the API key is valid.

### pytest fails during execute-plan

OmniCursor will attempt up to 2 self-correction cycles. If tests still fail it
marks the ticket blocked in Linear and reports what it tried. Show the Linear
comment as a demo moment — autonomous error reporting, no human intervention.

---

## Key env vars

| Variable | Set by | Effect |
|---|---|---|
| `INTELLIGENCE_SERVICE_URL` | `run_bc_stack.sh` | omniintelligence reducer URL for per-prompt pattern fetch (default: `http://localhost:18091`) |
| `OMNICURSOR_PATTERN_SYNC_HTTP` | `run_bc_stack.sh` | Set to `1` to enable session-end pattern sync pull |
| `KAFKA_BOOTSTRAP_SERVERS` | `run_bc_stack.sh` | Redpanda broker address (`localhost:19092`) |
| `OMNICURSOR_CONTEXT_API_TIMEOUT_MS` | Cursor env | Timeout for per-prompt API fetch in ms (default: 900) |
| `OMNICURSOR_SIDECAR_INTERVAL` | Terminal 1 | Drain poll interval in seconds (default: 2) |

---

## Quick reference — skill commands

| Command | What it does |
|---|---|
| `/plan-ticket <description>` | Generates YAML contract, creates Linear ticket |
| `/plan-to-tickets <plan-file>` | Creates one epic + one ticket per plan task |
| `/execute-plan <plan-file>` | Full pipeline: review → tickets → implement → PR |
| `/hostile-reviewer --pr <N> --repo <owner/repo>` | Adversarial multi-model PR review |
| `/recap` | Summarises the current session before handing off |
