# OmniNode Cursor Starter Pack

A self-contained Cursor Rules starter pack for porting OmniNode's Claude Code skills to Cursor.
Designed for the USF Capstone course — no OmniNode infrastructure required.

This starter pack covers the first 3 stages of OmniNode's 5-stage code generation pipeline:
**brainstorm → plan → ticket**. It uses only local files and public documentation.

---

## What's Inside

```
cursor-omninode/
├── .cursor/rules/          6 Cursor Rules (.mdc)
│   ├── 00-omninode-concepts.mdc    Always-on: vocabulary and bucket classification
│   ├── 01-codebase-research.mdc    Always-on: bounded file reading guard
│   ├── 10-brainstorming.mdc        Bucket 1: idea → design doc
│   ├── 11-writing-plans.mdc        Bucket 1: design doc → implementation plan
│   ├── 12-plan-ticket.mdc          Bucket 2: plan → ticket YAML template
│   └── 20-adapter-stub.mdc         Bucket 3 stub: shows adapter pattern, not wired
│
├── docs/
│   ├── STUDENT_GUIDE.md            6-phase project guide with pass/fail criteria
│   ├── SKILL_TRANSLATION_TEMPLATE.md  Template for porting SKILL.md → .mdc rule
│   └── ARCHITECTURE.md             3-bucket spec + frozen adapter contract
│
├── tests/
│   ├── prompts/                    8 test prompts to run against your rules
│   └── rubrics/                    4 rubric files with pass/fail checklists
│
├── HOW_TO_RUN_IN_CURSOR.md         Setup and usage instructions
└── README.md                       This file
```

---

## Quick Start

1. Open this folder in Cursor: `File → Open Folder → cursor-omninode/`
2. Confirm 6 rules are loaded: `Settings → Rules`
3. Run a test: open Composer (`⌘I`), type `@10-brainstorming I want to add a webhook to omniclaude`
4. Check the output against `tests/rubrics/brainstorming.md`

For full instructions see **[HOW_TO_RUN_IN_CURSOR.md](HOW_TO_RUN_IN_CURSOR.md)**.

---

## Project Guide

The 6-phase capstone project is documented in **[docs/STUDENT_GUIDE.md](docs/STUDENT_GUIDE.md)**:

| Phase | Summary |
|-------|---------|
| 1 | Read and classify 3 OmniNode skills from the public omniclaude repo |
| 2 | Port the brainstorming skill — pass all 3 test prompts |
| 3 | Port writing-plans + plan-ticket — run the full 3-step chain |
| 4 | Attempt porting decompose-epic — document the integration gap |
| 5 | Implement the adapter stub — test fail-soft behavior |
| 6 | Demo: full chain in one live Cursor session |

**Source skills** (public omniclaude repo):
- `plugins/onex/skills/brainstorming/SKILL.md`
- `plugins/onex/skills/writing-plans/SKILL.md`
- `plugins/onex/skills/plan-ticket/SKILL.md`
- `plugins/onex/skills/decompose-epic/SKILL.md` (Phase 4 reference)

---

## Architecture

The 3-bucket classification determines what each rule may do:

| Bucket | Rule | Examples |
|--------|------|---------|
| **1 — Pure Methodology** | No external service calls; may write local files | `brainstorming`, `writing-plans` |
| **2 — Local-Data Hybrid** | Reads bounded local files; no external services | `plan-ticket` |
| **3 — External Integration** | Requires Linear MCP, Kafka, or Python runtime | `decompose-epic` (stub only) |

For the full architecture spec including the frozen adapter contract, see **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.
