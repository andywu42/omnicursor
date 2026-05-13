# OmniNode SOW (February–May 2026) vs. Current OmniCursor Architecture

This note compares the **architecture described in the team Statement of Work (SOW)**—a Cursor-facing integration centered on **an MCP server as the OmniNode bridge**—to the **current OmniCursor repo shape**, which is **Cursor-native first** (rules, hooks, file-backed skills) with **optional MCP** for specific external tools and a **thin bridge** to OmniNode-style execution elsewhere (for example OmniMarket-backed nodes).

Primary SOW sources: stakeholder PDF (“OmniNode – Statement of Work,” Sponsor Jonah Gray).

Primary current sources: [`README.md`](../README.md), [`docs/ARCHITECTURE.md`](./ARCHITECTURE.md), [`docs/CURRENT_STATE.md`](./CURRENT_STATE.md).

---

## Side-by-side summary

| Concern | SOW (original / “paper” architecture) | Current repo (implemented direction) |
|--------|----------------------------------------|-------------------------------------|
| **Integration spine** | Cursor → **MCP server** → OmniNode (expose tools, enforce contracts, manage requests) | Cursor → **hooks + rules + skills on disk**; MCP used where Cursor plugs in external tools (e.g. ticketing), not as the only behavioral layer |
| **Behavior & safety** | Largely implied via MCP-mediated contracts | Explicit **lifecycle hooks**: prompt routing hints, shell guard tiers, diagnostic post-edit checks, session outcome aggregation |
| **Skills** | Deliverable: `.md` skills for workflows | Implemented: mirrored `skills/*.md` + `.cursor/skills/…`, with compliance smoke-checks in `src/omnicursor/` for CI |
| **Contracts / validation** | MCP layer “enforce contracts” alongside OmniNode runtime | Separation of concerns: **OmniMarket owns** node contracts and validation at execution time; OmniCursor stays a **thin mapper** from intent → tool/subprocess invocation |
| **Intelligence / memory** | **Postgres** as the intelligence layer (tasks, workflows) | **Local, file-backed patterns** (`~/.omnicursor/…`), session records, optional **Kafka / event-bus**-oriented wiring documented for pipeline feedback; Postgres appears in **`compose.yaml`** as part of broader local stack rather than MCP being the persistence API |
| **Testing** | Unit tests on skills/MCP pieces; integration across Cursor ↔ MCP ↔ OmniNode | **`pytest`** on library + deterministic hook behavior + rubric-aligned **3-bucket** model; avoids pretending unavailable external services succeeded |
| **Scope posture** | Prototype / proof of concept (“not fully polished”) | Same capstone realism, but with **explicit invariants** (starter-pack buckets, frozen HTTP adapter sketch in `ARCHITECTURE.md` for Bucket-style skills) |

---

## What stayed aligned with the SOW

- **Goal**: Cursor as a disciplined programming assistant—debugging, repeatable workflows, and structured methodology rather than one-off improvisation.
- **Artifacts**: Skills in Markdown, documentation set (quickstart / architecture / dev notes), Docker-related local infrastructure, Python (+ TypeScript where applicable) as core languages.
- **OmniNode vocabulary**: Nodes, handlers, contracts, and YAML-centric configuration remain the conceptual backbone; OmniCursor surfaces them through docs and mirrored **node contracts** concepts in `src/omnicursor/` for tests and teaching.

---

## Where the current design deliberately diverges (and why that helps)

### 1. Hooks and rules vs. MCP as the universal pipe

The SOW diagrams place **MCP** between Cursor AI and OmniNode for tool exposure and request shaping. OmniCursor instead uses **native Cursor hooks** on the latency-sensitive path (prompt submit, shell execution, edits, session stop). MCP remains valuable for **well-scoped integrations** Cursor already supports (external trackers), but it is **not** required for baseline routing or guardrail behavior.

**Benefits**: faster feedback, fewer moving parts during everyday editing, deterministic behavior easier to audit in-repo, and a clearer story for **offline-capable methodology** when external services are down.

### 2. Separation of OmniCursor vs. OmniMarket (no duplicated node semantics)

OmniMarket is treated as owning **workflow, node semantics, and contract validation**. OmniCursor concentrates on **capturing intent, invoking approved transports, rendering results**.

**Benefits**: single source of truth for node correctness (avoids drift between “MCP contract checks” and real handlers), lowers maintenance burden, and matches sponsor direction that **business logic stays in OmniNode-affiliated runtime**, not in IDE glue.

### 3. Three-bucket capability model vs. flat “everything is integrated” diagram

Implementation docs articulate **Bucket 1 / 2 / 3** tiers: pure methodology, local-data hybrid, and external-integration skills. Bucket 3 calls are designed to **fail soft** when services are unreachable (timeouts, blocked dry runs).

**Benefits**: teaching and grading clarity, predictable degradation, and safer demos when Linear/Kafka/full validators are absent.

### 4. Patterns and telemetry: phased complexity

The SOW foregrounds **Postgres** as **the** intelligence substrate. OmniCursor emphasizes **immediate local persistence** for patterns/events and folds larger data-plane pieces into **compose-backed** infra as an optional deepening path—not the minimum viable student path.

**Benefits**: demos work on a laptop without standing up full intelligence services; richer persistence can evolve without rewriting the UX layer.

### 5. Operational clarity for education and CI

The Python library exposes **routing, skill loading, and compliance helpers** exercised by **`pytest`**; hooks pledge **stdlib-only** execution.

**Benefits**: reproducible checks (`ruff`, tests, compliance registry) tied to identifiable files—more objective than asserting “MCP integration passed” without local OmniNode infra.

---

## Honest deltas (things the SOW foregrounded but the repo does differently)

| SOW expectation | Current reality |
|-----------------|----------------|
| MCP is *the* bridge | MCP is important but **secondary** to hooks/rules for orchestration ergonomics inside Cursor. OmniNode bridging is biased toward **subprocess / OmniMarket checkout** paths per repo guidance—not “one MCP façade over all handlers.” |
| Contract enforcement centralized in MCP | Enforcement is anchored in **OmniMarket nodes** where execution happens; MCP does not pretend to duplicate full validation. |

---

## Conclusion for stakeholders

The SOW framed a credible **thin-client plugin** narrative: MCP mediates nearly everything touching OmniNode, with Postgres absorbing learning signals. OmniCursor matured into an **IDE-native integration**: **deterministic hooks** provide guardrails and routing, **rules + skills** carry methodology, and **MCP/external services** sit at explicitly bounded attachment points—while **heavy orchestration correctness** stays in OmniNode-aligned runtimes (**OmniMarket**). That split trades a diagrammatic “one server in the middle” for **lower duplication, sharper ownership boundaries, simpler local development,** and **clearer phased adoption** from classroom prototype to fuller intelligence-stack deployments.
