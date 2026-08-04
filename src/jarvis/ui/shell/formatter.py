"""Shell output formatter — clean readable text rendering."""

from __future__ import annotations

from typing import Any


class ShellFormatter:
    """Renders command output as clean readable terminal text.

    No ANSI colour codes — keeps output deterministic and pipe-friendly.
    """

    @staticmethod
    def banner(version: str, workspace: str, status: str) -> str:
        """Render the startup banner."""
        lines = [
            "",
            "=" * 50,
            f"  Jarvis Platform v{version}",
            f"  Workspace: {workspace}",
            f"  Platform Status: {status}",
            '  Type "help" for available commands.',
            "=" * 50,
            "",
        ]
        return "\n".join(lines)

    @staticmethod
    def table(headers: list[str], rows: list[list[str]]) -> str:
        """Render a simple aligned text table."""
        if not rows:
            return "  (none)"

        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        header_line = "  ".join(
            h.ljust(col_widths[i]) for i, h in enumerate(headers)
        )
        separator = "  ".join("-" * w for w in col_widths)
        body_lines = []
        for row in rows:
            line = "  ".join(
                str(cell).ljust(col_widths[i])
                for i, cell in enumerate(row)
            )
            body_lines.append(line)

        return "\n".join(["  " + header_line, "  " + separator] + ["  " + ln for ln in body_lines])

    @staticmethod
    def key_value(data: dict[str, Any]) -> str:
        """Render a key-value block."""
        if not data:
            return "  (empty)"
        max_key = max(len(str(k)) for k in data)
        lines = []
        for key, value in data.items():
            lines.append(f"  {str(key).ljust(max_key + 1)}: {value}")
        return "\n".join(lines)

    @staticmethod
    def success(message: str) -> str:
        return f"  [OK] {message}"

    @staticmethod
    def error(message: str) -> str:
        return f"  [Error] {message}"

    @staticmethod
    def info(message: str) -> str:
        return f"  {message}"

    @staticmethod
    def section(title: str, content: str) -> str:
        """Render a titled section."""
        return f"\n  {title}\n  {'─' * len(title)}\n{content}"
