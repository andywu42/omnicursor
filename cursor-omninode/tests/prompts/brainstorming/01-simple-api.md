# Test Prompt: Brainstorming — Simple API Feature

**Rule under test:** `10-brainstorming.mdc`
**Expected bucket:** 1 (Pure Methodology)
**Difficulty:** Straightforward — clear scope, single repo

---

## Prompt

Paste this into Cursor Composer after opening `cursor-omninode/` as your project folder:

---

I want to add a webhook endpoint to omniclaude. When a Claude Code session ends, the endpoint should POST a JSON payload to a user-configured URL with the session summary.

---

## What to Observe

1. Does the rule announce what it reads before using file content?
2. Does the first response contain exactly ONE question?
3. Does the rule eventually propose at least 2 approaches with named trade-offs?
4. Is the design presented in sections of ~200–300 words with a check-in after each?
5. Does the session end with a handoff line referencing `docs/plans/YYYY-MM-DD-*-design.md`?
6. Does that file actually get written?

## Rubric File

See `tests/rubrics/brainstorming.md` for the full pass/fail checklist.
