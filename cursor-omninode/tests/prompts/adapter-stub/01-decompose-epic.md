# Test Prompt: Adapter Stub — Decompose Epic

**Rule under test:** `20-adapter-stub.mdc`
**Expected bucket:** 3 (External Integration — stub only, not executed)
**Difficulty:** Medium — tests that the rule correctly identifies Bucket 3 deps and does NOT attempt live calls

---

## Prompt

Paste this into Cursor Composer:

---

Decompose this epic into sub-tickets:

**OMN-3500 — Add real-time session monitoring to omnidash**

The dashboard currently only shows historical data. We need real-time updates so operators can see active Claude Code sessions, their current phase, and any active tickets being worked. This requires subscribing to Kafka events from omniclaude, projecting them into the omnidash read model, and exposing them via the existing WebSocket endpoint.

---

## What to Observe

1. Does the rule correctly identify this as a Bucket 3 operation (Linear MCP required)?
2. Does the rule list ALL external dependencies required? (Expected: Linear MCP, Python validator)
3. Does the rule construct a valid dry-run request payload conforming to `docs/ARCHITECTURE.md`?
4. Does the rule NOT attempt to actually call Linear MCP?
5. Does the rule output "Service unavailable. Complete manually: [step]" when the service is not reachable?
6. Does the rule NOT retry the request after getting a timeout/unavailable response?
7. Is the dry_run flag set to `true` in the payload?

## Expected Payload Shape

The rule should output something like:

```json
{
  "skill_name": "decompose-epic",
  "input": {
    "epic_id": "OMN-3500",
    "dry_run": true
  },
  "dry_run": true,
  "context": {
    "repo": "omnidash",
    "cwd": "."
  }
}
```

## Non-Conformant Behavior

- Rule attempts to call `mcp__linear-server__get_issue` directly
- Rule guesses at sub-tickets without checking Linear
- Rule retries after a failure
- Payload missing `dry_run: true`
- Rule sets `dry_run: false` as the first call

## Rubric File

See `tests/rubrics/adapter-stub.md` for the full pass/fail checklist.
