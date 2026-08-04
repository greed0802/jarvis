"""WorkbenchOrchestrator for EP-1006.

Manages the integrated workbench pipeline and acts as the composition root
for the M10.6 presentation layer. The orchestrator:

1. Holds WorkbenchState (the domain/workflow state snapshot)
2. Delegates navigation to WorkbenchNavigationRouter
3. Delegates projection to WorkbenchProjector
4. Exposes the canonical pipeline: Bind -> Validate -> Understand -> Chat -> Inspect

Per AC-1: WorkbenchOrchestrator consumes only existing public capability
          contracts and services. It does not introduce domain engines.
Per AC-5: The orchestrator executes the complete end-to-end pipeline.
Per AC-7: WorkbenchState and WorkbenchViewModel are strictly decoupled.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from jarvis.contracts.assistant import AssistantResponse
from jarvis.contracts.capabilities import EvidenceReference, FindingReport
from jarvis.contracts.understanding import ProjectUnderstanding
from jarvis.presentation.navigation import NavigationAction, NavigationIntent
from jarvis.presentation.projector import UIState, WorkbenchProjector
from jarvis.presentation.router import WorkbenchNavigationRouter
from jarvis.presentation.state import WorkbenchState, WorkbenchStage
from jarvis.presentation.viewmodels import WorkbenchViewModel

# =============================================================================
# WorkbenchOrchestrator
# =============================================================================

@dataclass
class WorkbenchOrchestrator:
    """Integrated workbench orchestrator for M10.6.

    The orchestrator is the single mutable coordinator in the EP-1006 layer.
    It owns WorkbenchState and orchestrates the full pipeline by delegating
    to existing M10.2-M10.5 capability services.

    Design:
    - WorkbenchState and WorkbenchViewModel remain strictly separate.
    - The projector is called after every state change.
    - Domain contracts are never mutated; new frozen instances always replace old.

    Per AC-1: The orchestrator references services by their public contracts;
              it does not depend on internal engine implementations.
    Per AC-5: Exposes bind_evidence, run_checkmate, ingest_understanding,
              submit_chat, and inspect methods for the complete pipeline.
    """

    # Core state — mutable across pipeline stages
    _state: WorkbenchState = field(default_factory=WorkbenchState)

    # Accumulated domain contracts
    _finding_report: FindingReport | None = field(default=None)
    _understanding: ProjectUnderstanding | None = field(default=None)
    _chat_responses: list[AssistantResponse] = field(default_factory=list)
    _evidence_items: list[EvidenceReference] = field(default_factory=list)

    # Infrastructure
    _projector: WorkbenchProjector = field(default_factory=WorkbenchProjector)
    _ui_state: UIState = field(default_factory=UIState)
    _highlighted_evidence_ids: frozenset[str] = field(default_factory=frozenset)
    _highlighted_finding_ids: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        """Initialize the router with empty indexes (rebuilt on each pipeline stage)."""
        self._router = WorkbenchNavigationRouter()

    # -------------------------------------------------------------------------
    # State accessors
    # -------------------------------------------------------------------------

    @property
    def state(self) -> WorkbenchState:
        """Return the current immutable WorkbenchState snapshot."""
        return self._state

    @property
    def current_view_model(self) -> WorkbenchViewModel:
        """Return the current WorkbenchViewModel computed from all current inputs."""
        return self._project()

    # -------------------------------------------------------------------------
    # Pipeline execution methods (AC-5)
    # -------------------------------------------------------------------------

    def bind_evidence(
        self,
        project_name: str,
        evidence_items: list[EvidenceReference],
    ) -> WorkbenchViewModel:
        """Stage 1: Bind evidence to the workbench.

        Accepts a list of EvidenceReference objects from the EvidenceRepository
        and advances the workbench to EVIDENCE_BOUND stage.

        Per AC-1: Accepts EvidenceReference public contracts only.
        Per AC-6: evidence_items are stored by reference; never mutated.

        Args:
            project_name:    Display name of the bound project/workspace.
            evidence_items:  EvidenceReference list from EvidenceRepository.

        Returns:
            New WorkbenchViewModel reflecting EVIDENCE_BOUND stage.
        """
        self._evidence_items = list(evidence_items)
        self._state = self._state.with_evidence_bound(project_name)
        self._rebuild_router()
        return self._project()

    def run_checkmate(self, finding_report: FindingReport) -> WorkbenchViewModel:
        """Stage 2: Accept CheckMate FindingReport into the workbench.

        Accepts a pre-computed FindingReport from the M10.3 validation
        pipeline and advances to CHECKMATE_EXECUTED stage.

        Per AC-1: Accepts FindingReport public contract only; does not
                  import engine internals.
        Per AC-6: finding_report is stored by reference; never mutated.

        Args:
            finding_report: The FindingReport produced by M10.3 pipeline.

        Returns:
            New WorkbenchViewModel reflecting CHECKMATE_EXECUTED stage.
        """
        self._finding_report = finding_report
        self._state = self._state.with_checkmate_executed(
            finding_report.provenance.execution_id
        )
        self._rebuild_router()
        return self._project()

    def ingest_understanding(
        self, understanding: ProjectUnderstanding
    ) -> WorkbenchViewModel:
        """Stage 3: Ingest ProjectUnderstanding into the workbench.

        Accepts a pre-computed ProjectUnderstanding (from M10.4 pipeline)
        and advances to UNDERSTANDING_INGESTED stage.

        Per AC-1: Accepts ProjectUnderstanding public contract only.

        Args:
            understanding: The ProjectUnderstanding produced by M10.4.

        Returns:
            New WorkbenchViewModel reflecting UNDERSTANDING_INGESTED stage.
        """
        self._understanding = understanding
        self._state = self._state.with_understanding_ingested()
        return self._project()

    def submit_chat(self, response: AssistantResponse) -> WorkbenchViewModel:
        """Stage 4: Accept an AssistantResponse into the workbench chat log.

        Accepts a pre-computed AssistantResponse (from M10.5 pipeline) and
        advances to CHAT_READY stage if not already there.

        Per AC-1: Accepts AssistantResponse public contract only.

        Args:
            response: The AssistantResponse produced by M10.5 assistant.

        Returns:
            New WorkbenchViewModel reflecting CHAT_READY stage.
        """
        self._chat_responses.append(response)
        self._state = self._state.with_chat_query(
            getattr(response, "query_text", "")
        ).with_chat_ready()
        self._rebuild_router()
        return self._project()

    # -------------------------------------------------------------------------
    # Navigation intent processing (router -> state -> projector)
    # -------------------------------------------------------------------------

    def apply_intent(self, intent: NavigationIntent) -> WorkbenchViewModel:
        """Apply a NavigationIntent to update WorkbenchState and re-project.

        The orchestrator is the only component permitted to mutate state.
        The router produced the intent; the projector computes the new view.

        Args:
            intent: The NavigationIntent produced by WorkbenchNavigationRouter.

        Returns:
            New WorkbenchViewModel reflecting intent application.
        """
        action = intent.action

        if action == NavigationAction.SELECT_EVIDENCE:
            self._state = self._state.with_evidence_selected(intent.target_id)
            # Highlight linked findings
            linked_ids_str = intent.metadata.get("linked_finding_ids", "")
            if linked_ids_str:
                self._highlighted_finding_ids = frozenset(linked_ids_str.split(","))
            else:
                self._highlighted_finding_ids = frozenset()
            self._highlighted_evidence_ids = frozenset([intent.target_id])

        elif action == NavigationAction.SELECT_FINDING:
            self._state = self._state.with_finding_selected(intent.target_id)
            linked_ids_str = intent.metadata.get("linked_evidence_ids", "")
            if linked_ids_str:
                self._highlighted_evidence_ids = frozenset(linked_ids_str.split(","))
            else:
                self._highlighted_evidence_ids = frozenset()
            self._highlighted_finding_ids = frozenset([intent.target_id])

        elif action == NavigationAction.NAVIGATE_CITATION:
            self._state = self._state.with_evidence_selected(intent.target_id)
            self._highlighted_evidence_ids = frozenset([intent.target_id])
            linked_ids_str = intent.metadata.get("linked_finding_ids", "")
            if linked_ids_str:
                self._highlighted_finding_ids = frozenset(linked_ids_str.split(","))
            else:
                self._highlighted_finding_ids = frozenset()

        elif action == NavigationAction.CLEAR_SELECTION:
            self._state = self._state.cleared()
            self._highlighted_evidence_ids = frozenset()
            self._highlighted_finding_ids = frozenset()

        return self._project()

    # -------------------------------------------------------------------------
    # UserInteractionSink interface implementation
    # -------------------------------------------------------------------------

    def on_select_evidence(self, evidence_id: str) -> None:
        """Dispatch an evidence selection gesture (UserInteractionSink impl)."""
        intent = self._router.route_evidence_click(evidence_id)
        self.apply_intent(intent)

    def on_select_finding(self, finding_id: str) -> None:
        """Dispatch a finding selection gesture (UserInteractionSink impl)."""
        intent = self._router.route_finding_click(finding_id)
        self.apply_intent(intent)

    def on_navigate_citation(self, citation_id: str) -> None:
        """Dispatch a citation navigation gesture (UserInteractionSink impl)."""
        intent = self._router.route_citation_click(citation_id)
        self.apply_intent(intent)

    def on_submit_chat(self, query_text: str) -> None:
        """Dispatch a chat query - placeholder (response comes from service)."""
        self._state = self._state.with_chat_query(query_text)

    def on_clear_selection(self) -> None:
        """Dispatch a selection-clear gesture (UserInteractionSink impl)."""
        intent = self._router.route_clear()
        self.apply_intent(intent)

    # -------------------------------------------------------------------------
    # Inspect helper (Stage 5 of the pipeline)
    # -------------------------------------------------------------------------

    def inspect_finding(self, finding_id: str) -> WorkbenchViewModel:
        """Stage 5: Inspect a specific finding (navigate to it)."""
        intent = self._router.route_finding_click(finding_id)
        return self.apply_intent(intent)

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------

    def _rebuild_router(self) -> None:
        """Rebuild the navigation router from current domain contracts."""
        findings = self._finding_report.findings if self._finding_report else []
        u_findings = list(self._understanding.findings) if self._understanding else []
        self._router = WorkbenchNavigationRouter(
            findings=findings,
            evidence_items=self._evidence_items,
            understanding_findings=u_findings,
            chat_responses=list(self._chat_responses),
        )

    def _project(self) -> WorkbenchViewModel:
        """Invoke the projector with all current state/contracts."""
        return self._projector.project(
            state=self._state,
            finding_report=self._finding_report,
            understanding=self._understanding,
            chat_responses=list(self._chat_responses),
            evidence_items=self._evidence_items,
            ui_state=self._ui_state,
            highlighted_evidence_ids=self._highlighted_evidence_ids,
            highlighted_finding_ids=self._highlighted_finding_ids,
        )
