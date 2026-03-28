# Test Prompt: Plan Ticket — Simple (Repo Explicit in Prompt)

**Rule under test:** `12-plan-ticket.mdc`
**Expected bucket:** 2 (Local-Data Hybrid)
**Difficulty:** Easy — repo name present in prompt

---

## Prompt

Paste this into Cursor Composer:

---

Create a ticket to add retry logic to the emit daemon in omniclaude. Currently, if the Kafka broker is unavailable, the daemon drops events immediately. We want it to retry up to 3 times with 1-second backoff before dropping.

---

## What to Observe

1. Does the rule announce what it reads before using file content?
2. Does repo detection follow Priority 1 (prompt contains "omniclaude")?
3. Is no clarifying question asked about the repo (Priority 1 should resolve it)?
4. Is the YAML template output correctly formatted with all required fields?
5. Is the `repo` field set to `omniclaude`?
6. Are requirements derived from the prompt (retry logic, 3 retries, 1-second backoff)?
7. Does the handoff line reference the `linear` rule?

## Expected Repo Detection Path

- Priority 1: prompt contains "omniclaude" → use `omniclaude`
- Priority 2 and 3: should NOT be reached

## Expected Output Shape

```yaml
title: "Add retry logic to emit daemon"
repo: "omniclaude"
requirements:
  - id: "R1"
    statement: "Emit daemon retries Kafka delivery up to 3 times before dropping"
    ...
  - id: "R2"
    statement: "Retry backoff is 1 second between attempts"
    ...
```

## Rubric File

See `tests/rubrics/plan-ticket.md` for the full pass/fail checklist.
