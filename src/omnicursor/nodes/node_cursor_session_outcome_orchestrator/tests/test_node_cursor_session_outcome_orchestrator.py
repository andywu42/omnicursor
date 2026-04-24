# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
from __future__ import annotations

import pytest

from omnicursor.nodes.node_cursor_session_outcome_orchestrator.models.input import SessionOutcomeInput
from omnicursor.nodes.node_cursor_session_outcome_orchestrator.models.output import SessionOutcomeOutput
from omnicursor.nodes.node_cursor_session_outcome_orchestrator.handlers.handle_session_stop import handle_session_stop
from omnicursor.nodes.node_cursor_session_outcome_orchestrator.node import run


class TestSessionOutcomeModels:
    def test_input_requires_status(self):
        with pytest.raises(Exception):
            SessionOutcomeInput()

    def test_input_events_defaults_empty(self):
        i = SessionOutcomeInput(status="success")
        assert i.events == []

    def test_output_has_outcome_and_reason(self):
        o = SessionOutcomeOutput(outcome="success", reason="work done")
        assert o.outcome == "success"


class TestHandlerSessionStop:
    def test_failed_status_returns_failed(self):
        result = handle_session_stop(SessionOutcomeInput(status="failed"))
        assert result.outcome == "failed"

    def test_error_status_returns_failed(self):
        result = handle_session_stop(SessionOutcomeInput(status="error"))
        assert result.outcome == "failed"

    def test_short_session_no_work_returns_abandoned(self):
        result = handle_session_stop(SessionOutcomeInput(status="stopped", events=[]))
        assert result.outcome in {"abandoned", "unknown"}

    def test_success_with_work_done(self):
        events = [
            {"event": "file_edited", "timestamp": "2026-01-01T00:00:00"},
            {"event": "prompt_classified", "timestamp": "2026-01-01T00:01:00"},
            {"text": "Task completed successfully", "timestamp": "2026-01-01T00:02:00"},
        ]
        result = handle_session_stop(SessionOutcomeInput(status="success", events=events))
        assert result.outcome in {"success", "unknown"}

    def test_output_is_typed(self):
        result = handle_session_stop(SessionOutcomeInput(status="stopped"))
        assert isinstance(result, SessionOutcomeOutput)

    def test_reason_is_non_empty(self):
        result = handle_session_stop(SessionOutcomeInput(status="failed"))
        assert len(result.reason) > 0

    def test_outcome_is_valid_value(self):
        result = handle_session_stop(SessionOutcomeInput(status="stopped"))
        assert result.outcome in {"success", "failed", "abandoned", "unknown"}


class TestNodeRunAPI:
    def test_run_returns_output(self):
        result = run("stopped")
        assert isinstance(result, SessionOutcomeOutput)

    def test_run_failed_status(self):
        result = run("failed")
        assert result.outcome == "failed"
