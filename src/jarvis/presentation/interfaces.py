"""Toolkit-agnostic presentation protocols for EP-1006.

Defines the abstract Protocol interfaces that decouple the workbench
presentation contracts from any concrete UI framework.

Per AC-2: EP-1006 MUST NOT import any concrete UI framework. All UI surfaces
          are defined as Python Protocol interfaces in this module.

Concrete implementations belong to M10.7+ milestone capability builds.

Architecture:
    WorkbenchView    — protocol for rendering a WorkbenchViewModel
    UserInteractionSink — protocol for dispatching raw user gestures
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jarvis.presentation.viewmodels import WorkbenchViewModel

# =============================================================================
# WorkbenchView — Abstract rendering surface
# =============================================================================

@runtime_checkable
class WorkbenchView(Protocol):
    """Abstract rendering surface for the integrated workbench.

    Implementors receive a complete WorkbenchViewModel and are responsible
    for rendering all panels from that immutable snapshot. Headless
    implementations satisfy this protocol for testing without any
    dependency on domain contracts.

    Per AC-2: No concrete UI framework imports are permitted in this module.

    Methods:
        render(view_model): Render the complete workbench from the given view model.
        set_headless(enabled): Switch rendering to headless (no-op) mode for testing.
    """

    def render(self, view_model: WorkbenchViewModel) -> None:
        """Render the complete workbench from the given immutable view model.

        Args:
            view_model: The complete WorkbenchViewModel computed by WorkbenchProjector.
                        Implementations render all sub-panels from this single object.

        Raises:
            NotImplementedError: when the concrete view does not implement rendering.
        """
        ...

    def set_headless(self, enabled: bool) -> None:
        """Enable or disable headless mode.

        When headless is True, render() becomes a no-op. Used in tests and
        automated scenarios where no visual output is desired.
        """
        ...

# =============================================================================
# UserInteractionSink — Abstract user gesture dispatcher
# =============================================================================

@runtime_checkable
class UserInteractionSink(Protocol):
    """Abstract dispatcher for raw user gestures from any UI panel.

    Implementors dispatch user gestures as typed calls to the workbench
    orchestrator. The orchestrator routes each gesture through
    WorkbenchNavigationRouter to produce a NavigationIntent, then updates
    WorkbenchState and re-projects the WorkbenchViewModel.

    Per AC-2: No concrete UI framework imports are permitted in this module.
    Per AC-7: This interface captures gestures; it does NOT modify state directly.

    Methods:
        on_select_evidence(evidence_id):      User clicked/selected an evidence item.
        on_select_finding(finding_id):        User clicked/selected a finding row.
        on_navigate_citation(citation_id):    User clicked a grounded citation link.
        on_submit_chat(query_text):           User submitted a chat query.
        on_clear_selection():                 User cleared all active selections.
    """

    def on_select_evidence(self, evidence_id: str) -> None:
        """Dispatch an evidence selection gesture.

        Args:
            evidence_id: The evidence_id of the EvidenceReference that was selected.
        """
        ...

    def on_select_finding(self, finding_id: str) -> None:
        """Dispatch a finding selection gesture.

        Args:
            finding_id: The rule_id of the Finding that was selected in the inspector.
        """
        ...

    def on_navigate_citation(self, citation_id: str) -> None:
        """Dispatch a citation navigation gesture from the chat panel.

        Args:
            citation_id: The evidence_id referenced by the clicked citation anchor.
        """
        ...

    def on_submit_chat(self, query_text: str) -> None:
        """Dispatch a chat query submission gesture.

        Args:
            query_text: The raw text query submitted by the user.
        """
        ...

    def on_clear_selection(self) -> None:
        """Dispatch a selection-clear gesture (deselect all)."""
        ...