"""EP-1006: Integrated Workbench Presentation Layer (M10.6).

Provides the toolkit-agnostic presentation architecture that composes
existing M10.2-M10.5 domain capabilities into a unified workbench.

Public API:
    Navigation:
        NavigationAction, NavigationOrigin, NavigationIntent

    State:
        WorkbenchStage, WorkbenchState

    View Models:
        FindingInspectorViewModel, EvidenceViewerViewModel,
        GroundedChatViewModel, WorkflowStatusViewModel, WorkbenchViewModel

    Interfaces (Protocols):
        WorkbenchView, UserInteractionSink

    Router:
        WorkbenchNavigationRouter

    Projector:
        WorkbenchProjector, UIState

    Orchestrator:
        WorkbenchOrchestrator
"""

from jarvis.presentation.navigation import NavigationAction, NavigationIntent, NavigationOrigin
from jarvis.presentation.state import WorkbenchStage, WorkbenchState
from jarvis.presentation.viewmodels import (
    EvidenceViewerViewModel,
    FindingInspectorViewModel,
    GroundedChatViewModel,
    WorkbenchViewModel,
    WorkflowStatusViewModel,
)
from jarvis.presentation.interfaces import UserInteractionSink, WorkbenchView
from jarvis.presentation.router import WorkbenchNavigationRouter
from jarvis.presentation.projector import UIState, WorkbenchProjector
from jarvis.presentation.workbench import WorkbenchOrchestrator

__all__ = [
    # Navigation
    "NavigationAction",
    "NavigationOrigin",
    "NavigationIntent",
    # State
    "WorkbenchStage",
    "WorkbenchState",
    # View Models
    "FindingInspectorViewModel",
    "EvidenceViewerViewModel",
    "GroundedChatViewModel",
    "WorkflowStatusViewModel",
    "WorkbenchViewModel",
    # Interfaces
    "WorkbenchView",
    "UserInteractionSink",
    # Router
    "WorkbenchNavigationRouter",
    # Projector
    "UIState",
    "WorkbenchProjector",
    # Orchestrator
    "WorkbenchOrchestrator",
]