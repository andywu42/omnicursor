# Rubric: Writing Plans Rule (`11-writing-plans.mdc`)

**Bucket:** 1 — Pure Methodology
**Grading mode:** Tier 1 is Pass/Fail. Tier 2 (R3–R6) is advisory — failures are noted but do not cause a FAIL.

---

## Tier 1 — Required (Pass/Fail)

### R1 — Count Integrity

- [ ] **R1a** — Rule performs an adversarial review pass and explicitly announces: "Draft staged. Running adversarial review..."
- [ ] **R1b** — R1 is explicitly acknowledged in the review output (even if clean)
- [ ] **R1c** — If the design doc contains numeric claims about task/phase counts, the rule recomputes from the actual list structure. A plan with 4 phases (including splits) that says "3 phases" in the header must be corrected.
- [ ] **R1d** — The review output states "R1: checked — [clean / issue found and fixed]". A rule that claims R1 is clean without providing evidence (e.g., "counted N tasks; all claims match") fails this criterion.

**Test with:** `tests/prompts/writing-plans/02-multi-phase.md` (explicit count mismatch)

### R2 — Acceptance Criteria Strength

- [ ] **R2a** — R2 is explicitly acknowledged in the review output
- [ ] **R2b** — At least one acceptance criterion in the plan is testable and specific (names exact conditions, not "tests pass")
- [ ] **R2c** — If any criterion contains "tests pass" as the sole verification, R2 must flag it and replace with a specific assertion
- [ ] **R2d** — No criterion contains subjective language ("clean", "robust", "nice") without a paired measurable check

**Test with:** `tests/prompts/writing-plans/01-new-node.md` (verify R2 catches weak criteria)

---

## Tier 2 — Advisory (Bonus)

Failures below are noted in the review but do not cause a FAIL. Students who catch these earn bonus credit.

### R3 — Scope Violations (Bonus)
- [ ] Rule identifies at least one case where a task's acceptance criteria exceed its stated scope
- [ ] Mismatched criteria are moved to the task with the correct scope, not deleted

### R4 — Integration Traps (Bonus)
- [ ] Rule verifies at least one import path or module reference against the codebase
- [ ] Unverified paths are flagged with "Mirror import from `<file>`" instruction

### R5 — Idempotency (Bonus)
- [ ] For any task that creates a file, table, or resource: dedup key is stated
- [ ] Script reruns are handled (IF NOT EXISTS, upsert, file existence check)

### R6 — Verification Soundness (Bonus)
- [ ] Each verification step is graded: strong / medium / weak
- [ ] No weak proof is the sole evidence for a core invariant

---

## Structural Checks (independent of adversarial review)

- [ ] Plan starts with the required header (Goal, Architecture, Tech Stack)
- [ ] Tasks are bite-sized: each step described as one 2–5 minute action
- [ ] File paths are exact — no "somewhere in src/"
- [ ] Code examples are complete — no "add validation here" placeholders
- [ ] Commands are exact with expected output
- [ ] Plan saved to `docs/plans/YYYY-MM-DD-<feature>.md`
- [ ] Handoff line references the actual saved file path

---

## Scoring

| Category | Criteria | Met |
|----------|----------|-----|
| Tier 1 R1 | 4 criteria | ___ / 4 |
| Tier 1 R2 | 4 criteria | ___ / 4 |
| Tier 2 (bonus) | 4 categories | ___ / 4 |
| Structural | 7 checks | ___ / 7 |

**Final:** PASS (all Tier 1 criteria met) OR FAIL (any Tier 1 criterion not met)
Tier 2 failures are advisory only.
