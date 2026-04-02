# OmniCursor — Definition of Done Rubric

> For CS 490 capstone evaluation. Tests whether the team understands
> the architectural concepts, not whether they match OmniNode's current codebase.

---

## How to use this

Each item has a **Claim** (what the team says they built) and a **Verification**
(how to prove it actually works). The verification must produce observable evidence —
not "we wrote a test" but "here is the output."

Grade on understanding, not on parity with omniclaude. The real system has 80+ skills,
20+ hooks, and a full Kafka event bus. That's not the bar. The bar is: do they understand
*why* those layers exist?

---

## 1. Layer Separation

**Concept being tested**: Rules, hooks, and tools serve different purposes. Rules shape
knowledge (always-on context). Hooks shape behavior (automatic lifecycle actions). Tools
provide capabilities (explicitly invoked). Mixing these layers creates fragile systems.

### Verification

- [ ] **Demo a prompt that hits all three layers in sequence.** Show the Cursor window.
  Type a prompt. Point to: (a) which rule injected background knowledge, (b) which hook
  fired automatically before the prompt reached the model, (c) which MCP tool the model
  called explicitly. If you can't trace all three, you don't have three layers — you have
  one layer wearing three hats.

- [ ] **Remove one layer and show what degrades.** Disable hooks (rename hooks.json).
  Run the same prompt. What changed? The model should still work (rules + MCP still
  function) but automatic routing and compliance should disappear. If nothing changes,
  the hooks weren't doing real work.

- [ ] **Explain why the hook can't replace the MCP tool (or vice versa).** Specific
  example: why does `get_agent_context` exist as an MCP tool when `on_prompt.py` already
  does routing? Answer should involve "manual override" or "the model needs to explicitly
  request a different agent mid-conversation." If the answer is "redundancy" — wrong.

---

## 2. Automatic Routing

**Concept being tested**: The system should route prompts to specialized agents without
the user or the model having to ask. This is the difference between "the LLM calls a tool
to figure out what to do" and "the infrastructure already decided before the LLM saw the
prompt."

### Verification

- [ ] **Run 5 prompts from different domains and show routing decisions.** Use prompts like:
  - "This function throws a NullPointerError on line 42"
  - "Write a plan for adding OAuth2 to our API"
  - "Review PR #38 for merge readiness"
  - "How should we structure the database schema?"
  - "Brainstorm ways to reduce API latency"

  For each: show which agent was selected, the confidence score, and the routing reason
  from `on_prompt.py` output. At least 4 of 5 should route to the correct specialized
  agent (not polymorphic-agent fallback).

- [ ] **Show a prompt that falls through to the fallback agent and explain why.**
  This proves you understand the floor threshold, not just the happy path. What does
  the system do when it doesn't know? Polymorphic-agent with score 0.0 is the right
  answer. Hallucinating a match is the wrong answer.

- [ ] **Show that routing happens before the model sees the prompt.** The `systemMessage`
  injection should be visible in Cursor's context or logs. If routing only happens when
  the model calls `get_agent_context`, that's Layer 3 (MCP), not Layer 2 (hooks) — and
  the whole architectural distinction collapses.

---

## 3. Compliance as Behavior, Not Policy

**Concept being tested**: Compliance checks should happen automatically, not because
someone remembered to call a tool. A compliance system that only works when the LLM
opts in is a suggestion, not a guardrail.

### Verification

- [ ] **Show the afterFileEdit hook catching a real lint violation.** Edit a Python file
  to introduce a real issue (unused import, missing type annotation, etc.). Save it.
  Show that ruff ran automatically and reported the violation without anyone asking.

- [ ] **Show the beforeShellExecution hook blocking a dangerous command.** Type a shell
  command like `rm -rf /` or `git push --force origin main`. Show that it was blocked
  or flagged before execution. If the hook only logs and doesn't actually prevent the
  action, say so — that's a valid design choice, but explain the trade-off.

- [ ] **Explain why auto-linting runs on afterFileEdit and not beforeSubmitPrompt.**
  Answer should involve "you lint the output, not the input" and "the prompt hasn't
  produced code yet when beforeSubmitPrompt fires." If the answer is "we just picked
  one" — that's a miss on understanding lifecycle ordering.

---

## 4. Pattern Persistence Across Sessions

**Concept being tested**: The system should learn from past sessions and surface that
learning in future sessions. This is the difference between a stateless tool and an
evolving assistant. Even with a JSON file, the concept matters more than the storage engine.

### Verification

