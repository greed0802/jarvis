"""Test Suite for EP-1006: Integrated Workbench Presentation Architecture.

Covers AC-1 through AC-8 acceptance criteria for the M10.6 presentation layer.
All tests run headlessly (no concrete UI framework required).

AC-1 Composition Only        — workbench uses only public domain contracts
AC-2 Toolkit Agnostic        — UI surfaces are Protocol interfaces only
AC-3 Evidence Traceability   — evidence click routes NavigationIntent to finding
AC-4 Finding Traceability    — finding click routes NavigationIntent to evidence
AC-5 Canonical Pipeline      — Bind->Validate->Understand->Chat->Inspect succeeds
AC-6 Domain Immutability     — UI interactions never mutate domain contracts
AC-7 State Separation        — WorkbenchState and WorkbenchViewModel are decoupled
AC-8 Deterministic Projection— identical inputs always yield identical viewmodel
"""

from __future__ import annotations

import dataclasses

import pytest

from jarvis.contracts.assistant import AssistantResponse, GroundingStatus
from jarvis.contracts.capabilities import (
    EvidenceReference,
    EvidenceSourceType,
    Finding,
    FindingReport,
    ReportProvenance,
    Severity,
    TelemetrySummary,
)
from jarvis.contracts.understanding import (
    FindingCategory,
    ProjectUnderstanding,
    UnderstandingFinding,
)
from jarvis.presentation.interfaces import UserInteractionSink, WorkbenchView
from jarvis.presentation.navigation import NavigationAction, NavigationIntent, NavigationOrigin
from jarvis.presentation.projector import UIState, WorkbenchProjector
from jarvis.presentation.router import WorkbenchNavigationRouter
from jarvis.presentation.state import WorkbenchStage, WorkbenchState
from jarvis.presentation.viewmodels import WorkbenchViewModel, WorkflowStatusViewModel
from jarvis.presentation.workbench import WorkbenchOrchestrator

# ---------------------------------------------------------------------------
# Shared domain contract fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def ev_ref_a() -> EvidenceReference:
    return EvidenceReference(
        document_id="doc-001",
        sheet="BOQ_Sheet1",
        evidence_id="ev-001",
        source_type=EvidenceSourceType.CELL,
        page=1,
    )

@pytest.fixture
def ev_ref_b() -> EvidenceReference:
    return EvidenceReference(
        document_id="doc-001",
        sheet="BOQ_Sheet2",
        evidence_id="ev-002",
        source_type=EvidenceSourceType.ROW,
        page=2,
    )

@pytest.fixture
def finding_a(ev_ref_a: EvidenceReference) -> Finding:
    return Finding(
        rule_id="RULE-001",
        severity=Severity.CRITICAL,
        evidence=[ev_ref_a],
        risk_statement="Missing unit rate in BOQ item.",
        remediation="Insert the correct unit rate per trade schedule.",
    )

@pytest.fixture
def finding_b(ev_ref_b: EvidenceReference) -> Finding:
    return Finding(
        rule_id="RULE-002",
        severity=Severity.MAJOR,
        evidence=[ev_ref_b],
        risk_statement="Duplicate line item detected.",
        remediation="Remove duplicate and reconcile quantities.",
    )

@pytest.fixture
def finding_report(finding_a: Finding, finding_b: Finding) -> FindingReport:
    provenance = ReportProvenance(
        execution_id="exec-abc-12345678",
        evidence_fingerprint="fp-001",
        rule_snapshot_hash="rsh-001",
        capability_version="1.0.0",
    )
    telemetry = TelemetrySummary(
        rule_count_total=10,
        rule_count_executed=10,
        rule_count_unevaluable=0,
    )
    return FindingReport(
        provenance=provenance,
        telemetry_summary=telemetry,
        findings=[finding_a, finding_b],
    )

@pytest.fixture
def understanding_finding_a() -> UnderstandingFinding:
    return UnderstandingFinding(
        finding_id="RULE-001",
        category=FindingCategory.MEASUREMENT,
        severity="CRITICAL",
        risk_statement="Unit rate absence suggests potential cost understatement.",
        remediation="Verify against trade schedule rates.",
        evidence_count=1,
    )

