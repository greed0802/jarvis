"""WorkflowHeaderWidget — displays WorkflowStatusViewModel."""

from __future__ import annotations

from textual.widgets import Static
from jarvis.presentation.viewmodels import WorkflowStatusViewModel

class WorkflowHeaderWidget(Static):
    """Passive header widget: renders WorkflowStatusViewModel.

    Displays stage, project label, and capability readiness indicators.
    """

    def update_view_model(self, status: WorkflowStatusViewModel) -> None:
        """Render the header from an immutable WorkflowStatusViewModel."""
        indicators = []
        if status.evidence_ready:
            indicators.append("[EVIDENCE]")
        if status.checkmate_ready:
            indicators.append("[CHECKMATE]")
        if status.understanding_ready:
            indicators.append("[UNDERSTANDING]")
        if status.chat_ready:
            indicators.append("[CHAT]")

        project = status.bound_project_label or "No project"
        stage_line = f"Stage: {status.stage_label}"
        project_line = f"Project: {project}"
        indicators_line = " ".join(indicators)

        text = f"╔══ {stage_line:60} {'':12} ╗\n" \
               f"║ {project_line:72s} ║\n" \
               f"║ {indicators_line:72s} ║\n" \
               f"╚══{'':70s}╝"
        self.update(text)

    def on_mount(self) -> None:
        """Initial empty render."""
        self.update("Workbench — Initializing…")