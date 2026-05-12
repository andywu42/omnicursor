# OmniCursor Demo Runbook

Two-act demo. Total time: ~15 minutes.

- **Act 1** — Ticket-to-code pipeline: type a task description, OmniCursor creates
  a Linear ticket, implements the code autonomously, and opens a PR.
- **Act 2** — Option C observability: the session from Act 1 appears as a live event
  stream in the terminal, sourced from the Unix socket sidecar.

Commands below use `$OMNICURSOR_ROOT` for the OmniCursor repo and `$OMNIDASH_ROOT`
for the OmniDash repo. Set these once before starting:

```bash
export OMNICURSOR_ROOT=<absolute path to OmniCursor repo>
export OMNIDASH_ROOT=<absolute path to OmniDash repo>
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

### 2. Linear MCP

Verify Linear MCP is configured in `~/.cursor/mcp.json`. It should contain a
`linear` entry. If not, follow `QUICKSTART.md`.

Quick check — open Cursor and run:
```
/plan-ticket test
```
If it calls `tracker.list_teams` without erroring, Linear MCP is live.

### 3. OmniDash dependencies

```bash
cd "$OMNIDASH_ROOT"
npm install
```

### 4. Sidecar directory

```bash
mkdir -p ~/.omnicursor
```

---

## Day-of setup (do this before the audience arrives)

Open **3 terminals** and leave them running.

### Terminal 1 — OmniCursor sidecar (Option C)

```bash
cd "$OMNICURSOR_ROOT"
source /home/andyw/cs490/omninode/OmniCursor/.venv/bin/activate
bash scripts/run_sidecar.sh --publisher noop
```

Expected output:
```
sidecar starting | publisher=noop outbox=~/.omnicursor/outbox.jsonl socket=~/.omnicursor/emit.sock interval=2.0s
socket listener bound to ~/.omnicursor/emit.sock
```

Leave it running. It polls every 2 seconds.

### Terminal 2 — Outbox watcher + preflight smoke test

Start the outbox watcher — leave it running for the whole demo:

```bash
cd "$OMNICURSOR_ROOT"
python3 scripts/watch_outbox.py
```

Then in a **separate shell** run the smoke test once to confirm the pipe is live:

```bash
cd "$OMNICURSOR_ROOT"
python3 scripts/smoke_test.py
```

Expected: `{"status": "queued", "event_id": "..."}` from the smoke test, and a color-coded `SESSION OUTCOME` block in Terminal 2 within 2 seconds. If it doesn't appear, check Terminal 1 for errors.

### Terminal 3 — Cursor (your working IDE)

Open Cursor pointed at the OmniCursor repo root. The repo already has hooks
and skills configured — no extra setup needed.

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

## Act 2 — Option C observability (~5 min)

### Step 1 — Point at the sidecar terminal (Terminal 1)

Switch to Terminal 1. Show the drain log lines that appeared while Act 1 ran:

```
drainer: noop.publish session.outcome
drainer: noop.publish utilization.scoring.requested
```

**Narrate:** "Every time a Cursor session ends, the stop hook emits a structured
event over a Unix socket to the sidecar. The sidecar drains it — in production
this goes straight to Kafka and into omniintelligence."

### Step 2 — Show the outbox watcher (Terminal 2)

Switch to Terminal 2. It has been running `watch_outbox.py` since setup and shows
the Act 1 session already formatted in color:

```
── SESSION OUTCOME  conv=437b7ae7…
  outcome  : SUCCESS
  agent    : documentation-architect  conf=0.73
  prompts  : 1   files edited: 9   patterns injected: 0

── SOCKET EVENT  utilization.scoring.requested  session=437b7ae7…
  patterns : auto-5f38e3a94eac
```

Point out the fields: agent matched, confidence score, files edited, which patterns
were injected.

**Narrate:** "Every session produces a structured record — agent used, outcome,
files changed, patterns injected. This is the same schema omniintelligence expects.
Connect Kafka and these flow directly into the intelligence pipeline."

### Step 3 — Show the architecture diagram (optional)

```
Cursor IDE
  └─ stop hook (stop.py)
       └─► ~/.omnicursor/emit.sock
             └─► sidecar (socket_listener)
                   └─► ~/.omnicursor/outbox.jsonl   (durable)
                         └─► drain_loop (2s tick)
                               └─► Kafka/Redpanda      (production)
                                     └─► omniintelligence
                                           └─► pattern injection
                                                 └─► next Cursor session
```

**Narrate:** "Option C puts OmniCursor on the same infrastructure as OmniClaude.
The gap closes at the event bus level — same topics, same schema, same pipeline."

---

## Troubleshooting

### Terminal 2 shows no events after a session ends

1. Check Terminal 1 — the sidecar should show drain log lines. If not, the stop hook didn't fire. Make sure Cursor was opened on the worktree directory.
2. Check the outbox directly:
   ```bash
   tail -5 ~/.omnicursor/outbox.jsonl
   ```
   If it's empty, the stop hook didn't write anything.

### Sidecar socket error on start

The sidecar cleans up stale sockets automatically. If it still fails:
```bash
rm -f ~/.omnicursor/emit.sock
cd "$OMNICURSOR_ROOT" && bash scripts/run_sidecar.sh --publisher noop
```

### Linear MCP not responding

Restart Cursor. MCP servers are started per IDE session. If still failing, check
`~/.cursor/mcp.json` has the `linear` entry and the API key is set.

### pytest fails during execute-plan

OmniCursor will attempt up to 2 self-correction cycles. If tests still fail it
marks the ticket blocked in Linear and reports what it tried. Show the Linear
comment as evidence of autonomous error reporting — it's still a good demo moment.

---

## Key env vars

| Variable | Where | Effect |
|---|---|---|
| `INTELLIGENCE_SERVICE_URL` | Cursor env | omniintelligence HTTP API for per-prompt pattern injection (default: `http://localhost:8053`) |
| `OMNICURSOR_CONTEXT_API_TIMEOUT_MS` | Cursor env | Timeout for API pattern fetch in ms (default: 900) |
| `OMNICURSOR_SIDECAR_INTERVAL` | Terminal 1 | Drain poll interval in seconds (default: 2) |
| `KAFKA_BOOTSTRAP_SERVERS` | Terminal 1 | Broker address when using `--publisher kafka` (requires Docker + Redpanda) |

---

## Quick reference — skill commands

| Command | What it does |
|---|---|
| `/plan-ticket <description>` | Generates YAML contract, creates Linear ticket |
| `/plan-to-tickets <plan-file>` | Creates one epic + one ticket per plan task |
| `/execute-plan <plan-file>` | Full pipeline: review → tickets → implement → PR |
| `/hostile-reviewer --pr <N> --repo <owner/repo>` | Adversarial multi-model PR review |
| `/recap` | Summarises the current session before handing off |
