# Cursor rules (`.mdc`)

OmniCursor **behavior surface** for the model. Rules `00` and `01` are **always on**; others activate on keywords or explicit `@mention`.

| File | Role |
|------|------|
| [`00-omninode-concepts.mdc`](./00-omninode-concepts.mdc) | ONEX vocabulary, buckets 1–3, pipeline stages. |
| [`01-codebase-research.mdc`](./01-codebase-research.mdc) | Bounded file-reading policy for agents. |
| [`10-brainstorming.mdc`](./10-brainstorming.mdc) | Bucket 1 — idea → design doc. |
| [`10-systematic-debugging.mdc`](./10-systematic-debugging.mdc) | Debugging methodology + MCP alignment. |
| [`11-writing-plans.mdc`](./11-writing-plans.mdc) | Bucket 1 — design → implementation plan. |
| [`12-plan-ticket.mdc`](./12-plan-ticket.mdc) | Bucket 2 — plan → YAML ticket template. |
| [`20-adapter-stub.mdc`](./20-adapter-stub.mdc) | Bucket 3 — adapter pattern, dry-run / fail-soft. |

**MCP:** Many rules assume OmniCursor server tools (`get_agent_context`, `invoke_skill`, `check_compliance`). See [docs/QUICKSTART.md](../../docs/QUICKSTART.md).

**Teaching / capstone:** [docs/STUDENT_GUIDE.md](../../docs/STUDENT_GUIDE.md), [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) (adapter contract).

**Tests:** Prompts under [`../../tests/prompts/`](../../tests/prompts/), rubrics under [`../../tests/rubrics/`](../../tests/rubrics/).
