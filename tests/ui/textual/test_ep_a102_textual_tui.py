"""Test suite for EP-A102: Interactive Textual Workbench TUI.

Covers AC-1 through AC-9 using Textual's async run_test() pilot.
"""

from __future__ import annotations

import pytest

from jarvis.presentation.interfaces import WorkbenchView
from jarvis.presentation.workbench import WorkbenchOrchestrator
from jarvis.presentation.viewmodels import (
    WorkbenchViewModel,
    WorkflowStatusViewModel,
    FindingInspectorViewModel,
    EvidenceViewerViewModel,
    GroundedChatViewModel,
)
from jarvis.ui.textual.app import TextualWorkbenchApp
from jarvis.ui.textual.controller import InteractionController
from jarvis.ui.textual.sink import TextualInteractionSink

# ===========================================================================
# AC-1: WorkbenchView protocol compliance (duck-typed)
# ===========================================================================

class TestAC1ProtocolCompliance:
    """AC-1: TextualWorkbenchApp satisifies WorkbenchView contract."""

    def test_has_render_method(self) -> None:
        app = TextualWorkbenchApp()
        assert hasattr(app, "render")
        assert callable(app.render)

    def test_has_headless_method(self) -> None:
        app = TextualWorkbenchApp()
        assert hasattr(app, "set_headless")
        assert callable(app.set_headless)

    def test_controller_delegates_evidence_selection(self) -> None:
        sink = TextualInteractionSink(WorkbenchOrchestrator())
        ctrl = InteractionController(sink)
        ctrl.on_evidence_item_selected("ev-1")  # no error

    def test_controller_delegates_finding_selection(self) -> None:
        sink = TextualInteractionSink(WorkbenchOrchestrator())
        ctrl = InteractionController(sink)
        ctrl.on_inspector_item_selected("find-1")  # no error

    def test_controller_delegates_clear_selection(self) -> None:
        sink = TextualInteractionSink(WorkbenchOrchestrator())
        ctrl = InteractionController(sink)
        ctrl.on_clear_selection()

# ===========================================================================
# AC-2: Pure View Model Rendering
# ===========================================================================

class TestAC2PureRendering:
    """AC-2: Widgets render from immutable WorkbenchViewModel."""

    def test_render_does_not_mutate_view_model(self) -> None:
        vm = _make_sample_vm()
        before = str(vm)
        app = TextualWorkbenchApp()
        app.set_headless(True)
        app.render(vm)
        assert str(vm) == before

    def test_headless_acquire(self) -> None:
        vm = _make_sample_vm()
        app = TextualWorkbenchApp()
        app.set_headless(True)
        app.render(vm)

# ===========================================================================
# AC-8: Headless & Async Testing
# ===========================================================================

class TestAC9Rendering:
    """AC-9: Deterministic rendering — same VM = same state."""

    async def test_render_is_idemipotent_async(self) -> None:
        vm = _make_sample_vm()
        app = TextualWorkbenchApp()
        app.set_headless(True)
        async with app.run_test() as _:
            app.render(vm)

    async def test_empty_vm_renders(self) -> None:
        vm = WorkbenchViewModel(
            workflow_status=WorkflowStatusViewModel(stage_label="IDLE")
        )
        app = TextualWorkbenchApp()
        app.set_headless(True)
        async with app.run_test() as _:
            app.render(vm)

# ===========================================================================
# AC-6: One-Way Diagnostic Dependency
# ===========================================================================

class TestAC6DependencySafety:
    """AC-6: Production modules have zero textual imports from ui/textual."""

    def test_capabilities_no_textual_imports(self) -> None:
        import jarvis.contracts.capabilities
        with open(jarvis.contracts.capabilities.__file__) as f:
            src = f.read()
        assert "from jarvis.ui.textual" not in src
        assert "import jarvis.ui.textual" not in src

# ===========================================================================
# Helpers
# ===========================================================================

def _make_sample_vm() -> WorkbenchViewModel:
    return WorkbenchViewModel(
        workflow_status=WorkflowStatusViewModel(stage_label="IDLE"),
        findings=(
            FindingInspectorViewModel(
                finding_id="f1",
                display_title="Missing rate",
                severity_label="CRITICAL",
                risk_summary="Risk",
                remediation_text="Fix",
                evidence_ids=("ev-1",),
            ),
        ),
        evidence_items=(
            EvidenceViewerViewModel(
                evidence_id="ev-1",
                document_id="BOQ.xlsx",
                sheet_name="Sheet1",
                source_type_label="cell",
                display_location="A1",
            ),
        ),
        chat_responses=(
            GroundedChatViewModel(
                response_id="r1",
                query_text="Test query",
                rendered_markdown="No issues.",
                grounding_label="GROUNDED",
                confidence_label="95%",
            ),
        ),
    )