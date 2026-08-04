"""Slash command handlers."""

from __future__ import annotations
from typing import Any
import sys

from jarvis.cli.formatter import BaseResponseRenderer

class CommandRegistry:
    """Handles parsing and executing /slash commands."""

    def __init__(self, service: Any, renderer: BaseResponseRenderer):
        self._service = service
        self._renderer = renderer
        self.last_trace = None

    def can_handle(self, text: str) -> bool:
        return text.strip().startswith("/")

    def handle(self, text: str) -> str:
        cmd = text.strip().lower()

        if cmd == "/help":
            return "\nCommands:\n/status : Platform health\n/trace : Detail last execution\n/clear : Clear screen\n/exit : Graceful shutdown\n"
        elif cmd == "/status":
            status = self._service.get_status()
            return self._renderer.render_status(status)
        elif cmd == "/trace":
            if not self.last_trace:
                return "\nNo trace available for this session.\n"
            return self._renderer.render_trace_detail(self.last_trace)
        elif cmd == "/clear":
            # Return special signal or ANSI code
            return "\033[H\033[2J"
        elif cmd in ("/exit", "/quit"):
            sys.exit(0)
        else:
            return f"\nUnknown command: {cmd}\n"