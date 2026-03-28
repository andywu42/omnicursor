# Test Prompt: Writing Plans — New Node

**Rule under test:** `11-writing-plans.mdc`
**Expected bucket:** 1 (Pure Methodology)
**Difficulty:** Straightforward — clear design doc provided

---

## Prompt

Paste this into Cursor Composer, including the design doc content below:

---

Here's the design doc for a new webhook delivery node. Please write the implementation plan.

```markdown
# Webhook Delivery Node — Design

**Goal:** Add a WebhookDeliveryNode to omniclaude that POSTs session summaries to a user-configured URL when a Claude Code session ends.

## Architecture

The node listens on the `onex.evt.omniclaude.session-ended.v1` Kafka topic. When it receives a session-ended event, it retrieves the session summary from the database and POSTs it as JSON to the URL configured in the node's contract.

## Components

- **WebhookDeliveryNode** — ONEX node with handler
- **WebhookDeliveryHandler** — calls the configured URL with the payload
- **WebhookDeliveryContract** — declares required config (webhook_url, timeout_ms, retry_count)

## Data Flow

1. Session ends → `session-ended.v1` event emitted
2. WebhookDeliveryNode receives event
3. Handler fetches session summary from Postgres
4. Handler POSTs `{"session_id": "...", "summary": "...", "ended_at": "..."}` to webhook_url
5. On HTTP 2xx: emit `webhook-delivered.v1`
6. On error after retry_count exhausted: emit `webhook-failed.v1`

## Error Handling

- Retry up to `retry_count` times with exponential backoff
- On final failure: emit `webhook-failed.v1` with error details
- Never block the session-ended event processing

## Testing Strategy

- Unit test handler with mocked HTTP client
- Unit test retry logic with mocked failure scenarios
- Contract test: verify `webhook_url` config key declared
```

---

## What to Observe

1. Does the rule announce "I'm using the writing-plans rule..." at the start?
2. Does the plan start with the required header (Goal, Architecture, Tech Stack)?
3. Are tasks bite-sized (2–5 minutes each)?
4. Does the rule run the adversarial review pass before presenting the plan?
5. Is R1 (count integrity) explicitly checked?
6. Is R2 (acceptance criteria strength) explicitly checked?
7. Does the plan save to `docs/plans/YYYY-MM-DD-webhook-delivery-node.md`?
8. Does the handoff line reference the saved file path?

## Rubric File

See `tests/rubrics/writing-plans.md` for the full pass/fail checklist.