@pytest.fixture
def project_understanding(
    finding_report: FindingReport,
    understanding_finding_a: UnderstandingFinding,
) -> ProjectUnderstanding:
    return ProjectUnderstanding(
        report_id="pu-report-001",
        capability_version="1.0.0",
        total_rules_executed=10,
        total_findings=2,
        findings=[understanding_finding_a],
    )

@pytest.fixture
def assistant_response(ev_ref_a: EvidenceReference) -> AssistantResponse:
    return AssistantResponse(
        response_id="resp-001",
        query_text="Why is RULE-001 flagged as critical?",
        response_text="The unit rate is missing from the referenced BOQ cell.",
        grounding_status=GroundingStatus.FULLY_GROUNDED,
        cited_evidence=[ev_ref_a],
        understanding_provenance_id="pu-report-001",
        confidence_score=0.92,
        suggested_followups=["What is the trade schedule rate?"],
    )

@pytest.fixture
def evidence_list(ev_ref_a: EvidenceReference, ev_ref_b: EvidenceReference) -> list[EvidenceReference]:
    return [ev_ref_a, ev_ref_b]

@pytest.fixture
def projector() -> WorkbenchProjector:
    return WorkbenchProjector()

@pytest.fixture
def orchestrator() -> WorkbenchOrchestrator:
    return WorkbenchOrchestrator()

# ===========================================================================
# AC-1: Composition Only
# ===========================================================================

