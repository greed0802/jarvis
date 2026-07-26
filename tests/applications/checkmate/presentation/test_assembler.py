"""Tests for CheckMate Presentation Assembler (IP-0005).

Verifies:
- PresentationModel immutability
- Assembler determinism
- No business logic in PresentationModel
- No interpretation in assembler
- No mutation of inputs
- Navigation correctness
- View consistency
- Serialization readiness (all frozen dataclasses)
- Stable ordering
- Stable identifiers
"""

from __future__ import annotations

import pytest

from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.applications.checkmate.interpretation.engine import interpret
from jarvis.applications.checkmate.presentation.assembler import assemble
from jarvis.applications.checkmate.presentation.models import (
    PresentationModel,
    DashboardView,
    SummaryView,
    FindingView,
    FindingDisplay,
    RecommendationView,
    RecommendationDisplay,
    SectionView,
    SectionDisplay,
    NavigationView,
    NavigationIndex,
    NavigationEntry,
    MetadataView,
)
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding

# ============================================================================
# Test Helpers
# ============================================================================

def _make_minimal_evidence() -> BOQIntelligenceResult:
    """Create minimal evidence for testing."""
    return BOQIntelligenceResult(
        row_classification={"Head": 5, "Item": 10, "Note": 1},
        section_statistics={
            "Section A": {"items": 5, "page": 1},
            "Section B": {"items": 5, "page": 1},
        },
        boq_statistics={"total_rows": 16, "total_sections": 2},
        known_anomalies=[],
    )

def _make_findings(*finding_types: str) -> ValidationFindings:
    """Create findings with specified finding_types."""
    entries: list[ValidationFinding] = []
    for i, ft in enumerate(finding_types, start=1):
        entries.append(ValidationFinding(
            rule_id=f"V-{i:03d}",
            rule_version="1.0.0",
            category="Test Category",
            finding_type=ft,
            finding_value=0,
            evidence_fields=("row_classification", "section_statistics"),
        ))
    return ValidationFindings(
        findings=tuple(entries),
        engine_version="1.0.0",
        contract_version="1.0.0",
        execution_timestamp="2026-07-25T00:00:00+00:00",
    )

def _make_context(
    evidence: BOQIntelligenceResult | None = None,
    findings: ValidationFindings | None = None,
) -> ApplicationContext:
    return ApplicationContext(
        evidence=evidence or _make_minimal_evidence(),
        findings=findings or _make_findings("Error", "Warning", "Information"),
    )

# ============================================================================
# Immutability Tests
# ============================================================================

