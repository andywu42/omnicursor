from omnicursor.agents import get_agent_context, AGENT_CONTEXTS


def test_debugging_category() -> None:
    ctx = get_agent_context("debugging")
    assert ctx.agent_name == "systematic-debugger"
    assert ctx.recommended_skill == "systematic-debugging"
    assert ctx.description != ""


def test_brainstorming_category() -> None:
    ctx = get_agent_context("brainstorming")
    assert ctx.agent_name == "brainstorming-guide"
    assert ctx.recommended_skill == "brainstorming"
    assert ctx.description != ""


def test_planning_category() -> None:
    ctx = get_agent_context("planning")
    assert ctx.agent_name == "plan-writer"
    assert ctx.recommended_skill == "writing-plans"
    assert ctx.description != ""


def test_ticketing_category() -> None:
    ctx = get_agent_context("ticketing")
    assert ctx.agent_name == "ticket-planner"
    assert ctx.recommended_skill == "plan-ticket"
    assert ctx.description != ""


def test_adapter_category() -> None:
    ctx = get_agent_context("adapter")
    assert ctx.agent_name == "adapter-guide"
    assert ctx.recommended_skill == "adapter-stub"
    assert ctx.description != ""


def test_fallback_for_unknown_category() -> None:
    ctx = get_agent_context("unknown-category")
    assert ctx.agent_name == "omnicursor-generalist"
    assert ctx.recommended_skill is None
    assert ctx.description != ""


def test_alias_debug_routes_to_debugging() -> None:
    ctx = get_agent_context("debug")
    assert ctx.agent_name == "systematic-debugger"


def test_alias_brainstorm_routes_to_brainstorming() -> None:
    ctx = get_agent_context("brainstorm")
    assert ctx.agent_name == "brainstorming-guide"


def test_alias_plan_routes_to_planning() -> None:
    ctx = get_agent_context("plan")
    assert ctx.agent_name == "plan-writer"


def test_alias_ticket_routes_to_ticketing() -> None:
    ctx = get_agent_context("ticket")
    assert ctx.agent_name == "ticket-planner"


def test_alias_adapter_stub_routes_to_adapter() -> None:
    ctx = get_agent_context("adapter-stub")
    assert ctx.agent_name == "adapter-guide"


def test_all_five_categories_present() -> None:
    expected = {"debugging", "brainstorming", "planning", "ticketing", "adapter"}
    assert set(AGENT_CONTEXTS.keys()) == expected
