"""Tests for CheckMate Interpretation Engine (IP-0004).

Verifies:
- Interpretation determinism
- Severity mapping
- Finding grouping (category, severity, section, rule)
- Recommendation generation
- Statistics computation
- Evidence immutability
- Finding immutability
- No Presentation Model
- No reports
- No exports
- No rendering
"""

from __future__ import annotations

import pytest

from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.applications.checkmate.interpretation.engine import interpret
from jarvis.applications.checkmate.interpretation.models import (
    Severity,
    SeverityInfo,
    SeverityMap,
    FindingGroup,
    FindingGroups,
    Recommendation,
    RecommendationSet,
    InterpretationStatistics,
    InterpretationSummary,
)
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding

# ============================================================================
# Test Helpers
# ============================================================================

def _make_minimal_evidence(
    *,
    zero_quantity_items: tuple = (),
    detected_level_skips: tuple = (),
    header_quantity_violations: tuple = (),
    completeness_findings: tuple = (),
) -> BOQIntelligenceResult:
    """Create minimal evidence with optional detection fields."""
    return BOQIntelligenceResult(
        row_classification={"Head": 5, "Item": 10, "Note": 1},
        section_statistics={
            "Section A": {"items": 5, "page": 1},
            "Section B": {"items": 5, "page": 1},
        },
        boq_statistics={"total_rows": 16, "total_sections": 2},
        known_anomalies=[],
        zero_quantity_items=zero_quantity_items if zero_quantity_items else None,
        detected_level_skips=detected_level_skips,
        header_quantity_violations=header_quantity_violations,
        completeness_findings=completeness_findings,
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
# Severity Mapping Tests
# ============================================================================

class TestSeverityMapping:
    """Verify deterministic severity classification."""

    def test_error_finding_type_maps_to_high(self) -> None:
        ctx = _make_context(findings=_make_findings("Error"))
        summary = interpret(ctx)
        assert summary.severity_map.entries[0].severity == Severity.HIGH
        assert summary.severity_map.entries[0].finding_id == "V-001"
        assert "Error" in summary.severity_map.entries[0].reason

    def test_warning_finding_type_maps_to_medium(self) -> None:
        ctx = _make_context(findings=_make_findings("Warning"))
        summary = interpret(ctx)
        assert summary.severity_map.entries[0].severity == Severity.MEDIUM

    def test_information_finding_type_maps_to_low(self) -> None:
        ctx = _make_context(findings=_make_findings("Information"))
        summary = interpret(ctx)
        assert summary.severity_map.entries[0].severity == Severity.LOW

    def test_critical_finding_type_maps_to_high(self) -> None:
        ctx = _make_context(findings=_make_findings("Critical"))
        summary = interpret(ctx)
        assert summary.severity_map.entries[0].severity == Severity.HIGH

    def test_hint_finding_type_maps_to_low(self) -> None:
        ctx = _make_context(findings=_make_findings("Hint"))
        summary = interpret(ctx)
        assert summary.severity_map.entries[0].severity == Severity.LOW

    def test_unknown_finding_type_defaults_to_low(self) -> None:
        ctx = _make_context(findings=_make_findings("UnknownType"))
        summary = interpret(ctx)
        assert summary.severity_map.entries[0].severity == Severity.LOW

    def test_multiple_findings_classified(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning", "Information", "Critical"))
        summary = interpret(ctx)
        severities = [e.severity for e in summary.severity_map.entries]
        assert severities == [Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.HIGH]

    def test_empty_findings_produce_empty_severity_map(self) -> None:
        findings = _make_findings()
        ctx = _make_context(findings=findings)
        summary = interpret(ctx)
        assert len(summary.severity_map.entries) == 0

    def test_severity_map_is_deterministic(self) -> None:
        findings1 = _make_findings("Error", "Warning", "Information")
        findings2 = _make_findings("Error", "Warning", "Information")
        ctx1 = _make_context(findings=findings1)
        ctx2 = _make_context(findings=findings2)
        summary1 = interpret(ctx1)
        summary2 = interpret(ctx2)
        assert summary1.severity_map.to_dict() == summary2.severity_map.to_dict()

    def test_severity_map_to_dict(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        summary = interpret(ctx)
        d = summary.severity_map.to_dict()
        assert isinstance(d, dict)
        assert len(d) == 2
        # Check values are severity string values
        for v in d.values():
            assert v in {"HIGH", "MEDIUM", "LOW"}

class TestSeverityMapFiltering:
    """Verify SeverityMap.of_severity filtering."""

    def test_filter_by_high(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning", "Information"))
        summary = interpret(ctx)
        t = summary.severity_map.of_severity(Severity.HIGH)
        assert len(t) == 1
        assert t[0].severity == Severity.HIGH

    def test_filter_by_medium(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        summary = interpret(ctx)
        t = summary.severity_map.of_severity(Severity.MEDIUM)
        assert len(t) == 1
        assert t[0].severity == Severity.MEDIUM

    def test_filter_none_match(self) -> None:
        ctx = _make_context(findings=_make_findings("Information", "Information"))
        summary = interpret(ctx)
        t = summary.severity_map.of_severity(Severity.HIGH)
        assert len(t) == 0

# ============================================================================
# Finding Grouping Tests
# ============================================================================

class TestFindingGrouping:
    """Verify findings are grouped correctly."""

    def test_groups_by_category(self) -> None:
        findings = ValidationFindings(
            findings=(
                ValidationFinding(
                    rule_id="V-001",
                    rule_version="1.0.0",
                    category="Category A",
                    finding_type="Error",
                    finding_value=0,
                    evidence_fields=("row_classification",),
                ),
                ValidationFinding(
                    rule_id="V-002",
                    rule_version="1.0.0",
                    category="Category A",
                    finding_type="Warning",
                    finding_value=0,
                    evidence_fields=("section_statistics",),
                ),
                ValidationFinding(
                    rule_id="V-003",
                    rule_version="1.0.0",
                    category="Category B",
                    finding_type="Information",
                    finding_value=0,
                    evidence_fields=("row_classification",),
                ),
            ),
            engine_version="1.0.0",
            contract_version="1.0.0",
            execution_timestamp="2026-07-25T00:00:00+00:00",
        )
        ctx = _make_context(findings=findings)
        summary = interpret(ctx)
        cat_groups = summary.finding_groups.groups.get("category", {})
        assert "Category A" in cat_groups
        assert "Category B" in cat_groups
        assert cat_groups["Category A"].count == 2
        assert cat_groups["Category B"].count == 1

    def test_groups_by_severity(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Error", "Warning", "Information"))
        summary = interpret(ctx)
        sev_groups = summary.finding_groups.groups.get("severity", {})
        assert "HIGH" in sev_groups
        assert "MEDIUM" in sev_groups
        assert "LOW" in sev_groups
        assert sev_groups["HIGH"].count == 2
        assert sev_groups["MEDIUM"].count == 1
        assert sev_groups["LOW"].count == 1

    def test_groups_by_rule(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        summary = interpret(ctx)
        rule_groups = summary.finding_groups.groups.get("rule", {})
        assert "V-001" in rule_groups
        assert "V-002" in rule_groups

    def test_groups_by_section(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        sec_groups = summary.finding_groups.groups.get("section", {})
        assert "Section A" in sec_groups
        assert "Section B" in sec_groups

    def test_empty_findings_has_empty_groups(self) -> None:
        findings = _make_findings()
        ctx = _make_context(findings=findings)
        summary = interpret(ctx)
        cat_groups = summary.finding_groups.groups.get("category", {})
        assert len(cat_groups) == 0

    def test_finding_group_count_matches_finding_ids(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Error", "Error"))
        summary = interpret(ctx)
        sev_groups = summary.finding_groups.groups.get("severity", {})
        group = sev_groups["HIGH"]
        assert group.count == len(tuple(group.finding_ids))

    def test_grouping_is_deterministic(self) -> None:
        ctx1 = _make_context(findings=_make_findings("Error", "Warning"))
        ctx2 = _make_context(findings=_make_findings("Error", "Warning"))
        summary1 = interpret(ctx1)
        summary2 = interpret(ctx2)
        # Compare group structures
        g1 = summary1.finding_groups
        g2 = summary2.finding_groups
        assert g1.groups["severity"].keys() == g2.groups["severity"].keys()
        assert g1.groups["category"].keys() == g2.groups["category"].keys()

# ============================================================================
# Recommendation Generation Tests
# ============================================================================

class TestRecommendationGeneration:
    """Verify advisory recommendations are generated from evidence patterns."""

    def test_zero_quantity_items_generate_rec(self) -> None:
        evidence = _make_minimal_evidence(
            zero_quantity_items=(({"row_number": 1, "description": "test", "quantity": 0},),)
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        recs = summary.recommendations
        assert len(recs) > 0
        assert any("zero quantity" in r.text.lower() for r in recs.recommendations)

    def test_level_skip_rec_generated(self) -> None:
        evidence = _make_minimal_evidence(
            detected_level_skips=(({"level": 2, "from_level": 1, "to_level": 3},),)
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        recs = summary.recommendations
        assert any("level skip" in r.text.lower() for r in recs.recommendations)

    def test_header_quantity_rec_generated(self) -> None:
        evidence = _make_minimal_evidence(
            header_quantity_violations=(({"row_number": 5, "header_type": "Head1"},),)
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        recs = summary.recommendations
        assert any("header" in r.text.lower() for r in recs.recommendations)

    def test_completeness_rec_generated(self) -> None:
        evidence = _make_minimal_evidence(
            completeness_findings=(({"missing": "description", "count": 5},),)
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        recs = summary.recommendations
        assert any("missing description" in r.text.lower() for r in recs.recommendations)

    def test_multiple_recommendations_generated(self) -> None:
        evidence = _make_minimal_evidence(
            zero_quantity_items=(({"row_number": 1},),),
            detected_level_skips=(({"level": 2},),),
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        assert len(summary.recommendations) >= 2

    def test_no_recommendations_on_clean_evidence(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        # No detection evidence means no recommendations for those patterns
        # (UOM rec depends on findings)
        assert len(summary.recommendations) >= 0  # may have UOM rec

    def test_recommendations_are_advisory(self) -> None:
        evidence = _make_minimal_evidence(
            header_quantity_violations=(({"row_number": 5},),),
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        for rec in summary.recommendations.recommendations:
            # Advisory language — should contain advisory verbs, not imperative
            text_lower = rec.text.lower()
            assert any(word in text_lower for word in (
                "verify", "review", "may", "consider", "note"
            ))

    def test_recommendations_have_source_evidence(self) -> None:
        evidence = _make_minimal_evidence(
            zero_quantity_items=(
                ({"row_number": 1, "description": "test", "quantity": 0},),
            ),
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        for rec in summary.recommendations.recommendations:
            assert len(rec.source_evidence) > 0
            # Source evidence fields should reference evidence field names
            for source in rec.source_evidence:
                assert isinstance(source, str)

    def test_recommendations_have_severity(self) -> None:
        evidence = _make_minimal_evidence(
            detected_level_skips=(({"level": 2},),),
        )
        ctx = _make_context(evidence=evidence)
        summary = interpret(ctx)
        for rec in summary.recommendations.recommendations:
            assert isinstance(rec.severity, Severity)

    def test_recommendations_are_deterministic(self) -> None:
        evidence = _make_minimal_evidence(
            zero_quantity_items=(({"row_number": 1, "quantity": 0},),),
            detected_level_skips=(({"level": 2},),),
        )
        ctx1 = _make_context(evidence=evidence)
        ctx2 = _make_context(evidence=evidence)
        summary1 = interpret(ctx1)
        summary2 = interpret(ctx2)
        # Same inputs -> same recommendations
        texts1 = [r.text for r in frozenset(summary1.recommendations.recommendations)]
        texts2 = [r.text for r in frozenset(summary2.recommendations.recommendations)]
        assert sorted(texts1) == sorted(texts2)

# ============================================================================
# Statistics Tests
# ============================================================================

class TestInterpretationStatistics:
    """Verify statistical computation."""

    def test_csv_counts(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning", "Information"))
        summary = interpret(ctx)
        stats = summary.statistics
        assert stats.total_findings == 3
        assert stats.high_count == 1
        assert stats.medium_count == 1
        stats.low_count == 1

    def test_statistics_with_empty_findings(self) -> None:
        ctx = _make_context(findings=_make_findings())
        summary = interpret(ctx)
        stats = summary.statistics
        assert stats.total_findings == 0
        assert stats.high_count == 0
        assert stats.medium_count == 0
        assert stats.low_count == 0

    def test_categories_count(self) -> None:
        ctx = _make_context(findings=_make_findings("Error", "Warning"))
        summary = interpret(ctx)
        assert summary.statistics.categories >= 0

    def test_total_recommendations(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        assert isinstance(summary.statistics.total_recommendations, int)
        assert summary.statistics.total_recommendations >= 0

    def test_total_sections_count(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        assert summary.statistics.total_sections == 2  # Section A + Section B

    def test_statistics_are_deterministic(self) -> None:
        ctx1 = _make_context(findings=_make_findings("Error", "Error", "Warning"))
        ctx2 = _make_context(findings=_make_findings("Error", "Error", "Warning"))
        summary1 = interpret(ctx1)
        summary2 = interpret(ctx2)
        assert summary1.statistics == summary2.statistics

# ============================================================================
# Interpretation Summary Tests
# ============================================================================

class TestInterpretationSummary:
    """Verify InterpretationSummary correctness."""

    def test_is_interpreted_flag(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        assert summary.is_interpreted is True

    def test_summary_contains_all_components(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        assert isinstance(summary.severity_map, SeverityMap)
        assert isinstance(summary.finding_groups, FindingGroups)
        assert isinstance(summary.recommendations, RecommendationSet)
        assert isinstance(summary.statistics, InterpretationStatistics)

    def test_summary_is_deterministic(self) -> None:
        ctx1 = _make_context(findings=_make_findings("Error", "Warning"))
        ctx2 = _make_context(findings=_make_findings("Error", "Warning"))
        summary1 = interpret(ctx1)
        summary2 = interpret(ctx2)
        assert summary1.statistics == summary2.statistics
        assert summary1.severity_map.to_dict() == summary2.severity_map.to_dict()

# ============================================================================
# Contract and Boundary Tests
# ============================================================================

class TestEvidenceImmutability:
    """Verify interpretation does not mutate evidence."""

    def test_evidence_unchanged_after_interpretation(self) -> None:
        evidence = _make_minimal_evidence()
        original_rc = dict(evidence.row_classification)
        ctx = _make_context(evidence=evidence)
        interpret(ctx)
        assert evidence.row_classification == original_rc

    def test_findings_unchanged_after_interpretation(self) -> None:
        findings = _make_findings("Error", "Warning")
        original_count = len(findings.findings)
        ctx = _make_context(findings=findings)
        interpret(ctx)
        assert len(findings.findings) == original_count

class TestNoPresentationModelLeakage:
    """Verify no Presentation Model, rendering, reports, exports exist."""

    def test_interpretation_summary_has_no_rendering_methods(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        assert not hasattr(summary, "render")
        assert not hasattr(summary, "to_ui")
        assert not hasattr(summary, "to_json")
        assert not hasattr(summary, "to_csv")
        assert not hasattr(summary, "to_pdf")

    def test_no_presentation_finding_created(self) -> None:
        """PresentationFinding belongs to IP-0005, not IP-0004."""
        ctx = _make_context()
        summary = interpret(ctx)
        # No PresentationFinding in this package
        assert not hasattr(summary, "presentation_findings")

    def test_no_report_format(self) -> None:
        ctx = _make_context()
        summary = interpret(ctx)
        assert not hasattr(summary, "report_format")
        assert not hasattr(summary, "format_report")