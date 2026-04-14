"""Pytest configuration — section headers for hook event test groups."""

from __future__ import annotations

_SECTIONS: dict[str, str] = {
    "test_suite_event1": "Event 1 — beforeSubmitPrompt",
    "test_suite_event2": "Event 2 — beforeShellExecution",
    "test_suite_event3": "Event 3 — afterFileEdit",
    "test_suite_event4": "Event 4 — stop",
}

_state: dict[str, str | None] = {"current": None}


def pytest_runtest_logstart(nodeid: str, location: tuple) -> None:  # type: ignore[type-arg]
    """Print a section banner the first time a new event group is entered."""
    for key, label in _SECTIONS.items():
        if key in nodeid and _state["current"] != key:
            _state["current"] = key
            print(f"\n{'─' * 56}\n  {label}\n{'─' * 56}", flush=True)
            break
