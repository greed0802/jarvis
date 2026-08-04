"""Interactive CLI REPL Adapter."""

from __future__ import annotations
from typing import Any
import sys
import asyncio

from jarvis.application.conversation import ConversationService
from jarvis.application.contracts import ConversationRequest
from jarvis.cli.formatter import BaseResponseRenderer
from jarvis.cli.slash_commands import CommandRegistry

class InteractiveCLIWorkbench:
    """Passive REPL reader executing prompt loops and presenting formatted results."""

    def __init__(self, service: ConversationService, renderer: BaseResponseRenderer):
        self._service = service
        self._renderer = renderer
        self._registry = CommandRegistry(service, renderer)
        self._running = False

    async def start_repl(self) -> None:
        """Run terminal input loop processing SIGINT exceptions gracefully."""
        self._running = True
        print("\nWelcome to Jarvis Workbench (Track C1). Type /help for commands.")

        while self._running:
            try:
                # Note: input() blocks async loops in standard REPL; we use asyncio.to_thread
                user_input = await asyncio.to_thread(input, "\njarvis> ")
                user_input = user_input.strip()

                if not user_input:
                    continue

                if self._registry.can_handle(user_input):
                    result = self._registry.handle(user_input)
                    print(result)
                    continue

                # Normal prompt execution
                req = ConversationRequest(prompt=user_input)
                resp, trace = await self._service.execute(req)

                self._registry.last_trace = trace

                print(self._renderer.render_response(resp), end="")
                print(self._renderer.render_metrics(trace), end="")

            except KeyboardInterrupt:
                # Graceful cancellation of prompt without exiting completely yet
                print("\n[Execution cancelled. Press Ctrl+C again to exit.]")
            except EOFError:
                print("\nExiting...")
                self._running = False
            except SystemExit:
                self._running = False
            except Exception as e:
                print(f"\n[Error] {e}")