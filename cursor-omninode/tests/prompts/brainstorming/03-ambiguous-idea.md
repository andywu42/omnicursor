# Test Prompt: Brainstorming — Ambiguous Idea (Stress Test)

**Rule under test:** `10-brainstorming.mdc`
**Expected bucket:** 1 (Pure Methodology)
**Difficulty:** Hard — vague prompt with no scope, repo, or success criteria

---

## Prompt

Paste this into Cursor Composer:

---

make the agent smarter

---

## What to Observe

This is the hardest brainstorming test. The prompt is intentionally:
- Too vague to act on ("smarter" is not measurable)
- Missing repo context (which repo? omniclaude? omniintelligence?)
- Missing success criteria (smarter how? faster? more accurate? more context-aware?)

### Conformant behavior:

1. Rule does NOT immediately propose a design or list approaches
2. Rule asks ONE clarifying question (multiple-choice preferred) to narrow scope
3. Rule continues asking one question at a time until the scope is clear
4. Only after scope is clear does the rule propose 2–3 approaches
5. YAGNI is applied — "smarter" is scoped to one concrete, measurable improvement

### Non-conformant behavior:

- Responding with a list of 5 ways to make the agent smarter (no questions asked)
- Asking "What do you mean by smarter, which agent, which repo, and what's your timeline?" (multiple questions)
- Assuming the answer is "add more context injection" without asking
- Proposing a design immediately from a vague prompt

## Grading Note

This prompt is primarily a stress test for the one-question-per-message invariant. A rule that
asks multiple questions on vague prompts fails this test even if it eventually produces a good design.

## Rubric File

See `tests/rubrics/brainstorming.md` for the full pass/fail checklist.
