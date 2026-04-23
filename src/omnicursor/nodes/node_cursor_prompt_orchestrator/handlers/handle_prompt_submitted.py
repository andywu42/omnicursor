# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Handler for node_cursor_prompt_orchestrator.

Delegates to .cursor/hooks/lib/agent_scoring.py (the canonical scoring
engine) via importlib — same pattern as prompt_pattern_read.py. The hook
script itself is never modified or imported directly.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from omnicursor.agents import _ALL_RAW_AGENTS
from omnicursor.nodes.node_cursor_prompt_orchestrator.models.input import PromptOrchestratorInput
from omnicursor.nodes.node_cursor_prompt_orchestrator.models.output import PromptOrchestratorOutput


def _load_agent_scoring() -> ModuleType:
    repo = Path(__file__).resolve().parents[5]
    path = repo / ".cursor" / "hooks" / "lib" / "agent_scoring.py"
    if not path.is_file():
        raise RuntimeError(f"agent_scoring.py not found at {path}")
    name = "_omnicursor_hook_agent_scoring"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load agent_scoring from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def handle_prompt_submitted(input: PromptOrchestratorInput) -> PromptOrchestratorOutput:
    scoring = _load_agent_scoring()

    prompt_lower = input.prompt.lower()
    prompt_words: set[str] = set(scoring.extract_keywords(input.prompt))

    best_name = "polymorphic-agent"
    best_score = 0.0
    best_reason = "No agent matched"

    for agent in _ALL_RAW_AGENTS:
        name = agent.get("name", "")
        if not name:
            continue
        sc, reason = scoring.score_agent(prompt_lower, prompt_words, agent)
        if sc >= scoring.HARD_FLOOR and sc > best_score:
            best_score, best_name, best_reason = sc, name, reason

    system_message = f"<!-- OmniCursor Agent: {best_name} ({best_score:.2f}) -->"

    return PromptOrchestratorOutput(
        agent_name=best_name,
        confidence=best_score,
        reason=best_reason,
        system_message=system_message,
        patterns_injected=[],
    )