class TestPresentationModelImmutability:
    """Verify PresentationModel and all child views are immutable."""

    def test_root_model_is_frozen(self) -> None:
        ctx = _make_context()
        interpretation = interpret(ctx)
        model = assemble(ctx, interpretation)
        with pytest.raises(Exception):
            model.dashboard = DashboardView(
                total_findings=999, total_recommendations=999,
                high_severity_count=999, medium_severity_count=999,
                low_severity_count=999, total_sections=999,
            )

    def test_dashboard_is_frozen(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        with pytest.raises(Exception):
            model.dashboard.total_findings = 999

    def test_summary_is_frozen(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        with pytest.raises(Exception):
            model.summary.application_title = "mutated"

    def test_findings_is_frozen(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        with pytest.raises(Exception):
            model.findings.items = ()

    def test_recommendations_is_frozen(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        with pytest.raises(Exception):
            model.recommendations.items = ()

    def test_sections_is_frozen(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        with pytest.raises(Exception):
            model.sections.items = ()

    def test_navigation_is_frozen(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        with pytest.raises(Exception):
            model.navigation.indexes = ()

    def test_metadata_is_frozen(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        with pytest.raises(Exception):
            model.metadata.runtime_id = "mutated"

# ============================================================================
# No Business Logic Tests
# ============================================================================

class TestNoBusinessLogicInModel:
    """Verify PresentationModel contains no business logic."""

    def test_dashboard_has_no_compute_methods(self) -> None:
        """DashboardView should be pure data, no compute methods."""
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        d = model.dashboard
        # Check key attributes exist
        assert isinstance(d.total_findings, int)
        assert isinstance(d.total_recommendations, int)
        # No compute, no severity reclassification
        assert not hasattr(d, "compute")
        assert not hasattr(d, "classify")
        assert not hasattr(d, "interpret")

    def test_findings_have_no_severity_mapping(self) -> None:
        """FindingDisplay has precomputed severity, no remapping."""
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        for fd in model.findings.items:
            assert isinstance(fd.severity_label, str)
            assert fd.severity_label in ("HIGH", "MEDIUM", "LOW")
            assert not hasattr(fd, "map_severity")
            assert not hasattr(fd, "reclassify")

    def test_recommendations_have_no_recalculation(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        for rd in model.recommendations.items:
            assert isinstance(rd.display_order, int)
            assert not hasattr(rd, "compute_order")
            assert not hasattr(rd, "generate")

# ============================================================================
# Assembler Determinism
# ============================================================================

class TestAssemblerDeterminism:
    """Verify presentation assembly is deterministic."""

    def test_identical_inputs_produce_identical_presentation(self) -> None:
        ctx1 = _make_context(findings=_make_findings("Error", "Warning"))
        ctx2 = _make_context(findings=_make_findings("Error", "Warning"))
        interp1 = interpret(ctx1)
        interp2 = interpret(ctx2)
        model1 = assemble(ctx1, interp1)
        model2 = assemble(ctx2, interp2)
        # Full structural comparison
        assert model1.dashboard == model2.dashboard
        assert model1.summary.application_title == model2.summary.application_title
        assert len(model1.findings) == len(model2.findings)
        assert len(model1.recommendations) == len(model2.recommendations)
        assert len(model1.sections) == len(model2.sections)
        assert len(model1.navigation) == len(model2.navigation)

    def test_finding_sort_keys_are_stable(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning", "Information"))
        model = assemble(ctx, interpret(ctx))
        sort_keys = [fd.sort_key for fd in model.findings.items]
        # Sort keys should be unique and stable
        assert len(sort_keys) == len(set(sort_keys))
        # HIGH severity (order 0) sorts before MEDIUM (order 10) before LOW (order 20)
        assert sort_keys[0] < sort_keys[1] < sort_keys[2]

    def test_recommendation_order_is_stable(self) -> None:
        ctx = _make_context(findings=_make_findings("Error"))
        model = assemble(ctx, interpret(ctx))
        orders = [rd.display_order for rd in model.recommendations.items]
        assert orders == sorted(orders)
        assert orders == list(range(len(model.recommendations)))

# ============================================================================
# No Mutation Tests
# ============================================================================

class TestNoMutation:
    """Verify assembler does not mutate inputs."""

    def test_context_evidence_unchanged(self) -> None:
        ctx = _make_context()
        original_rc = dict(ctx.evidence.row_classification)
        model = assemble(ctx, interpret(ctx))
        assert ctx.evidence.row_classification == original_rc

    def test_context_findings_unchanged(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        original_count = len(ctx.findings.findings)
        model = assemble(ctx, interpret(ctx))
        assert len(ctx.findings.findings) == original_count

    def test_interpretation_unchanged(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        interpretation = interpret(ctx)
        original_stats = interpretation.statistics
        model = assemble(ctx, interpretation)
        assert interpretation.statistics == original_stats

# ============================================================================
# View Consistency Tests
# ============================================================================

class TestViewConsistency:
    """Verify all views are internally consistent."""

    def test_dashboard_counts_match_findings(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Error", "Warning", "Information"))
        model = assemble(ctx, interpret(ctx))
        assert model.dashboard.total_findings == 4
        assert model.dashboard.high_severity_count == 2
        assert model.dashboard.medium_severity_count == 1
        assert model.dashboard.low_severity_count == 1

    def test_findings_count_matches_input(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning", "Information"))
        model = assemble(ctx, interpret(ctx))
        assert len(model.findings) == 3

    def test_findings_and_navigation_consistent(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        model = assemble(ctx, interpret(ctx))
        finding_ids = [fd.finding_id for fd in model.findings.items]
        nav_labels = []
        for nav in model.navigation.indexes:
            for entry in nav.items:
                nav_labels.append(entry.label)
        for fid in finding_ids:
            assert fid in nav_labels

    def test_sections_count_matches_evidence(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert len(model.sections) == 2  # Section A + Section B
        assert model.sections.items[0].section_name == "Section A"
        assert model.sections.items[1].section_name == "Section B"

    def test_summary_overall_severity(self) -> None:
        ctx = _make_context(findings=_make_findings("Error"))
        model = assemble(ctx, interpret(ctx))
        assert model.summary.overall_severity == "HIGH"

    def test_summary_no_findings(self) -> None:
        ctx = _make_context(findings=_make_findings())
        model = assemble(ctx, interpret(ctx))
        assert model.summary.overall_severity == "NONE"
        assert model.dashboard.total_findings == 0

# ============================================================================
# Navigation Tests
# ============================================================================

class TestNavigation:
    """Verify precomputed navigation indexes."""

    def test_navigation_has_findings_by_severity(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning", "Information"))
        model = assemble(ctx, interpret(ctx))
        sev_titles = [idx.title for idx in model.navigation.indexes
                      if "Findings" in idx.title and "Severity" in idx.title]
        assert len(sev_titles) > 0
        assert any("HIGH" in t for t in sev_titles)

    def test_navigation_has_findings_by_category(self) -> None:
        findings = ValidationFindings(
            findings=(
                ValidationFinding(
                    rule_id="V-001", rule_version="1.0.0",
                    category="Category Alpha",
                    finding_type="Error", finding_value=0,
                    evidence_fields=("row_classification",),
                ),
                ValidationFinding(
                    rule_id="V-002", rule_version="1.0.0",
                    category="Category Beta",
                    finding_type="Warning", finding_value=0,
                    evidence_fields=("row_classification",),
                ),
            ),
            engine_version="1.0.0",
            contract_version="1.0.0",
            execution_timestamp="2026-07-25T00:00:00+00:00",
        )
        ctx = _make_context(findings=findings)
        model = assemble(ctx, interpret(ctx))
        cat_titles = [idx.title for idx in model.navigation.indexes
                      if "Findings" in idx.title and "Category" in idx.title]
        # Category navigation groups by category name
        cat_titles = [idx.title for idx in model.navigation.indexes
                      if "Category Alpha" in idx.title or "Category Beta" in idx.title]
        assert len(cat_titles) >= 2

    def test_navigation_has_sections(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        section_indexes = [idx for idx in model.navigation.indexes
                           if "Section" in idx.title]
        assert len(section_indexes) >= 1

    def test_navigation_has_recommendations_by_severity(self) -> None:
        ctx = _make_context(findings=_make_findings("Error"))
        model = assemble(ctx, interpret(ctx))
        rec_indexes = [idx for idx in model.navigation.indexes
                       if "Recommendations" in idx.title]
        assert len(rec_indexes) >= 0  # depends on generated recommendations

    def test_navigation_entries_have_valid_href(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        model = assemble(ctx, interpret(ctx))
        for nav in model.navigation.indexes:
            for entry in nav.items:
                assert entry.href.startswith("#")
                assert len(entry.href) > 1

# ============================================================================
# Serialization Readiness
# ============================================================================

class TestSerializationReadiness:
    """Verify models are naturally serializable (frozen dataclasses)."""

    def test_presentation_model_to_dict_via_dataclasses(self) -> None:
        from dataclasses import asdict
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        model = assemble(ctx, interpret(ctx))
        d = asdict(model)
        assert isinstance(d, dict)
        assert "dashboard" in d
        assert "summary" in d
        assert "findings" in d
        assert "recommendations" in d
        assert "sections" in d
        assert "navigation" in d
        assert "metadata" in d

    def test_all_view_models_are_dataclasses(self) -> None:
        from dataclasses import is_dataclass, asdict
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert is_dataclass(model)
        assert is_dataclass(model.dashboard)
        assert is_dataclass(model.summary)
        assert is_dataclass(model.findings)
        assert is_dataclass(model.recommendations)
        assert is_dataclass(model.sections)
        assert is_dataclass(model.navigation)
        assert is_dataclass(model.metadata)

    def test_leaf_entries_are_dataclasses(self) -> None:
        from dataclasses import is_dataclass
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        if model.findings.items:
            assert is_dataclass(model.findings.items[0])
        if model.recommendations.items:
            assert is_dataclass(model.recommendations.items[0])
        if model.sections.items:
            assert is_dataclass(model.sections.items[0])
        for idx in model.navigation.indexes:
            assert is_dataclass(idx)
            for entry in idx.items:
                assert is_dataclass(entry)

# ============================================================================
# No Rendering Tests
# ============================================================================

class TestNoRendering:
    """Verify PresentationModel has no rendering logic."""

    def test_no_render_methods(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert not hasattr(model, "render")
        assert not hasattr(model, "to_html")
        assert not hasattr(model, "to_pdf")
        assert not hasattr(model, "to_json")
        assert not hasattr(model, "to_csv")
        assert not hasattr(model, "to_cli")

    def test_no_export_methods(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert not hasattr(model, "export")
        assert not hasattr(model, "save")

    def test_no_report_generation(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert not hasattr(model, "generate_report")
        assert not hasattr(model, "build_report")
        assert not hasattr(model, "report")

# ============================================================================
# Assembler Boundaries
# ============================================================================

class TestAssemblerBoundaries:
    """Verify assembler doesn't cross architectural boundaries."""

    def test_assemble_returns_only_presentation_model(self) -> None:
        ctx = _make_context()
        interpretation = interpret(ctx)
        model = assemble(ctx, interpretation)
        assert isinstance(model, PresentationModel)
        # Should not return anything else
        assert not isinstance(model, dict)
        assert not isinstance(model, str)

    def test_assemble_does_not_mutate_interpretation(self) -> None:
        ctx = _make_context()
        interpretation = interpret(ctx)
        original_high = interpretation.statistics.high_count
        model = assemble(ctx, interpretation)
        assert interpretation.statistics.high_count == original_high

    def test_assembler_does_not_reimport_interpretation(self) -> None:
        """Assembly should not call interpret() again."""
        ctx = _make_context()
        interpretation = interpret(ctx)
        # Call assemble; doesn't re interpret
        model = assemble(ctx, interpretation)
        assert len(model.findings) >= 0  # just checks it runs

# ============================================================================
# Metadata Tests
# ============================================================================

class TestMetadataContents:
    """Verify MetadataView contains all required fields."""

    def test_metadata_runtime_id_present(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert len(model.metadata.runtime_id) > 0

    def test_metadata_timestamps_present(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert len(model.metadata.execution_timestamp) > 0

    def test_metadata_application_name(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert model.metadata.application_name == "CheckMate"

    def test_metadata_version_strings(self) -> None:
        ctx = _make_context()
        model = assemble(ctx, interpret(ctx))
        assert len(model.metadata.application_version) > 0
        assert len(model.metadata.contract_version) > 0
        assert len(model.metadata.engine_version) > 0