- [ ] **Demonstrate the full lifecycle: create a pattern, end the session, start a new
  session, and show the pattern surfaced automatically.** This is the single most
  important demo for this concept. The pattern should appear in the `systemMessage`
  via `on_prompt.py`'s pattern injection — proving it crossed the session boundary.

- [ ] **Show the learned_patterns.json file with real content.** Open it. Point to a
  pattern that was created during a previous session. Explain the schema: what fields
  does a pattern have, and why those fields?

- [ ] **Explain why patterns are injected as HTML comments in systemMessage rather than
  as visible text.** Answer should involve "the model can read them but the user isn't
  distracted by infrastructure noise" or similar. If the answer is "we didn't think
  about it" — surface-level understanding only.

---

## 5. Skill Methodology vs. Skill Implementation

**Concept being tested**: OmniNode skills are methodology documents, not code libraries.
They encode *how to think about a problem* — steps, constraints, anti-patterns — not
*how to execute a function*. The LLM reads the skill and follows the methodology.
This is fundamentally different from a traditional API or library.

### Verification

- [ ] **Pick any ported skill and walk through how it changes the model's behavior.**
  Load `systematic-debugging` via MCP. Show a debugging prompt before and after
  loading the skill. The model's approach should visibly change — it should follow the
  skill's methodology (e.g., "reproduce first, then trace, then hypothesize") rather
  than just jumping to a fix.

- [ ] **Explain why skills are markdown files and not Python functions.** Answer should
  involve "the LLM is the runtime — it reads the methodology and applies it" and
  "a Python function would execute logic, but we want to shape reasoning, not execute
  code." If the answer is "markdown is easier" — partial credit only.

- [ ] **Identify one skill that would NOT port well from omniclaude and explain why.**
  Good answers: deploy-local-plugin (requires Claude Code's plugin system),
  merge-sweep (requires GitHub MCP + org-level access), autopilot (requires headless
  `claude -p`). The point is understanding which skills are methodology-portable and
  which are infrastructure-bound.

---

## 6. Architecture Reasoning (Oral or Written)

**Concept being tested**: Can the team explain *why* the system is built this way,
not just *what* they built?

### Verification (pick any 3)

- [ ] **Why three layers instead of one?** Bad answer: "separation of concerns."
  Good answer: "Rules are always loaded — zero-cost, but you can't make decisions with
  them. Hooks fire automatically but can't do complex multi-step work. MCP tools are
  powerful but only fire when the model decides to call them. Each layer has a different
  reliability-vs-capability trade-off."

- [ ] **What happens if Cursor drops hook support in v1.8?** Good answer: "We fall
  back to Phases 1-2 — rules + MCP still work. Routing becomes passive (model calls
  `get_agent_context` instead of `on_prompt.py` doing it automatically). Compliance
  becomes opt-in instead of automatic. The system degrades gracefully, it doesn't break."

- [ ] **Why is the routing confidence floor 0.55 and not 0.80?** Good answer involves
  balancing false positives (routing to wrong agent) vs false negatives (falling through
  to generic agent too often). The number itself doesn't matter — understanding that
  it's a tunable trade-off does.

- [ ] **Why does omniclaude have 80+ skills but you only ported 13?** Good answer:
  "Most omniclaude skills depend on infrastructure we don't have — Kafka, Linear MCP,
  Docker runtime, multi-repo worktrees. We ported the methodology-only skills that
  work in any IDE. Quality over quantity." Bad answer: "We ran out of time."

- [ ] **What would you build next if you had another semester?** Looking for: pattern
  lifecycle with real DB, routing accuracy evaluation loop, multi-agent coordination.
  NOT looking for: "port more skills" or "add more rules."

---

## Grading Summary

| Category | Weight | What it tests |
|----------|--------|---------------|
| Layer Separation | 20% | Do they know why three layers, not one? |
| Automatic Routing | 20% | Does routing happen without the model asking? |
| Compliance as Behavior | 15% | Do guardrails fire automatically? |
| Pattern Persistence | 15% | Does learning cross session boundaries? |
| Skill Methodology | 15% | Do they understand skills as reasoning, not code? |
| Architecture Reasoning | 15% | Can they explain *why*, not just *what*? |

**A**: Nails 5-6 categories with clear evidence and articulate reasoning.
**B**: Solid on 3-4 categories, weaker reasoning on the rest.
**C**: Built the thing, can demo it, but can't explain why the architecture matters.
**D**: Built parts of it, can't trace a prompt through all three layers.
