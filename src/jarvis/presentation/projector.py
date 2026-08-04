"""WorkbenchProjector — Pure function projector for EP-1006.

Implements the pure-function projection:
    (WorkbenchState, DomainContracts, UIState) -> WorkbenchViewModel

Per AC-8: Given identical inputs, WorkbenchProjector ALWAYS produces
identical WorkbenchViewModel instances. The projector is a pure function
with zero side effects and zero mutable state.

Per AC-6: The projector reads domain contracts; it NEVER writes to them.
Per AC-7: WorkbenchViewModel is produced by the projector; it is strictly
          decoupled from WorkbenchState.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from jarvis.contracts.assistant import AssistantResponse, GroundingStatus
from jarvis.contracts.capabilities import EvidenceReference, Finding, FindingReport
from jarvis.contracts.understanding import ProjectUnderstanding, UnderstandingFinding
from jarvis.presentation.state import WorkbenchState, WorkbenchStage
from jarvis.presentation.viewmodels import (
    EvidenceViewerViewModel,
    FindingInspectorViewModel,
    GroundedChatViewModel,
    WorkbenchViewModel,
    WorkflowStatusViewModel,
)

# =============================================================================
# UIState — Transient UI interaction state (not domain state)
# =============================================================================

@dataclass(frozen=True)
class UIState:
    """Immutable snapshot of transient UI interaction state.

    UIState captures UI-only state that is not part of the domain/workflow
    state (WorkbenchState). It feeds the projector alongside WorkbenchState
    and domain contracts.

    Per AC-7: UIState is separate from WorkbenchState.
    Per AC-8: UIState is deterministic — same inputs produce same outputs.

    Fields:
        filter_text:           Current inspector filter string.
        active_tab:            Name of the currently active panel tab.
        expanded_finding_ids:  Set of finding_ids whose inspector rows are expanded.
        is_headless:           True in headless/test mode.
    """

    filter_text: str = ""
    active_tab: str = "inspector"
    expanded_finding_ids: frozenset[str] = field(default_factory=frozenset)
    is_headless: bool = False

# =============================================================================
# Internal projection helpers
# =============================================================================

def _stage_label(stage: WorkbenchStage) -> str:
    """Return a human-readable label for the given WorkbenchStage."""
    labels = {
        WorkbenchStage.IDLE: "Idle",
        WorkbenchStage.EVIDENCE_BOUND: "Evidence Bound",
        WorkbenchStage.CHECKMATE_EXECUTED: "CheckMate Executed",
        WorkbenchStage.UNDERSTANDING_INGESTED: "Understanding Ingested",
        WorkbenchStage.CHAT_READY: "Chat Ready",
    }
    return labels.get(stage, stage.value)

def _project_workflow_status(state: WorkbenchState) -> WorkflowStatusViewModel:
    """Project WorkbenchState into a WorkflowStatusViewModel."""
    stage = state.stage
    return WorkflowStatusViewModel(
        stage_label=_stage_label(stage),
        evidence_ready=stage not in (WorkbenchStage.IDLE,),
        checkmate_ready=stage in (
            WorkbenchStage.CHECKMATE_EXECUTED,
            WorkbenchStage.UNDERSTANDING_INGESTED,
            WorkbenchStage.CHAT_READY,
        ),
        understanding_ready=stage in (
            WorkbenchStage.UNDERSTANDING_INGESTED,
            WorkbenchStage.CHAT_READY,
        ),
        chat_ready=(stage == WorkbenchStage.CHAT_READY),
        bound_project_label=state.bound_project or "",
        active_report_id_short=(state.active_report_id or "")[:8],
    )

def _project_finding(
    finding: Finding,
    understanding_findings: list[UnderstandingFinding],
    selected_finding_id: str | None,
    expanded_finding_ids: frozenset[str],
    highlighted_finding_ids: frozenset[str],
) -> FindingInspectorViewModel:
    """Project a Finding (+ optional UnderstandingFinding) into a view model."""
    finding_id = finding.rule_id

    # Find matching UnderstandingFinding by finding_id
    u_finding: UnderstandingFinding | None = None
    for uf in understanding_findings:
        if uf.finding_id == finding_id:
            u_finding = uf
            break

    evidence_ids = tuple(ev.evidence_id for ev in finding.evidence)

    return FindingInspectorViewModel(
        finding_id=finding_id,
        display_title=f"[{finding.severity}] {finding_id}",
        severity_label=str(finding.severity),
        risk_summary=finding.risk_statement,
        remediation_text=finding.remediation,
        category_label=str(u_finding.category) if u_finding else "",
        evidence_ids=evidence_ids,
        is_selected=(finding_id == selected_finding_id),
        is_expanded=(finding_id in expanded_finding_ids),
        has_understanding=(u_finding is not None),
        understanding_note=u_finding.risk_statement if u_finding else "",
    )

def _project_evidence(
    ev_ref: EvidenceReference,
    selected_evidence_id: str | None,
    highlighted_evidence_ids: frozenset[str],
    linked_finding_ids: list[str],
) -> EvidenceViewerViewModel:
    """Project an EvidenceReference into a view model."""
    evidence_id = ev_ref.evidence_id
    page_part = f" p.{ev_ref.page}" if ev_ref.page is not None else ""
    display_location = f"{ev_ref.sheet}{page_part}"

    return EvidenceViewerViewModel(
        evidence_id=evidence_id,
        document_id=ev_ref.document_id,
        sheet_name=ev_ref.sheet,
        source_type_label=str(ev_ref.source_type),
        display_location=display_location,
        is_highlighted=(evidence_id in highlighted_evidence_ids),
        is_selected=(evidence_id == selected_evidence_id),
        linked_finding_ids=tuple(linked_finding_ids),
        page=ev_ref.page,
        granularity_label="",
    )

def _project_chat(
    response: AssistantResponse,
) -> GroundedChatViewModel:
    """Project an AssistantResponse into a GroundedChatViewModel."""
    grounding_label = str(response.grounding_status).replace("_", " ").title()
    confidence_pct = int(getattr(response, "confidence_score", 0.0) * 100)
    confidence_label = f"{confidence_pct}%"

    # Build citation_targets from cited_evidence
    citations: dict[str, str] = {}
    for ev_ref in response.cited_evidence:
        anchor = f"[{ev_ref.document_id}:{ev_ref.evidence_id}]"
        citations[anchor] = ev_ref.evidence_id

    followups = tuple(getattr(response, "suggested_followups", []))

    is_unsupported = (response.grounding_status == GroundingStatus.UNSUPPORTED)

    return GroundedChatViewModel(
        response_id=response.response_id,
        query_text=getattr(response, "query_text", ""),
        rendered_markdown=getattr(response, "response_text", ""),
        grounding_label=grounding_label,
        confidence_label=confidence_label,
        citation_targets=citations,
        followup_prompts=followups,
        is_unsupported=is_unsupported,
    )

# =============================================================================
# WorkbenchProjector — Pure function projector
# =============================================================================

class WorkbenchProjector:
    """Pure-function projector: (WorkbenchState, contracts, UIState) -> WorkbenchViewModel.

    WorkbenchProjector computes WorkbenchViewModel from three inputs:
        1. WorkbenchState    — domain/workflow stage and artifact identifiers
        2. Domain contracts  — FindingReport, ProjectUnderstanding, AssistantResponse[]
        3. UIState           — transient UI interaction state

    Per AC-8: The projector is a pure function. Given identical inputs it
    ALWAYS produces identical WorkbenchViewModel instances.
    Per AC-6: The projector NEVER mutates domain contracts.
    Per AC-7: WorkbenchViewModel is strictly decoupled from WorkbenchState.
    """

    def project(
        self,
        state: WorkbenchState,
        finding_report: FindingReport | None,
        understanding: ProjectUnderstanding | None,
        chat_responses: list[AssistantResponse] | None,
        evidence_items: list[EvidenceReference] | None,
        ui_state: UIState | None = None,
        highlighted_evidence_ids: frozenset[str] | None = None,
        highlighted_finding_ids: frozenset[str] | None = None,
    ) -> WorkbenchViewModel:
        """Compute a complete WorkbenchViewModel from current domain state.

        This is a pure function: identical arguments always produce identical
        WorkbenchViewModel instances. No side effects are permitted.

        Args:
            state:                    Current WorkbenchState (domain/workflow).
            finding_report:           Active FindingReport (or None if not executed).
            understanding:            Active ProjectUnderstanding (or None).
            chat_responses:           List of AssistantResponse contracts (or None).
            evidence_items:           List of EvidenceReference items from store.
            ui_state:                 Transient UI state (filter, tab, expansions).
            highlighted_evidence_ids: Set of evidence_ids to highlight.
            highlighted_finding_ids:  Set of finding_ids to highlight.

        Returns:
            Immutable WorkbenchViewModel computed purely from the given inputs.
        """
        if ui_state is None:
            ui_state = UIState()
        if highlighted_evidence_ids is None:
            highlighted_evidence_ids = frozenset()
        if highlighted_finding_ids is None:
            highlighted_finding_ids = frozenset()

        chat_responses = chat_responses or []
        evidence_items = evidence_items or []
        findings_list: list[Finding] = finding_report.findings if finding_report else []
        u_findings: list[UnderstandingFinding] = (
            list(understanding.findings) if understanding else []
        )

        # 1. Workflow status
        workflow_status = _project_workflow_status(state)

        # 2. Build evidence->finding index for viewer projection
        ev_to_findings: dict[str, list[str]] = {}
        for finding in findings_list:
            for ev_ref in finding.evidence:
                eid = ev_ref.evidence_id
                if eid not in ev_to_findings:
                    ev_to_findings[eid] = []
                if finding.rule_id not in ev_to_findings[eid]:
                    ev_to_findings[eid].append(finding.rule_id)

        # 3. Project findings
        projected_findings = tuple(
            _project_finding(
                finding=f,
                understanding_findings=u_findings,
                selected_finding_id=state.selected_finding_id,
                expanded_finding_ids=ui_state.expanded_finding_ids,
                highlighted_finding_ids=highlighted_finding_ids,
            )
            for f in findings_list
            if not ui_state.filter_text
            or ui_state.filter_text.lower() in f.rule_id.lower()
        )

        # 4. Project evidence items
        projected_evidence = tuple(
            _project_evidence(
                ev_ref=ev,
                selected_evidence_id=state.selected_evidence_id,
                highlighted_evidence_ids=highlighted_evidence_ids,
                linked_finding_ids=ev_to_findings.get(ev.evidence_id, []),
            )
            for ev in evidence_items
        )

        # 5. Project chat responses
        projected_chat = tuple(
            _project_chat(r) for r in chat_responses
        )

        # 6. Build navigation breadcrumb
        breadcrumb_parts = []
        if state.selected_finding_id:
            breadcrumb_parts.append(f"Finding: {state.selected_finding_id}")
        if state.selected_evidence_id:
            breadcrumb_parts.append(f"Evidence: {state.selected_evidence_id}")
        navigation_breadcrumb = " > ".join(breadcrumb_parts)

        return WorkbenchViewModel(
            workflow_status=workflow_status,
            findings=projected_findings,
            evidence_items=projected_evidence,
            chat_responses=projected_chat,
            active_tab=ui_state.active_tab,
            filter_text=ui_state.filter_text,
            highlighted_evidence_ids=highlighted_evidence_ids,
            highlighted_finding_ids=highlighted_finding_ids,
            navigation_breadcrumb=navigation_breadcrumb,
            is_headless=ui_state.is_headless,
        )