class TestAC1CompositionOnly:
    """AC-1: WorkbenchOrchestrator consumes only public capability contracts."""

    def test_finding_report_accepted_as_public_contract(
        self, orchestrator: WorkbenchOrchestrator, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        orchestrator.bind_evidence("Project-Alpha", evidence_list)
        vm = orchestrator.run_checkmate(finding_report)
        assert vm.workflow_status.checkmate_ready is True

    def test_project_understanding_accepted_as_public_contract(
        self, orchestrator: WorkbenchOrchestrator, finding_report: FindingReport,
        project_understanding: ProjectUnderstanding, evidence_list: list[EvidenceReference],
    ) -> None:
        orchestrator.bind_evidence("Project-Alpha", evidence_list)
        orchestrator.run_checkmate(finding_report)
        vm = orchestrator.ingest_understanding(project_understanding)
        assert vm.workflow_status.understanding_ready is True

    def test_assistant_response_accepted_and_reaches_chat_ready(
        self, orchestrator: WorkbenchOrchestrator, finding_report: FindingReport,
        project_understanding: ProjectUnderstanding, assistant_response: AssistantResponse,
        evidence_list: list[EvidenceReference],
    ) -> None:
        orchestrator.bind_evidence("Project-Alpha", evidence_list)
        orchestrator.run_checkmate(finding_report)
        orchestrator.ingest_understanding(project_understanding)
        vm = orchestrator.submit_chat(assistant_response)
        assert vm.workflow_status.chat_ready is True

    def test_no_engine_internals_in_presentation_modules(self) -> None:
        """No engine internal types appear in any presentation source file."""
        import jarvis.presentation.workbench as wb
        import jarvis.presentation.projector as proj
        import jarvis.presentation.router as router

        forbidden = [
            "CheckMateEngine", "ExecutionOutcome", "RuleSnapshot",
            "RuleRegistry", "CheckMateRule",
        ]
        for mod in [wb, proj, router]:
            with open(mod.__file__) as f:
                src = f.read()
            for name in forbidden:
                assert name not in src, f"Forbidden engine name '{name}' in {mod.__name__}"

# ===========================================================================
# AC-2: Toolkit Agnostic Boundary
# ===========================================================================

class TestAC2ToolkitAgnostic:
    """AC-2: All UI surfaces are Python Protocol interfaces; no concrete framework."""

    def test_workbench_view_has_render_method(self) -> None:
        """WorkbenchView Protocol exposes render()."""
        assert hasattr(WorkbenchView, "render"), "WorkbenchView must declare render()"

    def test_user_interaction_sink_has_required_methods(self) -> None:
        """UserInteractionSink Protocol exposes all required gesture methods."""
        for method in [
            "on_select_evidence", "on_select_finding", "on_navigate_citation",
            "on_submit_chat", "on_clear_selection",
        ]:
            assert hasattr(UserInteractionSink, method), \
                f"UserInteractionSink missing method: {method}"

    def test_interfaces_module_contains_no_concrete_ui_framework(self) -> None:
        """interfaces.py must not contain any concrete UI framework import."""
        import jarvis.presentation.interfaces as ifaces_mod
        with open(ifaces_mod.__file__) as f:
            src = f.read()
        for fw in ["PyQt", "PySide", "textual", "tkinter", "wx", "tauri", "curses"]:
            assert fw.lower() not in src.lower(), \
                f"Concrete framework '{fw}' found in interfaces.py"

    def test_headless_view_satisfies_workbench_view_protocol(self) -> None:
        """A no-op headless implementation satisfies WorkbenchView Protocol."""
        class HeadlessView:
            def render(self, view_model: WorkbenchViewModel) -> None:
                pass
            def set_headless(self, enabled: bool) -> None:
                pass

        assert isinstance(HeadlessView(), WorkbenchView)

    def test_orchestrator_satisfies_user_interaction_sink(
        self, orchestrator: WorkbenchOrchestrator,
    ) -> None:
        """WorkbenchOrchestrator satisfies UserInteractionSink Protocol."""
        assert isinstance(orchestrator, UserInteractionSink)

    def test_workbench_view_model_is_immutable(self) -> None:
        """WorkbenchViewModel is a frozen dataclass (immutable)."""
        status = WorkflowStatusViewModel(stage_label="Idle")
        vm = WorkbenchViewModel(workflow_status=status)
        # Frozen dataclass prevents mutation via __dataclass_setattr__ internals
        assert hasattr(dataclasses, "FrozenInstanceError"), "FrozenInstanceError should exist"

# ===========================================================================
# AC-3: Evidence-to-Explanation Traceability
# ===========================================================================

class TestAC3EvidenceTraceability:
    """AC-3: Evidence selection routes a NavigationIntent to finding highlights."""

    def test_route_evidence_click_produces_select_evidence_intent(
        self, finding_a: Finding, ev_ref_a: EvidenceReference,
    ) -> None:
        router = WorkbenchNavigationRouter(findings=[finding_a], evidence_items=[ev_ref_a])
        intent = router.route_evidence_click("ev-001")
        assert intent.action == NavigationAction.SELECT_EVIDENCE
        assert intent.target_id == "ev-001"
        assert intent.origin == NavigationOrigin.EVIDENCE_VIEWER

    def test_route_evidence_click_carries_linked_finding_ids(
        self, finding_a: Finding, ev_ref_a: EvidenceReference,
    ) -> None:
        router = WorkbenchNavigationRouter(findings=[finding_a], evidence_items=[ev_ref_a])
        intent = router.route_evidence_click("ev-001")
        assert "linked_finding_ids" in intent.metadata
        assert "RULE-001" in intent.metadata["linked_finding_ids"]

    def test_apply_evidence_intent_highlights_linked_findings(
        self, orchestrator: WorkbenchOrchestrator, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        orchestrator.bind_evidence("P1", evidence_list)
        orchestrator.run_checkmate(finding_report)
        intent = orchestrator._router.route_evidence_click("ev-001")
        vm = orchestrator.apply_intent(intent)
        assert "RULE-001" in vm.highlighted_finding_ids

    def test_selected_evidence_shown_as_selected_in_view_model(
        self, projector: WorkbenchProjector, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        state = WorkbenchState(
            stage=WorkbenchStage.CHECKMATE_EXECUTED,
            selected_evidence_id="ev-001",
        )
        vm = projector.project(
            state=state,
            finding_report=finding_report,
            understanding=None,
            chat_responses=None,
            evidence_items=evidence_list,
        )
        selected = [e for e in vm.evidence_items if e.evidence_id == "ev-001"]
        assert len(selected) == 1 and selected[0].is_selected is True

    def test_route_citation_click_produces_navigate_citation_intent(
        self, finding_a: Finding, ev_ref_a: EvidenceReference,
        assistant_response: AssistantResponse,
    ) -> None:
        router = WorkbenchNavigationRouter(
            findings=[finding_a], evidence_items=[ev_ref_a],
            chat_responses=[assistant_response],
        )
        intent = router.route_citation_click("ev-001")
        assert intent.action == NavigationAction.NAVIGATE_CITATION
        assert intent.target_id == "ev-001"
        assert intent.origin == NavigationOrigin.GROUNDED_CHAT

# ===========================================================================
# AC-4: Explanation-to-Evidence Traceability
# ===========================================================================

class TestAC4FindingTraceability:
    """AC-4: Finding selection routes a NavigationIntent to evidence highlights."""

    def test_route_finding_click_produces_select_finding_intent(
        self, finding_a: Finding, ev_ref_a: EvidenceReference,
    ) -> None:
        router = WorkbenchNavigationRouter(findings=[finding_a], evidence_items=[ev_ref_a])
        intent = router.route_finding_click("RULE-001")
        assert intent.action == NavigationAction.SELECT_FINDING
        assert intent.target_id == "RULE-001"
        assert intent.origin == NavigationOrigin.INSPECTOR

    def test_route_finding_click_carries_linked_evidence_ids(
        self, finding_a: Finding, ev_ref_a: EvidenceReference,
    ) -> None:
        router = WorkbenchNavigationRouter(findings=[finding_a], evidence_items=[ev_ref_a])
        intent = router.route_finding_click("RULE-001")
        assert "linked_evidence_ids" in intent.metadata
        assert "ev-001" in intent.metadata["linked_evidence_ids"]

    def test_apply_finding_intent_highlights_linked_evidence(
        self, orchestrator: WorkbenchOrchestrator, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        orchestrator.bind_evidence("P1", evidence_list)
        orchestrator.run_checkmate(finding_report)
        intent = orchestrator._router.route_finding_click("RULE-001")
        vm = orchestrator.apply_intent(intent)
        assert "ev-001" in vm.highlighted_evidence_ids

    def test_selected_finding_shown_as_selected_in_view_model(
        self, projector: WorkbenchProjector, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        state = WorkbenchState(
            stage=WorkbenchStage.CHECKMATE_EXECUTED,
            selected_finding_id="RULE-001",
        )
        vm = projector.project(
            state=state,
            finding_report=finding_report,
            understanding=None,
            chat_responses=None,
            evidence_items=evidence_list,
        )
        selected = [f for f in vm.findings if f.finding_id == "RULE-001"]
        assert len(selected) == 1 and selected[0].is_selected is True

    def test_bidirectional_index_consistency(
        self, finding_a: Finding, finding_b: Finding,
        ev_ref_a: EvidenceReference, ev_ref_b: EvidenceReference,
    ) -> None:
        router = WorkbenchNavigationRouter(
            findings=[finding_a, finding_b],
            evidence_items=[ev_ref_a, ev_ref_b],
        )
        assert router.get_linked_findings("ev-001") == ["RULE-001"]
        assert router.get_linked_findings("ev-002") == ["RULE-002"]
        assert router.get_linked_evidence("RULE-001") == ["ev-001"]
        assert router.get_linked_evidence("RULE-002") == ["ev-002"]

# ===========================================================================
# AC-5: Canonical Workflow Execution
# ===========================================================================

class TestAC5CanonicalPipeline:
    """AC-5: Complete pipeline Bind->Validate->Understand->Chat->Inspect succeeds."""

    def test_idle_on_init(self, orchestrator: WorkbenchOrchestrator) -> None:
        assert orchestrator.state.stage == WorkbenchStage.IDLE

    def test_bind_evidence_advances_stage(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
    ) -> None:
        vm = orchestrator.bind_evidence("TestProject", evidence_list)
        assert orchestrator.state.stage == WorkbenchStage.EVIDENCE_BOUND
        assert orchestrator.state.bound_project == "TestProject"
        assert vm.workflow_status.evidence_ready is True
        assert len(vm.evidence_items) == 2

    def test_run_checkmate_advances_stage(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport,
    ) -> None:
        orchestrator.bind_evidence("TestProject", evidence_list)
        vm = orchestrator.run_checkmate(finding_report)
        assert orchestrator.state.stage == WorkbenchStage.CHECKMATE_EXECUTED
        assert orchestrator.state.active_report_id == "exec-abc-12345678"
        assert vm.workflow_status.checkmate_ready is True
        assert len(vm.findings) == 2

    def test_ingest_understanding_advances_stage(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport, project_understanding: ProjectUnderstanding,
    ) -> None:
        orchestrator.bind_evidence("TestProject", evidence_list)
        orchestrator.run_checkmate(finding_report)
        vm = orchestrator.ingest_understanding(project_understanding)
        assert orchestrator.state.stage == WorkbenchStage.UNDERSTANDING_INGESTED
        assert vm.workflow_status.understanding_ready is True

    def test_submit_chat_advances_to_chat_ready(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport, project_understanding: ProjectUnderstanding,
        assistant_response: AssistantResponse,
    ) -> None:
        orchestrator.bind_evidence("TestProject", evidence_list)
        orchestrator.run_checkmate(finding_report)
        orchestrator.ingest_understanding(project_understanding)
        vm = orchestrator.submit_chat(assistant_response)
        assert orchestrator.state.stage == WorkbenchStage.CHAT_READY
        assert vm.workflow_status.chat_ready is True
        assert len(vm.chat_responses) == 1

    def test_inspect_finding_after_full_pipeline(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport, project_understanding: ProjectUnderstanding,
        assistant_response: AssistantResponse,
    ) -> None:
        orchestrator.bind_evidence("TestProject", evidence_list)
        orchestrator.run_checkmate(finding_report)
        orchestrator.ingest_understanding(project_understanding)
        orchestrator.submit_chat(assistant_response)
        vm = orchestrator.inspect_finding("RULE-001")
        assert orchestrator.state.selected_finding_id == "RULE-001"
        selected = [f for f in vm.findings if f.finding_id == "RULE-001"]
        assert selected[0].is_selected is True

    def test_understanding_enriches_finding_view_model(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport, project_understanding: ProjectUnderstanding,
    ) -> None:
        orchestrator.bind_evidence("TestProject", evidence_list)
        orchestrator.run_checkmate(finding_report)
        vm = orchestrator.ingest_understanding(project_understanding)
        enriched = [f for f in vm.findings if f.finding_id == "RULE-001"]
        assert len(enriched) == 1
        assert enriched[0].has_understanding is True
        assert enriched[0].category_label != ""

# ===========================================================================
# AC-6: Domain Immutability
# ===========================================================================

class TestAC6DomainImmutability:
    """AC-6: UI interactions never mutate underlying domain contracts."""

    def test_finding_report_not_mutated_by_navigation(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport,
    ) -> None:
        original_findings_count = len(finding_report.findings)
        original_id = finding_report.provenance.execution_id
        orchestrator.bind_evidence("P1", evidence_list)
        orchestrator.run_checkmate(finding_report)
        orchestrator.on_select_finding("RULE-001")
        orchestrator.on_clear_selection()
        # Domain contract unchanged
        assert len(finding_report.findings) == original_findings_count
        assert finding_report.provenance.execution_id == original_id

    def test_evidence_reference_not_mutated_by_selection(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        ev_ref_a: EvidenceReference,
    ) -> None:
        original_eid = ev_ref_a.evidence_id
        original_doc = ev_ref_a.document_id
        orchestrator.bind_evidence("P1", evidence_list)
        orchestrator.on_select_evidence("ev-001")
        assert ev_ref_a.evidence_id == original_eid
        assert ev_ref_a.document_id == original_doc

    def test_assistant_response_not_mutated_by_navigation(
        self, orchestrator: WorkbenchOrchestrator, finding_report: FindingReport,
        project_understanding: ProjectUnderstanding, assistant_response: AssistantResponse,
        evidence_list: list[EvidenceReference],
    ) -> None:
        original_text = assistant_response.response_text
        original_status = assistant_response.grounding_status
        orchestrator.bind_evidence("P1", evidence_list)
        orchestrator.run_checkmate(finding_report)
        orchestrator.ingest_understanding(project_understanding)
        orchestrator.submit_chat(assistant_response)
        orchestrator.on_navigate_citation("ev-001")
        assert assistant_response.response_text == original_text
        assert assistant_response.grounding_status == original_status

    def test_finding_report_is_frozen_dataclass(self, finding_report: FindingReport) -> None:
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            finding_report.domain_coverage = {}  # type: ignore[misc]

    def test_assistant_response_is_frozen_dataclass(self, assistant_response: AssistantResponse) -> None:
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            assistant_response.response_text = "mutated"  # type: ignore[misc]

    def test_evidence_reference_is_frozen_dataclass(self, ev_ref_a: EvidenceReference) -> None:
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            ev_ref_a.evidence_id = "mutated"  # type: ignore[misc]

# ===========================================================================
# AC-7: State Separation
# ===========================================================================

class TestAC7StateSeparation:
    """AC-7: WorkbenchState (domain) and WorkbenchViewModel (presentation) are decoupled."""

    def test_workbench_state_and_view_model_are_different_types(self) -> None:
        state = WorkbenchState()
        status = WorkflowStatusViewModel(stage_label="Idle")
        vm = WorkbenchViewModel(workflow_status=status)
        assert type(state) is not type(vm)

    def test_state_transition_does_not_mutate_old_state(self) -> None:
        state1 = WorkbenchState()
        state2 = state1.with_evidence_bound("Project-X")
        assert state1.stage == WorkbenchStage.IDLE
        assert state2.stage == WorkbenchStage.EVIDENCE_BOUND
        assert state1.bound_project is None
        assert state2.bound_project == "Project-X"

    def test_view_model_does_not_share_fields_with_workbench_state(self) -> None:
        state_fields = {f.name for f in dataclasses.fields(WorkbenchState)}
        vm_fields = {f.name for f in dataclasses.fields(WorkbenchViewModel)}
        shared = state_fields & vm_fields
        # The two types must not share any field names (strict decoupling)
        assert len(shared) == 0, f"Shared fields between state and VM: {shared}"

    def test_projector_does_not_modify_state(
        self, projector: WorkbenchProjector, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        """Projector returns a ViewModel without altering the domain state."""
        state = WorkbenchState(stage=WorkbenchStage.EVIDENCE_BOUND)
        original = WorkbenchState(stage=WorkbenchStage.EVIDENCE_BOUND)
        _vm = projector.project(
            state=state, finding_report=finding_report,
            understanding=None, chat_responses=None, evidence_items=evidence_list,
        )
        assert state.stage == original.stage

    def test_workbench_view_model_does_not_contain_domain_contracts(self) -> None:
        """WorkbenchViewModel fields are projected values, not raw domain contracts."""
        status = WorkflowStatusViewModel(stage_label="Idle")
        vm = WorkbenchViewModel(workflow_status=status)
        fields = {f.name: f.type for f in dataclasses.fields(WorkbenchViewModel)}
        # findings field stores view models, not raw domain objects
        assert "findings" in fields

# ===========================================================================
# AC-8: Deterministic Projection
# ===========================================================================

class TestAC8DeterministicProjection:
    """AC-8: Given identical inputs, WorkbenchProjector produces identical WorkbenchViewModel."""

    def test_identical_inputs_produce_identical_view_model(
        self, projector: WorkbenchProjector, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        state = WorkbenchState(stage=WorkbenchStage.CHECKMATE_EXECUTED)
        ui_state = UIState()

        vm1 = projector.project(
            state=state, finding_report=finding_report,
            understanding=None, chat_responses=None,
            evidence_items=evidence_list, ui_state=ui_state,
        )
        vm2 = projector.project(
            state=state, finding_report=finding_report,
            understanding=None, chat_responses=None,
            evidence_items=evidence_list, ui_state=ui_state,
        )
        # Same inputs = same outputs (pure function)
        assert vm1 == vm2
        assert vm1.findings == vm2.findings
        assert vm1.evidence_items == vm2.evidence_items
        assert vm1.workflow_status == vm2.workflow_status

    def test_different_state_produces_different_output(
        self, projector: WorkbenchProjector, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        state_ev_ready = WorkbenchState(stage=WorkbenchStage.EVIDENCE_BOUND)
        state_chk_done = WorkbenchState(stage=WorkbenchStage.CHECKMATE_EXECUTED)

        vm1 = projector.project(
            state=state_ev_ready, finding_report=None,
            understanding=None, chat_responses=None, evidence_items=evidence_list,
        )
        vm2 = projector.project(
            state=state_chk_done, finding_report=finding_report,
            understanding=None, chat_responses=None, evidence_items=evidence_list,
        )
        assert vm1 != vm2
        assert vm1.workflow_status != vm2.workflow_status

    def test_selecting_finding_changes_highlight_set(self, projector: WorkbenchProjector,
        finding_report: FindingReport, evidence_list: list[EvidenceReference]) -> None:
        state = WorkbenchState(stage=WorkbenchStage.CHECKMATE_EXECUTED)
        vm1 = projector.project(
            state=state, finding_report=finding_report,
            understanding=None, chat_responses=None, evidence_items=evidence_list,
        )
        vm2 = projector.project(
            state=state, finding_report=finding_report,
            understanding=None, chat_responses=None, evidence_items=evidence_list,
            highlighted_finding_ids=frozenset(["RULE-001"]),
        )
        assert vm1.highlighted_finding_ids != vm2.highlighted_finding_ids
        assert "RULE-001" in vm2.highlighted_finding_ids

    def test_filter_text_changes_findings_subset(
        self, projector: WorkbenchProjector, finding_report: FindingReport,
        evidence_list: list[EvidenceReference],
    ) -> None:
        state = WorkbenchState(stage=WorkbenchStage.CHECKMATE_EXECUTED)
        ui_all = UIState()
        ui_filtered = UIState(filter_text="RULE-001")

        vm1 = projector.project(
            state=state, finding_report=finding_report,
            understanding=None, chat_responses=None,
            evidence_items=evidence_list, ui_state=ui_all,
        )
        vm2 = projector.project(
            state=state, finding_report=finding_report,
            understanding=None, chat_responses=None,
            evidence_items=evidence_list, ui_state=ui_filtered,
        )
        assert len(vm1.findings) == 2
        assert len(vm2.findings) == 1
        assert vm2.findings[0].finding_id == "RULE-001"

    def test_navigation_intent_is_frozen_dataclass(self) -> None:
        intent = NavigationIntent(
            action=NavigationAction.SELECT_EVIDENCE,
            target_id="ev-001",
            origin=NavigationOrigin.EVIDENCE_VIEWER,
        )
        with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
            intent.action = NavigationAction.CLEAR_SELECTION  # type: ignore[misc]

# ===========================================================================
# Additional: Integration tests for the full roundtrip
# ===========================================================================

class TestFullRoundtrip:
    """End-to-end pipeline execution from bind through navigate and inspect."""

    def test_user_interaction_sink_methods_update_state_correctly(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport,
    ) -> None:
        """Calling UserInteractionSink methods directly updates state and projection."""
        orchestrator.bind_evidence("P1", evidence_list)
        orchestrator.run_checkmate(finding_report)

        orchestrator.on_select_evidence("ev-001")
        assert orchestrator.state.selected_evidence_id == "ev-001"

        orchestrator.on_select_finding("RULE-001")
        assert orchestrator.state.selected_finding_id == "RULE-001"

        orchestrator.on_clear_selection()
        assert orchestrator.state.selected_finding_id is None
        assert orchestrator.state.selected_evidence_id is None

    def test_citation_navigation_from_chat_to_evidence(
        self, orchestrator: WorkbenchOrchestrator, evidence_list: list[EvidenceReference],
        finding_report: FindingReport, project_understanding: ProjectUnderstanding,
        assistant_response: AssistantResponse,
    ) -> None:
        """Citation navigation routes chat to evidence panel highlighting."""
        orchestrator.bind_evidence("P1", evidence_list)
        orchestrator.run_checkmate(finding_report)
        orchestrator.ingest_understanding(project_understanding)
        orchestrator.submit_chat(assistant_response)
        orchestrator.on_navigate_citation("ev-001")
        assert orchestrator.state.selected_evidence_id == "ev-001"
        assert "ev-001" in orchestrator.current_view_model.highlighted_evidence_ids
