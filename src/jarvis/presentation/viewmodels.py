"""View Models for the Integrated Workbench Presentation Layer (EP-1006).

Defines immutable, pure-data view models that project domain contracts into
UI-displayable state. View models are computed by WorkbenchProjector and
consumed by concrete WorkbenchView implementations.

Per AC-6: View models project domain state into UI state. UI interactions
(filtering, selecting, expanding) MUST NEVER mutate underlying domain contracts
(FindingReport, ProjectUnderstanding, AssistantResponse).

Per AC-7: WorkbenchViewModel (presentation state) is strictly decoupled
from WorkbenchState (domain/workflow state).

Per AC-8: Given identical inputs, WorkbenchProjector always produces identical
WorkbenchViewModel instances (pure function determinism).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# =============================================================================
# FindingInspectorViewModel — Projection of Finding + UnderstandingFinding
# =============================================================================

@dataclass(frozen=True)
class FindingInspectorViewModel:
    """Presentation projection of a Finding with optional Understanding enrichment.

    Produced by WorkbenchProjector from a (Finding, UnderstandingFinding?) pair.
    Contains all UI display attributes needed by the inspector panel without
    referencing any mutable domain objects.

    Per AC-6: This is a read-only projections. UI expand/collapse toggles are
    captured as new WorkbenchViewModel instances -- never by mutating this object.

    Fields:
        finding_id:         Unique stable identifier (rule_id from Finding).
        display_title:      Human-readable title for the inspector header.
        severity_label:     Severity string (CRITICAL/MAJOR/MINOR/INFORMATIONAL).
        risk_summary:       Short risk statement text for display.
        remediation_text:   Actionable remediation guidance text.
        category_label:     Domain category label from ProjectUnderstanding (or empty).
        evidence_ids:       Ordered list of evidence_ids linked to this finding.
        is_selected:        True when this finding is the active selection.
        is_expanded:        True when the inspector row is expanded in the UI.
        has_understanding:  True when an UnderstandingFinding projection is available.
        understanding_note: Short understanding summary text (empty if none).
    """

    finding_id: str
    display_title: str
    severity_label: str
    risk_summary: str
    remediation_text: str
    category_label: str = ""
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    is_selected: bool = False
    is_expanded: bool = False
    has_understanding: bool = False
    understanding_note: str = ""

# =============================================================================
# EvidenceViewerViewModel — Projection of EvidenceReference
# =============================================================================

@dataclass(frozen=True)
class EvidenceViewerViewModel:
    """Presentation projection of an EvidenceReference for the viewer panel.

    Produced by WorkbenchProjector from an EvidenceReference domain contract.
    Carries UI rendering attributes such as highlight flags and display
    coordinates without holding a mutable reference to the domain object.

    Fields:
        evidence_id:        Unique stable identifier (evidence_id from EvidenceReference).
        document_id:        Source document identifier.
        sheet_name:         Source sheet/tab name within the document.
        source_type_label:  Human-readable source type (cell/row/section/range/computed).
        display_location:   Formatted display-ready location string (e.g. "Sheet1:A1").
        is_highlighted:     True when this evidence item is actively highlighted.
        is_selected:        True when this evidence item is the active selection.
        linked_finding_ids: Tuple of finding_ids that reference this evidence item.
        page:               Optional page number for paginated source documents.
        granularity_label:  Evidence granularity level label.
    """

    evidence_id: str
    document_id: str
    sheet_name: str
    source_type_label: str
    display_location: str
    is_highlighted: bool = False
    is_selected: bool = False
    linked_finding_ids: tuple[str, ...] = field(default_factory=tuple)
    page: int | None = None
    granularity_label: str = ""

# =============================================================================
# GroundedChatViewModel — Projection of AssistantResponse
# =============================================================================

@dataclass(frozen=True)
class GroundedChatViewModel:
    """Presentation projection of an AssistantResponse for the chat panel.

    Produced by WorkbenchProjector from an AssistantResponse domain contract.
    Renders markdown and exposes citation click targets for navigation routing.

    Fields:
        response_id:        Stable identifier (response_id from AssistantResponse).
        query_text:         The original query text that produced this response.
        rendered_markdown:  Pre-rendered markdown text for direct panel display.
        grounding_label:    Human-readable grounding status label.
        confidence_label:   Formatted confidence score string (e.g. "87%").
        citation_targets:   Mapping from citation anchor text to evidence_id for routing.
        followup_prompts:   Suggested follow-up query strings.
        is_unsupported:     True when grounding_status is UNSUPPORTED.
    """

    response_id: str
    query_text: str
    rendered_markdown: str
    grounding_label: str
    confidence_label: str
    citation_targets: dict[str, str] = field(default_factory=dict)
    followup_prompts: tuple[str, ...] = field(default_factory=tuple)
    is_unsupported: bool = False

# =============================================================================
# WorkflowStatusViewModel — Execution step indicators
# =============================================================================

@dataclass(frozen=True)
class WorkflowStatusViewModel:
    """Presentation projection of the workbench pipeline execution status.

    Produced by WorkbenchProjector from WorkbenchState.stage. Exposes
    capability readiness flags for each pipeline step so the UI can show
    progress indicators without coupling to the WorkbenchStage enum directly.

    Fields:
        stage_label:              Human-readable current stage name.
        evidence_ready:           True when evidence has been bound.
        checkmate_ready:          True when CheckMate has been executed.
        understanding_ready:      True when Project Understanding has been ingested.
        chat_ready:               True when the AI assistant is ready.
        bound_project_label:      Display name of the currently bound project (or empty).
        active_report_id_short:   First 8 chars of active_report_id for display (or empty).
    """

    stage_label: str
    evidence_ready: bool = False
    checkmate_ready: bool = False
    understanding_ready: bool = False
    chat_ready: bool = False
    bound_project_label: str = ""
    active_report_id_short: str = ""

# =============================================================================
# WorkbenchViewModel — Top-level immutable composition view model
# =============================================================================

@dataclass(frozen=True)
class WorkbenchViewModel:
    """Top-level immutable composition view model for the integrated workbench.

    WorkbenchViewModel is the root output of WorkbenchProjector. It composes
    all sub-panel view models into a single immutable snapshot that a concrete
    WorkbenchView implementation can render completely from this one object.

    Per AC-7: WorkbenchViewModel is strictly decoupled from WorkbenchState.
    Per AC-8: Identical (WorkbenchState, domain-contracts, ui-state) inputs
              always produce identical WorkbenchViewModel instances.

    Fields:
        workflow_status:        Stage and capability readiness indicators.
        findings:               Ordered tuple of FindingInspectorViewModels.
        evidence_items:         Ordered tuple of EvidenceViewerViewModels.
        chat_responses:         Ordered tuple of GroundedChatViewModels.
        active_tab:             Name of the currently active panel tab.
        filter_text:            Current filter/search text applied in the inspector.
        highlighted_evidence_ids: Set of evidence_ids that are currently highlighted.
        highlighted_finding_ids:  Set of finding_ids that are currently highlighted.
        navigation_breadcrumb:  Human-readable description of the current navigation.
        is_headless:            True when running in headless/test mode (no UI).
    """

    workflow_status: WorkflowStatusViewModel
    findings: tuple[FindingInspectorViewModel, ...] = field(default_factory=tuple)
    evidence_items: tuple[EvidenceViewerViewModel, ...] = field(default_factory=tuple)
    chat_responses: tuple[GroundedChatViewModel, ...] = field(default_factory=tuple)
    active_tab: str = "inspector"
    filter_text: str = ""
    highlighted_evidence_ids: frozenset[str] = field(default_factory=frozenset)
    highlighted_finding_ids: frozenset[str] = field(default_factory=frozenset)
    navigation_breadcrumb: str = ""
    is_headless: bool = False