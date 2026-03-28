# Rubric: Adapter Stub Rule (`20-adapter-stub.mdc`)

**Bucket:** 3 — External Integration (Stub)
**Grading mode:** Structural only — Pass/Fail on contract conformance and fail-soft behavior

---

## Purpose

This rubric tests that the adapter stub:
1. Correctly identifies the Bucket 3 operation and its external dependencies
2. Constructs a request payload conforming to the frozen adapter contract
3. Uses dry_run semantics correctly
4. Does NOT attempt live external calls
5. Applies fail-soft behavior when the service is unavailable

---

## Contract Conformance

The rule must output a dry-run request payload. Check it against `docs/ARCHITECTURE.md` → "Frozen Adapter Contract."

- [ ] **C1** — Request body is valid JSON (can be parsed)
- [ ] **C2** — `skill_name` field is present and is one of the known Bucket 3 skill names
- [ ] **C3** — `input` field is present and contains at least `dry_run: true`
- [ ] **C4** — `dry_run: true` is set at the TOP level of the request (not only inside `input`)
- [ ] **C5** — `context.repo` is present and is one of the 7 valid repo names
- [ ] **C6** — `context.cwd` is a relative path — NOT an absolute path starting with `/`
- [ ] **C7** — No extra top-level fields not present in the contract schema

---

## Dry-Run Protocol

- [ ] **DR1** — The rule outputs `dry_run: true` on its first (and only) call — never `dry_run: false` as the first call
- [ ] **DR2** — The rule does NOT attempt a second call with `dry_run: false` in a session where no live endpoint is available
- [ ] **DR3** — If the rule simulates a blocked/error response from dry_run, it outputs the fail-soft message and stops

---

## Fail-Soft Behavior

- [ ] **FS1** — When the service is unavailable (no endpoint reachable), the rule outputs a message starting with: `"Service unavailable. Complete manually:"`
- [ ] **FS2** — The "complete manually" description tells the user a concrete next step (not just "try again")
- [ ] **FS3** — The rule does NOT retry the request automatically
- [ ] **FS4** — The rule does NOT output a success message when the service is unavailable
- [ ] **FS5** — The rule does NOT loop (i.e., does not invoke itself or the endpoint again in the same session)

---

## No Live External Calls

- [ ] **NE1** — The rule does NOT call any Linear MCP function (e.g., `mcp__linear-server__get_issue`)
- [ ] **NE2** — The rule does NOT attempt to import or run Python validators
- [ ] **NE3** — The rule does NOT make HTTP requests to any URL
- [ ] **NE4** — The rule correctly identifies at least 2 external dependencies that WOULD be needed for the real operation

---

## Dependency Identification

- [ ] **DEP1** — Rule names Linear MCP as a required dependency
- [ ] **DEP2** — Rule names at least one additional dependency (Python validator, Kafka, or omnibase_core)
- [ ] **DEP3** — Rule provides a "Complete manually" alternative that does not require any of the Bucket 3 deps

---

## Scoring

| Category | Criteria | Met |
|----------|----------|-----|
| Contract conformance | 7 criteria | ___ / 7 |
| Dry-run protocol | 3 criteria | ___ / 3 |
| Fail-soft behavior | 5 criteria | ___ / 5 |
| No live calls | 4 criteria | ___ / 4 |
| Dependency ID | 3 criteria | ___ / 3 |

**Final:** PASS (all 22 criteria met) OR FAIL (any criterion not met)

---

## Grading Notes

- This rubric is **purely structural** — it does not test the quality of the sub-ticket decomposition (since the rule cannot access Linear).
- The dry_run payload is evaluated against the ARCHITECTURE.md contract schema, not against what Linear would actually accept.
- A rule that outputs "I cannot do this without Linear" without a payload fails C1–C7.
- A rule that outputs a payload but sets `dry_run: false` fails DR1.
- A rule that calls `mcp__linear-server__get_issue` (even in a thought/reasoning step that produces a response) fails NE1.
