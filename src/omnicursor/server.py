"""Minimal OmniCursor MCP server."""

from __future__ import annotations

import os
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

from .agents import get_agent_context as build_agent_context
from .compliance import check_compliance as run_compliance_check
from .skills import SkillRepository


mcp = FastMCP("OmniCursor", json_response=True)
skill_repository = SkillRepository()


def build_agent_context_payload(category: str) -> Dict[str, Any]:
    """Build a JSON-friendly agent context payload."""

    return build_agent_context(category).model_dump(mode="json")


def build_skill_payload(skill_name: str) -> Dict[str, Any]:
    """Build a JSON-friendly skill payload."""

    return skill_repository.load_skill(skill_name).model_dump(mode="json")


def build_compliance_payload(skill_name: str, response_summary: str) -> Dict[str, Any]:
    """Build a JSON-friendly compliance check payload."""

    return run_compliance_check(skill_name, response_summary).model_dump(mode="json")


@mcp.tool()
def get_agent_context(category: str) -> Dict[str, Any]:
    """Return OmniCursor routing context for a rule-selected category."""

    return build_agent_context_payload(category)


@mcp.tool()
def invoke_skill(skill_name: str) -> Dict[str, Any]:
    """Load a Markdown skill from the repository-local skills directory."""

    return build_skill_payload(skill_name)


@mcp.tool()
def check_compliance(skill_name: str, response_summary: str) -> Dict[str, Any]:
    """Check whether a model response complies with a skill's expected output pattern.

    Args:
        skill_name: Which skill was used (e.g., "systematic-debugging").
        response_summary: A summary of what the model produced.

    Returns a compliance checklist with pass/fail for each expected element.
    """

    return build_compliance_payload(skill_name, response_summary)


def main() -> None:
    """Run the server with the selected MCP transport."""

    transport = os.getenv("OMNICURSOR_MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
