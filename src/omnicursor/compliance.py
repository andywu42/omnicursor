"""Compliance checking for OmniCursor skill outputs."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from .schemas import ComplianceResult


# Each skill maps to a list of (check_name, keywords) tuples.
# A check passes if ANY of its keywords appear in the response summary.
COMPLIANCE_REGISTRY: Dict[str, List[Tuple[str, List[str]]]] = {
    "systematic-debugging": [
        ("states_problem_clearly", [
            "symptom", "error", "failure", "bug", "issue", "problem",
            "traceback", "exception", "regression",
        ]),
        ("provides_hypothesis", [
            "hypothesis", "hypotheses", "cause", "theory", "suspect",
            "likely", "root cause", "because",
        ]),
        ("suggests_minimal_fix", [
            "fix", "patch", "change", "update", "modify", "resolve",
            "smallest", "minimal",
        ]),
        ("includes_verification_step", [
            "verify", "verification", "test", "confirm", "run",
            "check", "assert", "validate", "reproduce",
        ]),
    ],
    "brainstorming": [
        ("asks_clarifying_questions", [
            "question", "?", "which", "what", "how", "where", "why",
            "option", "choice", "prefer",
        ]),
        ("presents_multiple_approaches", [
            "option a", "option b", "approach", "alternative",
            "trade-off", "tradeoff", "trade off", "pros", "cons",
            "vs", "versus",
        ]),
        ("provides_recommendation", [
            "recommend", "recommendation", "suggest", "preferred",
            "best", "chosen", "selected",
        ]),
        ("includes_design_sections", [
            "architecture", "component", "data flow", "error handling",
            "testing", "design", "structure",
        ]),
        ("references_output_path", [
            "docs/plans/", "design.md", "handoff", "next step",
        ]),
    ],
    "writing-plans": [
        ("has_plan_header", [
            "goal", "architecture", "tech stack", "implementation plan",
        ]),
        ("has_exact_file_paths", [
            ".py", ".ts", ".js", ".yaml", ".yml", ".md",
            "src/", "tests/", "create:", "modify:",
        ]),
        ("follows_tdd_order", [
            "failing test", "test first", "red", "green", "tdd",
            "write test", "run test", "confirm fail", "confirm pass",
        ]),
        ("has_bite_sized_steps", [
            "step 1", "step 2", "step 3", "phase",
            "commit", "git add", "git commit",
        ]),
        ("includes_adversarial_review", [
            "adversarial", "r1", "r2", "review", "count integrity",
            "acceptance criteria",
        ]),
    ],
    "plan-ticket": [
        ("detects_repo", [
            "omniclaude", "omnibase_core", "omnibase_infra", "omnidash",
            "omniintelligence", "omnimemory", "omninode_infra", "repo",
        ]),
        ("outputs_yaml_template", [
            "yaml", "title:", "repo:", "requirements:", "verification:",
            "template", "contract",
        ]),
        ("has_requirements_section", [
            "requirement", "r1", "statement", "rationale", "acceptance",
        ]),
        ("has_verification_section", [
            "verification", "pytest", "lint", "ruff", "mypy",
            "unit_test", "unit test", "blocking",
        ]),
    ],
    "adapter-stub": [
        ("identifies_bucket_3_operation", [
            "bucket 3", "external", "linear", "kafka", "decompose",
            "adapter", "service",
        ]),
        ("constructs_dry_run_payload", [
            "dry_run", "dry run", "payload", "request",
            "/onex/api/v1/skills/", "post",
        ]),
        ("shows_fail_soft_behavior", [
            "fail-soft", "fail soft", "unavailable", "complete manually",
            "service unavailable", "fallback",
        ]),
        ("no_automatic_retry", [
            "not retry", "no retry", "do not retry", "does not retry",
            "no loop", "never retry", "manual",
        ]),
    ],
}


def check_compliance(skill_name: str, response_summary: str) -> ComplianceResult:
    """Check a response summary against the compliance registry for a skill."""

    registry_entry = COMPLIANCE_REGISTRY.get(skill_name)

    if registry_entry is None:
        return ComplianceResult(
            skill_name=skill_name,
            checks={},
            compliant=False,
            missing=[f"no_registry_entry_for_{skill_name}"],
        )

    summary_lower = response_summary.lower()
    checks: Dict[str, bool] = {}
    missing: List[str] = []

    for check_name, keywords in registry_entry:
        passed = any(kw.lower() in summary_lower for kw in keywords)
        checks[check_name] = passed
        if not passed:
            missing.append(check_name)

    return ComplianceResult(
        skill_name=skill_name,
        checks=checks,
        compliant=len(missing) == 0,
        missing=missing,
    )
