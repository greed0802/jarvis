"""MainWorkbenchScreen — multi-panel grid layout."""

from __future__ import annotations

from textual.screen import Screen
from textual.containers import Horizontal

from jarvis.ui.textual.widgets.header import WorkflowHeaderWidget
from jarvis.ui.textual.widgets.inspector import FindingInspectorWidget
from jarvis.ui.textual.widgets.viewer import EvidenceViewerWidget
from jarvis.ui.textual.widgets.chat import GroundedChatWidget

class MainWorkbenchScreen(Screen):
    """Main multi-panel screen for the workbench TUI.

    Layout:
        WorkflowHeaderWidget (top, full width)
        Horizontal panel of (Inspector | Evidence Viewer | Chat)
    """

    def compose(self) -> None:
        yield WorkflowHeaderWidget()
        with Horizontal():
            yield FindingInspectorWidget()
            yield EvidenceViewerWidget()
            yield GroundedChatWidget()

    @property
    def header(self) -> WorkflowHeaderWidget:
        return self.query_one(WorkflowHeaderWidget)

    @property
    def inspector(self) -> FindingInspectorWidget:
        return self.query_one(FindingInspectorWidget)

    @property
    def viewer(self) -> EvidenceViewerWidget:
        return self.query_one(EvidenceViewerWidget)

    @property
    def chat(self) -> GroundedChatWidget:
        return self.query_one(GroundedChatWidget)