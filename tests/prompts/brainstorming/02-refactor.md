# Test Prompt: Brainstorming — Refactor

**Rule under test:** `10-brainstorming.mdc`
**Expected bucket:** 1 (Pure Methodology)
**Difficulty:** Medium — refactor prompts tend to produce over-engineered designs

---

## Prompt

Paste this into Cursor Composer:

---

I want to refactor the hook system in omniclaude to be more testable. Right now the hooks are hard to test in isolation because they do too many things at once. I'd like to separate concerns so I can test each part independently.

---

## What to Observe

1. Does the rule ask ONE question first (not propose a full refactor immediately)?
2. Does the rule apply YAGNI — resist the urge to redesign everything at once?
3. Are at least 2 refactor strategies proposed with trade-offs before settling?
4. Does the rule present the design incrementally (200–300 word sections) with check-ins?
5. Is the design scoped to what was asked — not a full architectural overhaul?
6. Does the session end with a handoff line and a written design file?

## Stress Test

This prompt is designed to tempt the rule into over-engineering. A non-conformant rule might:
- Propose a complete new architecture in the first response
- Ask multiple questions at once ("What do you want to test? What's your current test setup? Are you using pytest?")
- Write a 1000-word design without breaking it into sections

A conformant rule asks one question first, then narrows scope, then presents a minimal design.

## Rubric File

See `tests/rubrics/brainstorming.md` for the full pass/fail checklist.
