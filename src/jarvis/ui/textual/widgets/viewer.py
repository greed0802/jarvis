"""EvidenceViewerWidget — renders EvidenceViewerViewModel list."""

from __future__ import annotations

from textual.widgets import ListView, ListItem

from jarvis.presentation.viewmodels import EvidenceViewerViewModel

class EvidenceViewerWidget(ListView):
    """Passive list widget: renders EvidenceViewerViewModel items."""

    def update_view_model(self, items: tuple[EvidenceViewerViewModel, ...]) -> None:
        """Render evidence items from an immutable view model list."""
        self.clear()
        if not items:
            self.append(ListItem("No evidence to display."))
            return
        for ev in items:
            prefix = "▶ " if ev.is_selected else "  "
            hl = "✱ " if ev.is_highlighted else ""
            loc = ev.display_location
            text = f"{prefix}{hl}{ev.document_id} | {ev.sheet_name} | {loc}"
            self.append(ListItem(text))