"""WorkspaceShell — Interactive command-line interface for the Jarvis Platform.

The Shell is a pure presentation layer.  It accepts user input, parses it
into commands and arguments, delegates every command to a platform service
(via CommandHandler classes), and displays the formatted result.

The Shell contains NO business logic.
"""

from __future__ import annotations

import asyncio
import logging
import uuid
from typing import Any

from jarvis.version import __version__
from jarvis.ui.shell.commands import (
    COMMAND_REGISTRY,
    CommandHandler,
    ShellContext,
)
from jarvis.ui.shell.formatter import ShellFormatter
from jarvis.ui.shell.history import ShellHistory

logger = logging.getLogger(__name__)


class WorkspaceShell:
    """Interactive command-line REPL for the Jarvis Platform.

    Created *after* the platform reaches RUNNING state.
    Its ``run()`` method blocks until the user issues ``exit`` or
    a shutdown signal is received.
    """

    def __init__(
        self,
        application: Any,
        developer_mode: bool = False,
    ) -> None:
        self._application = application
        self._developer_mode = developer_mode
        self._running = False
        self._formatter = ShellFormatter()
        self._session_id = str(uuid.uuid4())

        # Build handler lookup — supports multi-word names like "debug runtime"
        self._handlers: dict[str, CommandHandler] = {}
        for handler in COMMAND_REGISTRY:
            self._handlers[handler.name] = handler

        self._context = ShellContext(
            application=application,
            assistant=application.workspace_assistant,
            session_id=self._session_id,
            developer_mode=developer_mode,
            formatter=self._formatter,
        )

        self._history = ShellHistory(
            memory_service=getattr(application, "memory_service", None)
        )

    # ── Public API ───────────────────────────────────────────────────

    async def run(self) -> None:
        """Start the interactive REPL loop."""
        self._running = True
        self._print_banner()

        while self._running:
            try:
                prompt = self._build_prompt()
                user_input = await asyncio.to_thread(input, prompt)
                user_input = user_input.strip()

                if not user_input:
                    continue

                self._history.record(
                    user_input,
                    workspace_id=self._active_workspace_id(),
                )

                output = self._dispatch(user_input)
                if output == "__EXIT__":
                    print("\n  Shutting down Jarvis Platform...")
                    self._running = False
                    continue

                if output:
                    print(output)

            except KeyboardInterrupt:
                print("\n\n  Shutting down Jarvis Platform...")
                self._running = False

            except EOFError:
                print("\n\n  Shutting down Jarvis Platform...")
                self._running = False

            except Exception as exc:
                print(self._formatter.error(f"Unexpected error: {exc}"))

    # ── Internals ────────────────────────────────────────────────────

    def _print_banner(self) -> None:
        ws = self._context.assistant.get_active_workspace()
        ws_name = ws.name if ws else "(none)"
        banner = self._formatter.banner(
            version=__version__,
            workspace=ws_name,
            status=str(self._application.state),
        )
        print(banner)

    def _build_prompt(self) -> str:
        ws = self._context.assistant.get_active_workspace()
        if ws:
            return f"\nJarvis [{ws.name}]> "
        return "\nJarvis> "

    def _active_workspace_id(self) -> str:
        ws = self._context.assistant.get_active_workspace()
        return ws.workspace_id if ws else "default"

    def _dispatch(self, user_input: str) -> str:
        """Match input to a handler, preferring longer (multi-word) names."""
        # Try two-word match first for "debug xxx" style commands
        parts = user_input.split(maxsplit=2)
        if len(parts) >= 2:
            two_word = f"{parts[0]} {parts[1]}"
            handler = self._handlers.get(two_word)
            if handler is not None:
                if handler.developer_only and not self._developer_mode:
                    return self._formatter.error(
                        f"Unknown command: {user_input}. "
                        'Type "help" for available commands.'
                    )
                args = parts[2].split() if len(parts) > 2 else []
                return self._execute_safe(handler, args)

        # Single-word match
        parts = user_input.split(maxsplit=1)
        cmd = parts[0]
        handler = self._handlers.get(cmd)
        if handler is None:
            return self._formatter.error(
                f"Unknown command: {cmd}. "
                'Type "help" for available commands.'
            )
        if handler.developer_only and not self._developer_mode:
            return self._formatter.error(
                f"Unknown command: {cmd}. "
                'Type "help" for available commands.'
            )
        args = parts[1].split() if len(parts) > 1 else []
        return self._execute_safe(handler, args)

    def _execute_safe(
        self, handler: CommandHandler, args: list[str]
    ) -> str:
        """Execute a handler, catching and formatting exceptions."""
        try:
            return handler.execute(args, self._context)
        except Exception as exc:
            logger.exception("Command execution error")
            return self._formatter.error(str(exc))
