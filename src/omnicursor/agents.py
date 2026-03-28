"""Routing contexts used by the OmniCursor MCP tools."""

from __future__ import annotations

from typing import Dict

from .schemas import AgentContext


DEFAULT_CONTEXT = AgentContext(
    agent_name="omnicursor-generalist",
    description="General-purpose fallback agent for unmatched categories.",
    instructions=[
        "Prefer the preserved Cursor rules before inventing a new workflow.",
        "Use MCP tools only to add routing context or load a local skill.",
        "Check 00-omninode-concepts for shared vocabulary.",
    ],
    recommended_skill=None,
)


AGENT_CONTEXTS: Dict[str, AgentContext] = {
    "debugging": AgentContext(
        agent_name="systematic-debugger",
        description="Structured debugging agent — reproduce, hypothesize, verify.",
        instructions=[
            "Keep 00-omninode-concepts and 01-codebase-research as the always-on base.",
            "Reproduce the issue before editing whenever a repro is available.",
            "Load the systematic-debugging skill and follow it step-by-step.",
            "Prefer the smallest verified fix over a redesign.",
        ],
        recommended_skill="systematic-debugging",
    ),
    "brainstorming": AgentContext(
        agent_name="brainstorming-guide",
        description="Collaborative idea refinement agent — one question at a time, 2-3 approaches, design doc output.",
        instructions=[
            "Reuse the preserved 10-brainstorming rule as the primary methodology.",
            "Keep research bounded with 01-codebase-research.",
            "Ask one question per message — never combine two questions.",
            "Present 2-3 approaches with named trade-offs before settling.",
            "Write design outputs to docs/plans/ using the existing handoff protocol.",
        ],
        recommended_skill="brainstorming",
    ),
    "planning": AgentContext(
        agent_name="plan-writer",
        description="Implementation plan writer — bite-sized TDD tasks with exact file paths.",
        instructions=[
            "Reuse the preserved 11-writing-plans rule as the primary methodology.",
            "Keep tasks small, explicit, and artifact-path anchored.",
            "Each step is one action, 2-5 minutes of work.",
            "Use the preserved adversarial review structure (R1-R6) before handing off.",
            "Output complete code examples, not placeholders.",
        ],
        recommended_skill="writing-plans",
    ),
    "ticketing": AgentContext(
        agent_name="ticket-planner",
        description="Ticket contract generator — deterministic repo detection and YAML template output.",
        instructions=[
            "Reuse the preserved 12-plan-ticket rule for deterministic repo detection.",
            "Follow the 3-priority chain: CWD/prompt, README, ask user.",
            "Keep output YAML-only and use the documented handoff to the linear rule.",
            "Pre-fill fields from prompt context; mark uncertain fields as FILL IN.",
        ],
        recommended_skill="plan-ticket",
    ),
    "adapter": AgentContext(
        agent_name="adapter-guide",
        description="Bucket 3 adapter stub agent — dry-run protocol and fail-soft behavior.",
        instructions=[
            "Reuse the preserved 20-adapter-stub rule for Bucket 3 dry-run behavior.",
            "Always call dry_run: true first; never skip.",
            "Do not skip the fail-soft contract described in docs/ARCHITECTURE.md.",
            "Output complete request payloads for review, never execute live calls.",
        ],
        recommended_skill="adapter-stub",
    ),
}


ALIASES = {
    "debug": "debugging",
    "bug": "debugging",
    "systematic-debugging": "debugging",
    "brainstorm": "brainstorming",
    "idea": "brainstorming",
    "design": "brainstorming",
    "writing-plans": "planning",
    "plan": "planning",
    "plans": "planning",
    "plan-ticket": "ticketing",
    "ticket": "ticketing",
    "tickets": "ticketing",
    "adapter-stub": "adapter",
    "bucket-3": "adapter",
    "stub": "adapter",
}


def normalize_category(category: str) -> str:
    """Normalize free-form categories to the v1 routing table."""

    normalized = category.strip().lower().replace("_", "-")
    return ALIASES.get(normalized, normalized)


def get_agent_context(category: str) -> AgentContext:
    """Return a structured context object for a rule-selected category."""

    normalized = normalize_category(category)
    return AGENT_CONTEXTS.get(normalized, DEFAULT_CONTEXT)
