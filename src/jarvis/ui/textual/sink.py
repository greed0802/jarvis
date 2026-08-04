"""TextualInteractionSink — implements UserInteractionSink protocol for Textual TUI.

Dispatches user gestures to the WorkbenchOrchestrator.
"""

from __future__ import annotations

from jarvis.presentation.workbench import WorkbenchOrchestrator


class TextualInteractionSink:
    """Implements UserInteractionSink protocol for the Textual TUI.

    Delegates platform events to WorkbenchOrchestrator.
    Zero business logic — pure dispatch.
    """

    def __init__(self, orchestrator: WorkbenchOrchestrator) -> None:
        self._orchestrator = orchestrator

    def on_select_evidence(self, evidence_id: str) -> None:
        self._orchestrator.on_select_evidence(evidence_id)

    def on_select_finding(self, finding_id: str) -> None:
        self._orchestrator.on_select_finding(finding_id)

    def on_navigate_citation(self, citation_id: str) -> None:
        self._orchestrator.on_navigate_citation(citation_id)

    def on_submit_chat(self, query_text: str) -> None:
        self._orchestrator.on_submit_chat(query_text)

    def on_clear_selection(self) -> None:
        self._orchestrator.on_clear_selection()