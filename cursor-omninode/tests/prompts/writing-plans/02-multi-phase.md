# Test Prompt: Writing Plans — Multi-Phase (Count Integrity Stress Test)

**Rule under test:** `11-writing-plans.mdc`
**Expected bucket:** 1 (Pure Methodology)
**Difficulty:** Hard — designed to trigger R1 count integrity failures

---

## Prompt

Paste this into Cursor Composer:

---

Here's the design for adding rate limiting to the omniclaude API. Please write the implementation plan.

```markdown
# API Rate Limiting — Design

**Goal:** Add per-user rate limiting to omniclaude's webhook and API endpoints to prevent abuse.

## Architecture

Use a token bucket algorithm stored in Valkey (Redis-compatible). Each user gets a bucket refilled at `requests_per_minute` rate. Exceeded requests return HTTP 429.

## Components

- **RateLimitMiddleware** — FastAPI middleware that checks the bucket before passing to route handler
- **TokenBucketStore** — Valkey-backed implementation of the token bucket
- **RateLimitConfig** — Contract config keys: `requests_per_minute`, `burst_size`, `user_id_header`
- **RateLimitMetrics** — Emit `rate-limit-hit.v1` events to Kafka when limits are exceeded

## Data Flow

1. Request arrives → RateLimitMiddleware intercepts
2. Extract user_id from `user_id_header`
3. Check TokenBucketStore for remaining tokens
4. If tokens available: decrement and pass request through
5. If no tokens: return 429 with `Retry-After` header; emit `rate-limit-hit.v1`

## Error Handling

- Valkey unavailable → fail-open (allow request, log warning)
- Missing user_id_header → use IP address as fallback key
- Invalid config values → use safe defaults (60 req/min, burst 10)

## Testing Strategy

- Unit test token bucket logic (fill, drain, refill)
- Unit test middleware with mocked store
- Integration test with real Valkey
- Load test: 1000 req/s should correctly throttle to configured limit

## Phases

There are **3 main phases**: (1) Token bucket implementation, (2) Middleware integration, (3) Metrics and observability.

Phase 2 has two sub-phases: (2a) basic middleware, (2b) Kafka emission.
```

---

## What to Observe (R1 Focus)

The design doc says "3 main phases" but then describes 4 distinct deliverables (phase 2 splits into 2a and 2b). This is a deliberate R1 trap.

**R1 conformant behavior:**
- Rule counts actual phases/tasks in the plan it generates
- If plan has phases 1, 2a, 2b, 3 → that's 4 tasks, not 3
- Rule fixes the prose to say "4 phases" (or "3 phases with phase 2 split into 2a/2b")
- Adversarial review explicitly notes the count fix

**R1 non-conformant behavior:**
- Rule writes "This plan has 3 phases" in the header but lists 4 phase headings
- Rule ignores the count mismatch in the adversarial review
- Rule claims R1 is clean without counting

## Also Observe

- Does R2 check "fail-open" criterion against "unit tests pass" weakness?
- Does R3 catch the load-test step (scope: correctness test cannot verify throughput at the unit test level)?

## Rubric File

See `tests/rubrics/writing-plans.md` for the full pass/fail checklist.
