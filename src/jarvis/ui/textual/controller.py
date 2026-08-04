"""InteractionController — maps Textual events to UserInteractionSink calls."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jarvis.ui.textual.sink import TextualInteractionSink
    from jarvis.presentation.viewmodels import WorkbenchViewModel


class InteractionController:
    """Mediates between Textual UI widgets and the interaction sink.

    Receives raw widget events (selections, submissions, keypresses) and
    maps them to typed calls on TextualInteractionSink.
    """

    def __init__(self, sink: TextualInteractionSink) -> None:
        self._sink = sink
        self._current_view_model: WorkbenchViewModel | None = None

    # -- Widget event handlers --

    def on_inspector_item_selected(self, finding_id: str) -> None:
        """A finding was selected in the inspector widget."""
        self._sink.on_select_finding(finding_id)

    def on_evidence_item_selected(self, evidence_id: str) -> None:
        """An evidence item was selected in the evidence viewer."""
        self._sink.on_select_evidence(evidence_id)

    def on_citation_clicked(self, citation_id: str) -> None:
        """A citation was clicked in the chat widget."""
        self._sink.on_navigate_citation(citation_id)

    def on_chat_submitted(self, query_text: str) -> None:
        """A chat query was submitted."""
        self._sink.on_submit_chat(query_text)

    def on_clear_selection(self) -> None:
        """Selection was cleared."""
        self._sink.on_clear_selection()

    # -- View model tracking for deterministic updates --

    def set_view_model(self, view_model: WorkbenchViewModel) -> None:
        """Set the latest view model (used for widget updates)."""
        self._current_view_model = view_model

    @property
    def current_view_model(self) -> WorkbenchViewModel | None:
        return self._current_view_model