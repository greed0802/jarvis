"""Unit tests for Shell components (formatter, history, command handlers)."""

from __future__ import annotations

import pytest

from jarvis.ui.shell.formatter import ShellFormatter
from jarvis.ui.shell.history import ShellHistory


class TestShellFormatter:
    """Verify formatter produces clean deterministic output."""

    def test_banner_contains_version(self) -> None:
        f = ShellFormatter()
        banner = f.banner("1.2.3", "MyWorkspace", "RUNNING")
        assert "1.2.3" in banner
        assert "MyWorkspace" in banner
        assert "RUNNING" in banner
        assert "help" in banner

    def test_table_formats_rows(self) -> None:
        f = ShellFormatter()
        result = f.table(["A", "B"], [["x", "y"], ["xx", "yy"]])
        assert "A" in result
        assert "x" in result
        assert "yy" in result

    def test_table_empty(self) -> None:
        f = ShellFormatter()
        assert "(none)" in f.table(["A"], [])

    def test_key_value(self) -> None:
        f = ShellFormatter()
        result = f.key_value({"Name": "Jarvis", "Ver": "1.0"})
        assert "Name" in result and "Jarvis" in result

    def test_key_value_empty(self) -> None:
        assert "(empty)" in ShellFormatter.key_value({})

    def test_success(self) -> None:
        assert "[OK]" in ShellFormatter.success("done")

    def test_error(self) -> None:
        assert "[Error]" in ShellFormatter.error("failed")

    def test_section(self) -> None:
        result = ShellFormatter.section("Title", "body")
        assert "Title" in result and "body" in result


class TestShellHistory:
    """Verify history recording works."""

    def test_record_in_memory(self) -> None:
        h = ShellHistory(memory_service=None)
        h.record("help")
        h.record("status")
        assert h.count == 2
        assert h.entries == ["help", "status"]

    def test_record_with_memory_service(self) -> None:
        """If a memory service is provided, entries are persisted."""

        class FakeMemory:
            def __init__(self):
                self.stored = []
            def store_entry(self, **kw):
                self.stored.append(kw)

        mem = FakeMemory()
        h = ShellHistory(memory_service=mem)
        h.record("help", workspace_id="ws-1")
        assert h.count == 1
        assert len(mem.stored) == 1
        assert mem.stored[0]["category"] == "shell_history"

    def test_record_survives_memory_error(self) -> None:
        """History still works even if persistence fails."""

        class BrokenMemory:
            def store_entry(self, **kw):
                raise RuntimeError("boom")

        h = ShellHistory(memory_service=BrokenMemory())
        h.record("help")
        assert h.count == 1
