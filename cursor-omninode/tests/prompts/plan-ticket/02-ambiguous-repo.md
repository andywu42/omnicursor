# Test Prompt: Plan Ticket — Ambiguous Repo (Triggers Question)

**Rule under test:** `12-plan-ticket.mdc`
**Expected bucket:** 2 (Local-Data Hybrid)
**Difficulty:** Medium — no repo name in prompt or README → triggers Priority 3 question

---

## Setup

Before running this prompt, ensure:
- The project opened in Cursor is `cursor-omninode/` (this starter pack)
- The README.md does not contain any of the 7 valid repo names as a project name
- (This starter pack's README says "cursor-omninode" which is not a valid repo name)

---

## Prompt

Paste this into Cursor Composer:

---

Create a ticket to add caching for frequently-accessed configuration values to reduce database load.

---

## What to Observe

1. Does the rule announce what it reads before using file content?
2. Does repo detection correctly fail Priority 1 (no repo name in "add caching for frequently-accessed configuration values")?
3. Does repo detection correctly fail Priority 2 (README doesn't name a valid repo)?
4. Does the rule ask exactly ONE multiple-choice question with all 7 options + "other"?
5. After the user answers (e.g., "B — omnibase_core"), is the template generated with the correct repo?
6. Is only ONE question asked — not follow-up questions about the caching mechanism before generating the template?

## Expected Question Format

```
Which repository does this ticket belong to?

A) omniclaude
B) omnibase_core
C) omnibase_infra
D) omnidash
E) omniintelligence
F) omnimemory
G) omninode_infra
H) Other (describe below)
```

## Non-Conformant Behavior

- Guessing a repo without asking (e.g., assuming omnibase_core because "configuration" sounds like infra)
- Asking "Which repo?" as a free-text question without providing the 7 options
- Asking additional questions after the repo is confirmed (e.g., "What cache backend? Redis or in-memory?")
- Skipping Priority 1/2 checks and going straight to asking

## Rubric File

See `tests/rubrics/plan-ticket.md` for the full pass/fail checklist.
