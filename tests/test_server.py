import pytest


pytest.importorskip("mcp")
pytest.importorskip("pydantic")

from omnicursor.server import get_agent_context, invoke_skill, check_compliance


def test_get_agent_context_tool_returns_debugging_profile() -> None:
    payload = get_agent_context("debugging")

    assert payload["agent_name"] == "systematic-debugger"
    assert payload["recommended_skill"] == "systematic-debugging"


def test_get_agent_context_tool_returns_brainstorming_profile() -> None:
    payload = get_agent_context("brainstorming")

    assert payload["agent_name"] == "brainstorming-guide"
    assert payload["recommended_skill"] == "brainstorming"


def test_invoke_skill_tool_loads_markdown_skill() -> None:
    payload = invoke_skill("systematic-debugging")

    assert payload["skill_name"] == "systematic-debugging"
    assert payload["path"] == "skills/systematic-debugging.md"


def test_invoke_skill_tool_loads_brainstorming_skill() -> None:
    payload = invoke_skill("brainstorming")

    assert payload["skill_name"] == "brainstorming"
    assert payload["path"] == "skills/brainstorming.md"


def test_check_compliance_tool_returns_result() -> None:
    payload = check_compliance(
        "systematic-debugging",
        "The symptom was an error. The cause is a bug. The fix updates the code. Run tests to verify.",
    )

    assert payload["skill_name"] == "systematic-debugging"
    assert payload["compliant"] is True
    assert payload["missing"] == []


def test_check_compliance_tool_detects_missing() -> None:
    payload = check_compliance(
        "systematic-debugging",
        "There was an error. I think the cause is X.",
    )

    assert payload["compliant"] is False
    assert "suggests_minimal_fix" in payload["missing"]
