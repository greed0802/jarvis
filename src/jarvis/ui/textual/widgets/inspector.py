"""FindingInspectorWidget — renders FindingInspectorViewModel list."""

from __future__ import annotations

from textual.widgets import ListView, ListItem

from jarvis.presentation.viewmodels import FindingInspectorViewModel

class FindingInspectorWidget(ListView):
    """Passive list widget: renders FindingInspectorViewModel items.

    Each item displays severity, display_title, and selection state.
    """

    def update_view_model(self, findings: tuple[FindingInspectorViewModel, ...]) -> None:
        """Render findings from an immutable view model list."""
        self.clear()
        if not findings:
            self.append(ListItem("No findings to display."))
            return
        for finding in findings:
            prefix = "▶ " if finding.is_selected else "  "
            hl = "✱ " if finding.is_selected else ""
            title = finding.display_title
            text = f"{prefix}{hl}{finding.severity_label} | {title}"
            self.append(ListItem(text))