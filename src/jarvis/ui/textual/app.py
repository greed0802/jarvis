"""TextualWorkbenchApp — main TUI app implementing WorkbenchView protocol.

Uses duck-typing for WorkbenchView (not inheritance) because Textual's App
and Protocol have incompatible metaclasses.
"""

from __future__ import annotations

from textual.app import App

from jarvis.presentation.viewmodels import WorkbenchViewModel
from jarvis.presentation.workbench import WorkbenchOrchestrator
from jarvis.ui.textual.controller import InteractionController
from jarvis.ui.textual.sink import TextualInteractionSink
from jarvis.ui.textual.screens.main_screen import MainWorkbenchScreen

class TextualWorkbenchApp(App):
    """Textual-based workbench TUI satisfying WorkbenchView by duck typing."""

    CSS = """
    MainWorkbenchScreen {
        layout: grid;
        grid-size: 1 4;
        grid-rows: auto 1fr;
    }
    WorkflowHeaderWidget {
        height: auto;
        column-span: 4;
    }
    FindingInspectorWidget {
        width: 1fr;
        border: solid green;
    }
    EvidenceViewerWidget {
        width: 1fr;
        border: solid blue;
    }
    GroundedChatWidget {
        width: 1fr;
        border: solid yellow;
    }
    """

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("escape", "clear_selection", "Clear selection"),
    ]

    def __init__(
        self,
        orchestrator: WorkbenchOrchestrator | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._orchestrator = orchestrator or WorkbenchOrchestrator()
        self._sink = TextualInteractionSink(self._orchestrator)
        self._controller = InteractionController(self._sink)
        self._headless = False
        self._screen: MainWorkbenchScreen | None = None

    # ---- WorkbenchView protocol (duck-typed, AC-1) ----

    def render(self, view_model: WorkbenchViewModel) -> None:
        """Render the complete workbench from an immutable WorkbenchViewModel."""
        self._controller.set_view_model(view_model)
        if self._headless or not self._screen:
            return
        vm = view_model
        self._screen.header.update_view_model(vm.workflow_status)
        self._screen.inspector.update_view_model(vm.findings)
        self._screen.viewer.update_view_model(vm.evidence_items)
        self._screen.chat.update_view_model(vm.chat_responses)

    def set_headless(self, enabled: bool) -> None:
        self._headless = enabled

    # ---- Textual lifecycle ----

    def on_mount(self) -> None:
        self._screen = MainWorkbenchScreen()
        self.push_screen(self._screen)
        vm = self._orchestrator.current_view_model
        self.render(vm)

    # ---- Keyboard bindings ----

    def action_clear_selection(self) -> None:
        self._controller.on_clear_selection()
        self._refresh_view()

    def _refresh_view(self) -> None:
        vm = self._orchestrator.current_view_model
        self.render(vm)