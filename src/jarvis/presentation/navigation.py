"""Navigation contracts for the Integrated Workbench Presentation Layer (EP-1006).

Defines the strongly-typed NavigationIntent model that decouples raw user
gestures from domain state mutations. The router produces NavigationIntent
objects; the WorkbenchOrchestrator consumes them.

Architecture:
    User Gesture → UserInteractionSink → NavigationIntent → WorkbenchOrchestrator
                                                              → WorkbenchProjector
                                                              → WorkbenchViewModel
                                                              → WorkbenchView.render()

Per AC-2: No concrete UI framework dependencies.
Per AC-7: Navigation is decoupled from WorkbenchState mutation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

# =============================================================================
# NavigationAction — Typed action vocabulary
# =============================================================================

class NavigationAction(Enum):
    """Strongly-typed vocabulary of workbench navigation actions.

    Each value represents a distinct, deterministic navigation event that can
    be produced by user interaction in any panel.
    """

    SELECT_EVIDENCE = "select_evidence"
    """User selected a specific EvidenceReference in any panel."""

    SELECT_FINDING = "select_finding"
    """User selected a specific Finding in the inspector panel."""

    NAVIGATE_CITATION = "navigate_citation"
    """User activated a grounded citation link in the chat panel."""

    CLEAR_SELECTION = "clear_selection"
    """User cleared the active selection (deselect)."""

# =============================================================================
# NavigationOrigin — Source panel vocabulary
# =============================================================================

class NavigationOrigin(Enum):
    """Identifies which UI panel originated a navigation action.

    This allows the router to apply bidirectional routing logic based on the
    source context of the navigation.
    """

    INSPECTOR = "inspector"
    """Action originated from the Finding Inspector panel."""

    EVIDENCE_VIEWER = "evidence_viewer"
    """Action originated from the Evidence Viewer panel."""

    GROUNDED_CHAT = "grounded_chat"
    """Action originated from the Grounded Chat panel (citation click)."""

# =============================================================================
# NavigationIntent — Immutable navigation command
# =============================================================================

@dataclass(frozen=True)
class NavigationIntent:
    """Immutable, strongly-typed navigation directive produced by the router.

    A NavigationIntent represents a complete, self-describing navigation event.
    It carries the action type, the target identifier, the source panel origin,
    and optional string metadata for extended context.

    The router produces NavigationIntent objects.
    The WorkbenchOrchestrator consumes NavigationIntent objects to update
    WorkbenchState and invoke WorkbenchProjector.

    The NavigationIntent MUST NOT be mutated after construction.
    The router MUST NOT apply state changes directly.

    Fields:
        action: The strongly-typed navigation action to perform.
        target_id: The unique identifier of the navigation target (evidence_id,
                   finding_id, or citation reference).
        origin: The panel that originated this navigation action.
        metadata: Optional string key-value pairs for extended routing context
                  (e.g., highlight offsets, scroll positions, filter hints).
    """

    action: NavigationAction
    target_id: str
    origin: NavigationOrigin
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate NavigationIntent invariants after construction."""
        if not self.target_id and self.action != NavigationAction.CLEAR_SELECTION:
            raise ValueError(
                f"NavigationIntent.target_id must not be empty for action={self.action!r}"
            )