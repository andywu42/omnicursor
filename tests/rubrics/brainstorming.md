# Rubric: Brainstorming Rule (`10-brainstorming.mdc`)

**Bucket:** 1 — Pure Methodology
**Grading mode:** Pass/Fail — any one FAIL trigger causes a FAIL for the session

---

## PASS Criteria (all 7 required)

- [ ] **P1 — Rule activates** within the first response (auto-activation via description keywords OR student uses `@10-brainstorming` mention). Either counts as activation.

- [ ] **P2 — Announces before reading** — the rule outputs a `Reading: ... | Listing: ...` line before using any file content in its response. If the rule uses file information without announcing, this fails.

- [ ] **P3 — One question per message** — every message that contains a question contains exactly ONE question. Count the `?` characters and verify each question mark corresponds to a separate message.

- [ ] **P4 — At least 2 approaches with named trade-offs** — before the design is presented, the rule presents 2 or 3 distinct approaches. Each approach must name at least one pro AND one con (not just a name).

- [ ] **P5 — Design in 200–300 word sections with check-in** — when the design is presented, it is broken into sections. Each section is between 150–350 words (±20% tolerance). After each section, the rule asks whether it looks right (this counts as the one allowed question for that message).

- [ ] **P6 — Handoff line is artifact-path-anchored** — the final message contains the literal handoff sentence with `docs/plans/YYYY-MM-DD-<topic>-design.md` as a specific, filled-in path. The path must include the actual date and actual topic slug.

- [ ] **P7 — Design file exists** — the file referenced in the handoff line actually exists at the stated path after the session.

---

## FAIL Triggers (any one causes FAIL)

- [ ] **F1 — Two or more questions in a single message.** Count question marks. If a message contains two or more questions, mark FAIL. (Check-in questions after design sections count — verify they are one per section.)

- [ ] **F2 — No approach comparison before settling.** If the rule presents a design without first showing 2–3 alternatives with trade-offs, mark FAIL. Exception: if the user explicitly says "just go with option X" after seeing options, the rule may skip further comparison.

- [ ] **F3 — "Paste above" or non-path handoff.** If the handoff line says "paste the above design", "use the content above", or any variant that does not reference a specific file path, mark FAIL.

- [ ] **F4 — Design file not written.** If the session ends and `docs/plans/YYYY-MM-DD-*-design.md` does not exist (or the path in the handoff line does not resolve to an existing file), mark FAIL.

---

## Scoring

| Result | Count |
|--------|-------|
| PASS criteria met | ___ / 7 |
| FAIL triggers hit | ___ / 4 |

**Final:** PASS (all 7 P criteria met AND 0 F triggers) OR FAIL (any condition above not met)

---

## Notes for Graders

- Trigger mode: auto-activation and @mention are equally valid. Do not penalize for requiring @mention.
- Word count: check 3 sections, not all. If 2+ sections are within range, P5 passes.
- Approach comparison: 2 approaches minimum. They don't need to be dramatically different — they must have named, distinct trade-offs.
- The design file date should be today's date (or the date of the session). A date that is ±1 day from session date is acceptable.
