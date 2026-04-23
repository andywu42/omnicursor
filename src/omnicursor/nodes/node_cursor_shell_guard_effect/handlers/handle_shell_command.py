# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from omnicursor.nodes.node_cursor_shell_guard_effect.models.input import ShellGuardInput
from omnicursor.nodes.node_cursor_shell_guard_effect.models.output import ShellGuardOutput


def _load_shell_guard() -> ModuleType:
    repo = Path(__file__).resolve().parents[5]
    path = repo / ".cursor" / "hooks" / "scripts" / "shell-guard.py"
    if not path.is_file():
        raise RuntimeError(f"shell-guard.py not found at {path}")
    spec = importlib.util.spec_from_file_location("_omnicursor_hook_shell_guard", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load shell-guard from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def handle_shell_command(input: ShellGuardInput) -> ShellGuardOutput:
    hook = _load_shell_guard()
    result = hook.guard_command(input.command, conversation_id=input.conversation_id)
    return ShellGuardOutput(
        permission=result.get("permission", "allow"),
        user_message=result.get("userMessage"),
    )
