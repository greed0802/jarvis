"""WorkbenchState — Immutable domain/workflow state for EP-1006.

Represents the execution stage of the integrated workbench pipeline and the
identifiers of active domain artifacts. WorkbenchState is the *domain* state;
it is strictly decoupled from WorkbenchViewModel (the *presentation* state).

Per AC-7: WorkbenchState and WorkbenchViewModel are strictly separate types.
Per AC-6: State transitions produce new WorkbenchState instances; the
          underlying domain contracts (FindingReport, etc.) are never mutated.

Architecture:
    WorkbenchOrchestrator owns WorkbenchState.
    WorkbenchProjector reads WorkbenchState (never writes).
    WorkbenchViewModel is computed from WorkbenchState by WorkbenchProjector.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

# =============================================================================
# WorkbenchStage — Deterministic pipeline stage vocabulary
# =============================================================================

class WorkbenchStage(Enum):
    """Deterministic execution stage of the workbench pipeline.

    Stages progress strictly forward: IDLE -> EVIDENCE_BOUND ->
    CHECKMATE_EXECUTED -> UNDERSTANDING_INGESTED -> CHAT_READY.

    Each stage unlocks additional capabilities in the workbench:
    - IDLE:                   No evidence bound; no capabilities active.
    - EVIDENCE_BOUND:         Evidence store populated; CheckMate can run.
    - CHECKMATE_EXECUTED:     FindingReport produced; Understanding can ingest.
    - UNDERSTANDING_INGESTED: ProjectUnderstanding produced; Chat can respond.
    - CHAT_READY:             Assistant ready; full workbench available.
    """

    IDLE = "idle"
    EVIDENCE_BOUND = "evidence_bound"
    CHECKMATE_EXECUTED = "checkmate_executed"
    UNDERSTANDING_INGESTED = "understanding_ingested"
    CHAT_READY = "chat_ready"

# =============================================================================
# WorkbenchState — Immutable snapshot of domain/workflow execution state
# =============================================================================

@dataclass(frozen=True)
class WorkbenchState:
    """Immutable snapshot of the integrated workbench's domain/workflow state.

    WorkbenchState captures the execution stage, bound project context, and
    the identifiers of active domain artifacts (report, finding, evidence).

    This is the *domain state* passed to WorkbenchProjector. It contains
    identifiers and references to domain contracts -- it does NOT contain
    UI-specific state such as scroll positions, filter text, or sort order.

    Per AC-7: WorkbenchState is strictly decoupled from WorkbenchViewModel.
    The projector reads WorkbenchState; it never mutates it.

    Fields:
        stage:                The current execution stage of the workbench pipeline.
        bound_project:        Optional identifier for the bound project/workspace.
        active_report_id:     Optional execution_id of the active FindingReport.
        selected_finding_id:  Optional rule_id of the currently selected Finding.
        selected_evidence_id: Optional evidence_id of the selected EvidenceReference.
        chat_query_context:   Optional last chat query string for presentation context.
    """

    stage: WorkbenchStage = WorkbenchStage.IDLE
    bound_project: str | None = None
    active_report_id: str | None = None
    selected_finding_id: str | None = None
    selected_evidence_id: str | None = None
    chat_query_context: str | None = None

    # -------------------------------------------------------------------------
    # State transition helpers — each returns a new frozen WorkbenchState.
    # Domain contracts (FindingReport etc.) are NEVER mutated by transitions.
    # -------------------------------------------------------------------------

    def with_evidence_bound(self, project: str) -> WorkbenchState:
        """Return a new state reflecting evidence binding completion."""
        return WorkbenchState(
            stage=WorkbenchStage.EVIDENCE_BOUND,
            bound_project=project,
            active_report_id=self.active_report_id,
            selected_finding_id=self.selected_finding_id,
            selected_evidence_id=self.selected_evidence_id,
            chat_query_context=self.chat_query_context,
        )

    def with_checkmate_executed(self, report_id: str) -> WorkbenchState:
        """Return a new state reflecting CheckMate execution completion."""
        return WorkbenchState(
            stage=WorkbenchStage.CHECKMATE_EXECUTED,
            bound_project=self.bound_project,
            active_report_id=report_id,
            selected_finding_id=self.selected_finding_id,
            selected_evidence_id=self.selected_evidence_id,
            chat_query_context=self.chat_query_context,
        )

    def with_understanding_ingested(self) -> WorkbenchState:
        """Return a new state reflecting understanding ingestion completion."""
        return WorkbenchState(
            stage=WorkbenchStage.UNDERSTANDING_INGESTED,
            bound_project=self.bound_project,
            active_report_id=self.active_report_id,
            selected_finding_id=self.selected_finding_id,
            selected_evidence_id=self.selected_evidence_id,
            chat_query_context=self.chat_query_context,
        )

    def with_chat_ready(self) -> WorkbenchState:
        """Return a new state reflecting assistant chat readiness."""
        return WorkbenchState(
            stage=WorkbenchStage.CHAT_READY,
            bound_project=self.bound_project,
            active_report_id=self.active_report_id,
            selected_finding_id=self.selected_finding_id,
            selected_evidence_id=self.selected_evidence_id,
            chat_query_context=self.chat_query_context,
        )

    def with_finding_selected(self, finding_id: str) -> WorkbenchState:
        """Return a new state with the specified finding selected."""
        return WorkbenchState(
            stage=self.stage,
            bound_project=self.bound_project,
            active_report_id=self.active_report_id,
            selected_finding_id=finding_id,
            selected_evidence_id=self.selected_evidence_id,
            chat_query_context=self.chat_query_context,
        )

    def with_evidence_selected(self, evidence_id: str) -> WorkbenchState:
        """Return a new state with the specified evidence item selected."""
        return WorkbenchState(
            stage=self.stage,
            bound_project=self.bound_project,
            active_report_id=self.active_report_id,
            selected_finding_id=self.selected_finding_id,
            selected_evidence_id=evidence_id,
            chat_query_context=self.chat_query_context,
        )

    def with_chat_query(self, query: str) -> WorkbenchState:
        """Return a new state capturing the chat query context string."""
        return WorkbenchState(
            stage=self.stage,
            bound_project=self.bound_project,
            active_report_id=self.active_report_id,
            selected_finding_id=self.selected_finding_id,
            selected_evidence_id=self.selected_evidence_id,
            chat_query_context=query,
        )

    def cleared(self) -> WorkbenchState:
        """Return a new state with all selections cleared (preserves stage)."""
        return WorkbenchState(
            stage=self.stage,
            bound_project=self.bound_project,
            active_report_id=self.active_report_id,
            selected_finding_id=None,
            selected_evidence_id=None,
            chat_query_context=self.chat_query_context,
        )