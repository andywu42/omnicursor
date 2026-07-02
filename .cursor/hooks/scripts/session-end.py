"""sessionEnd hook — emit the true session-close event.

Fires when Cursor closes a composer conversation (distinct from ``stop``, which
marks the end of an agent loop). Fire-and-forget: Cursor logs but does not consume
the response, so this only emits ``onex.evt.omnicursor.session-ended.v1`` and logs
locally. Complements ``stop`` (loop-end) with a real conversation-close signal.

Node contract: ``node_cursor_session_outcome_orchestrator`` (session lifecycle).
Stdlib only; always exits 0; never blocks Cursor.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

_hooks = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_hooks / "lib"))
sys.path.insert(0, str(_hooks.parent.parent / "src"))

from _common import (  # noqa: E402
    log_event,
    read_session_context,
    read_stdin,
    write_stdout,
)
from emit_client import send_event  # noqa: E402


def main() -> None:
    _start = time.monotonic()
    try:
        data = read_stdin()
        conversation_id = data.get("conversation_id", "")
        session_id = data.get("session_id", "")
        reason = data.get("reason", "")
        duration_ms = data.get("duration_ms")
        final_status = data.get("final_status", "")
        error_message = data.get("error_message", "")

        session = read_session_context()
        correlation_id = session.get("latest_correlation_id", "")

        hook_ms = int((time.monotonic() - _start) * 1000)
        log_event(
            {
                "event": "session_ended",
                "conversation_id": conversation_id,
                "session_id": session_id,
                "correlation_id": correlation_id,
                "reason": reason,
                "final_status": final_status,
                "duration_ms": duration_ms,
                "hook_duration_ms": hook_ms,
            }
        )

        send_event(
            "onex.evt.omnicursor.session-ended.v1",
            {
                "conversation_id": conversation_id,
                "session_id": session_id,
                "correlation_id": correlation_id,
                "reason": reason,
                "final_status": final_status,
                "duration_ms": duration_ms,
                "error_message": error_message or None,
            },
        )
    except Exception:
        pass
    write_stdout({})


if __name__ == "__main__":
    main()
