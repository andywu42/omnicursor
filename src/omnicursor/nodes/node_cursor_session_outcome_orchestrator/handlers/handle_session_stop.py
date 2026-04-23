# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from omnicursor.nodes.node_cursor_session_outcome_orchestrator.models.input import SessionOutcomeInput
from omnicursor.nodes.node_cursor_session_outcome_orchestrator.models.output import SessionOutcomeOutput


def _load_stop() -> ModuleType:
    repo = Path(__file__).resolve().parents[5]
    path = repo / ".cursor" / "hooks" / "scripts" / "stop.py"
    if not path.is_file():
        raise RuntimeError(f"stop.py not found at {path}")
    spec = importlib.util.spec_from_file_location("_omnicursor_hook_stop", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load stop from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def handle_session_stop(input: SessionOutcomeInput) -> SessionOutcomeOutput:
    hook = _load_stop()
    outcome, reason = hook.derive_session_outcome(input.status, input.events)
    return SessionOutcomeOutput(outcome=outcome, reason=reason)
