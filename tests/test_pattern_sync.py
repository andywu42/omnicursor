"""Tests for omnicursor.sync.pattern_sync."""

from __future__ import annotations

import json
import urllib.error
from pathlib import Path
from unittest import mock

from omnicursor.sync.pattern_sync import run


def test_run_uses_default_base_url_port_18091(tmp_path: Path) -> None:
    target = tmp_path / "learned.json"
    captured: dict[str, str] = {}
    raw = json.dumps({"patterns": []}).encode()

    class _Resp:
        def __enter__(self) -> "_Resp":
            return self

        def __exit__(self, *_a: object) -> None:
            return None

        def read(self) -> bytes:
            return raw

    def fake_urlopen(req, **_kw):  # type: ignore[no-untyped-def]
        captured["url"] = req.full_url
        return _Resp()

    with (
        mock.patch.dict("omnicursor.sync.pattern_sync.os.environ", {}, clear=True),
        mock.patch("omnicursor.sync.pattern_sync.urllib.request.urlopen", fake_urlopen),
    ):
        assert run(target, timeout_s=1.0) is True

    assert captured["url"] == "http://127.0.0.1:18091/api/v1/patterns"


def test_run_writes_list_response(tmp_path: Path) -> None:
    target = tmp_path / "learned.json"
    payload = [{"pattern_id": "p1", "domain": "test", "description": "d"}]
    raw = json.dumps(payload).encode()

    class _Resp:
        def __enter__(self) -> "_Resp":
            return self

        def __exit__(self, *_a: object) -> None:
            return None

        def read(self) -> bytes:
            return raw

    def fake_urlopen(*_a, **_kw):  # type: ignore[no-untyped-def]
        return _Resp()

    with mock.patch("omnicursor.sync.pattern_sync.urllib.request.urlopen", fake_urlopen):
        assert run(target, base_url="http://example.invalid", timeout_s=1.0) is True
    data = json.loads(target.read_text())
    assert data["patterns"] == payload


def test_run_writes_dict_with_patterns_key(tmp_path: Path) -> None:
    target = tmp_path / "out.json"
    body = {"patterns": [{"pattern_id": "x"}]}
    raw = json.dumps(body).encode()

    class _Resp:
        def __enter__(self) -> "_Resp":
            return self

        def __exit__(self, *_a: object) -> None:
            return None

        def read(self) -> bytes:
            return raw

    def fake_urlopen(*_a, **_kw):  # type: ignore[no-untyped-def]
        return _Resp()

    with mock.patch("omnicursor.sync.pattern_sync.urllib.request.urlopen", fake_urlopen):
        assert run(target, base_url="http://example.invalid") is True
    assert json.loads(target.read_text()) == body


def test_run_merges_remote_patterns_with_local(tmp_path: Path) -> None:
    target = tmp_path / "learned.json"
    target.write_text(
        json.dumps(
            {
                "patterns": [
                    {"pattern_id": "local-1", "domain": "local"},
                    {"pattern_id": "shared", "domain": "local-shared"},
                ]
            }
        ),
        encoding="utf-8",
    )
    remote = {
        "patterns": [
            {"pattern_id": "shared", "domain": "remote-should-not-overwrite"},
            {"pattern_id": "remote-1", "domain": "remote"},
        ]
    }
    raw = json.dumps(remote).encode()

    class _Resp:
        def __enter__(self) -> "_Resp":
            return self

        def __exit__(self, *_a: object) -> None:
            return None

        def read(self) -> bytes:
            return raw

    def fake_urlopen(*_a, **_kw):  # type: ignore[no-untyped-def]
        return _Resp()

    with mock.patch("omnicursor.sync.pattern_sync.urllib.request.urlopen", fake_urlopen):
        assert run(target, base_url="http://example.invalid") is True

    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["patterns"] == [
        {"pattern_id": "local-1", "domain": "local"},
        {"pattern_id": "shared", "domain": "local-shared"},
        {"pattern_id": "remote-1", "domain": "remote"},
    ]


def test_run_returns_false_on_network_error(tmp_path: Path) -> None:
    target = tmp_path / "missing.json"
    with mock.patch(
        "omnicursor.sync.pattern_sync.urllib.request.urlopen",
        side_effect=OSError("no network"),
    ):
        assert run(target, base_url="http://127.0.0.1:1", timeout_s=0.1) is False
    assert not target.exists()


def test_run_keeps_local_file_when_network_unavailable(tmp_path: Path) -> None:
    target = tmp_path / "learned.json"
    local = {"patterns": [{"pattern_id": "local-only"}]}
    target.write_text(json.dumps(local), encoding="utf-8")

    with mock.patch(
        "omnicursor.sync.pattern_sync.urllib.request.urlopen",
        side_effect=OSError("no network"),
    ):
        assert run(target, base_url="http://127.0.0.1:1", timeout_s=0.1) is False

    assert json.loads(target.read_text(encoding="utf-8")) == local


def test_run_offline_falls_back_to_local_only_without_raising(tmp_path: Path) -> None:
    target = tmp_path / "learned.json"
    local = {"patterns": [{"pattern_id": "local-a"}, {"pattern_id": "local-b"}]}
    target.write_text(json.dumps(local), encoding="utf-8")

    with mock.patch(
        "omnicursor.sync.pattern_sync.urllib.request.urlopen",
        side_effect=urllib.error.URLError("offline"),
    ):
        # Offline stack should not raise and should keep local data as-is.
        result = run(target, base_url="http://127.0.0.1:18091", timeout_s=0.1)

    assert result is False
    assert json.loads(target.read_text(encoding="utf-8")) == local
