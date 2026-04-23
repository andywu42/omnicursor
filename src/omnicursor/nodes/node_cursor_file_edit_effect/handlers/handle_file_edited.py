# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from omnicursor.nodes.node_cursor_file_edit_effect.models.input import FileEditInput
from omnicursor.nodes.node_cursor_file_edit_effect.models.output import FileEditOutput


def _load_post_edit() -> ModuleType:
    repo = Path(__file__).resolve().parents[5]
    path = repo / ".cursor" / "hooks" / "scripts" / "post-edit.py"
    if not path.is_file():
        raise RuntimeError(f"post-edit.py not found at {path}")
    spec = importlib.util.spec_from_file_location("_omnicursor_hook_post_edit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load post-edit from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def handle_file_edited(input: FileEditInput) -> FileEditOutput:
    hook = _load_post_edit()
    result = hook.handle_edit({
        "file_path": input.file_path,
        "edits": input.edits,
        "conversation_id": input.conversation_id,
    })
    return FileEditOutput(
        event=result.get("event", "file_edited"),
        file_path=result.get("file_path", input.file_path),
        language=result.get("language", "other"),
        edit_count=result.get("edit_count", 0),
        ruff_findings=result.get("ruff_findings", 0),
        conversation_id=result.get("conversation_id", input.conversation_id),
    )
