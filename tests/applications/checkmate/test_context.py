"""Tests for CheckMate ApplicationContext (IP-0004).

Verifies:
- ApplicationContext immutability
- ApplicationContext construction
- Runtime ID uniqueness
- Evidence immutability
- Findings immutability
- No Presentation Model
- No business logic
"""

from __future__ import annotations

from datetime import datetime

import pytest

from jarvis.applications.checkmate.config import CheckMateConfig
from jarvis.applications.checkmate.context import ApplicationContext
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding


def _make_minimal_evidence() -> BOQIntelligenceResult:
    """Create minimal valid evidence for testing."""
    return BOQIntelligenceResult(
        row_classification={"Head": 5, "Item": 10},
        section_statistics={"Section A": {"items": 10, "page": 1}},
        boq_statistics={"total_rows": 15, "total_sections": 1},
        known_anomalies=[],
    )


def _make_minimal_findings() -> ValidationFindings:
    """Create minimal valid findings for testing."""
    return ValidationFindings(
        findings=(
            ValidationFinding(
                rule_id="V-001",
                rule_version="1.0.0",
                category="Contract Enforcement",
                finding_type="Error",
                finding_value=0,
                evidence_fields=("row_classification", "section_statistics", "boq_statistics", "known_anomalies"),
            ),
        ),
        engine_version="1.0.0",
        contract_version="1.0.0",
        execution_timestamp="2026-07-25T00:00:00+00:00",
    )


class TestApplicationContextConstruction:
    """Verify ApplicationContext construction."""

    def test_constructs_with_valid_inputs(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert ctx.evidence is evidence
        assert ctx.findings is findings
        assert ctx.runtime_id is not None
        assert len(ctx.runtime_id) > 0
        assert ctx.application_version == "0.0.1-alpha.14"

    def test_constructs_with_custom_config(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        config = CheckMateConfig(log_level="DEBUG", enable_diagnostics=True)
        ctx = ApplicationContext(evidence=evidence, findings=findings, config=config)
        assert ctx.config == config
        assert ctx.enable_diagnostics is True

    def test_runtime_id_is_unique(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx1 = ApplicationContext(evidence=evidence, findings=findings)
        ctx2 = ApplicationContext(evidence=evidence, findings=findings)
        assert ctx1.runtime_id != ctx2.runtime_id

    def test_execution_timestamp_is_set(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert ctx.execution_timestamp is not None
        assert len(ctx.execution_timestamp) > 0
        # Should be parseable as ISO 8601
        datetime.fromisoformat(ctx.execution_timestamp)

    def test_enable_diagnostics_defaults_to_config(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        # Default config has enable_diagnostics=False
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert ctx.enable_diagnostics is False

    def test_enable_diagnostics_when_config_enables(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        config = CheckMateConfig(enable_diagnostics=True)
        ctx = ApplicationContext(evidence=evidence, findings=findings, config=config)
        assert ctx.enable_diagnostics is True


class TestApplicationContextImmutability:
    """Verify ApplicationContext is immutable."""

    def test_context_is_frozen(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        with pytest.raises(Exception):
            ctx.evidence = _make_minimal_evidence()  # type: ignore[misc]

    def test_cannot_modify_runtime_id(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        with pytest.raises(Exception):
            ctx.runtime_id = "new-id"  # type: ignore[misc]

    def test_cannot_modify_version(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        with pytest.raises(Exception):
            ctx.application_version = "0.0.2"  # type: ignore[misc]

    def test_cannot_add_attribute(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        with pytest.raises(Exception):
            ctx.new_field = "value"  # type: ignore[misc]


class TestApplicationContextBoundaries:
    """Verify ApplicationContext has no Presentation Model, reports, etc."""

    def test_no_presentation_model_fields(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        # Should not have presentation-related fields
        assert not hasattr(ctx, "presentation_findings")
        assert not hasattr(ctx, "presentation_sections")
        assert not hasattr(ctx, "presentation_summary")
        assert not hasattr(ctx, "presentation_recommendations")

    def test_no_review_state(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert not hasattr(ctx, "review_status")
        assert not hasattr(ctx, "accepted_set")
        assert not hasattr(ctx, "rejected_set")

    def test_no_export_state(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert not hasattr(ctx, "export_format")
        assert not hasattr(ctx, "export_path")

    def test_to_dict_contains_metadata(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        d = ctx.to_dict()
        assert "runtime_id" in d
        assert "application_version" in d
        assert "execution_timestamp" in d
        assert "config" in d
        # Evidence and findings themselves should not be in the dict
        assert "evidence" not in d
        assert "findings" not in d


class TestEvidenceImmutabilityPreserved:
    """Verify evidence and findings remain immutable within context."""

    def test_evidence_field_types_preserved(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert isinstance(ctx.evidence, BOQIntelligenceResult)
        assert isinstance(ctx.evidence.row_classification, dict)
        assert isinstance(ctx.evidence.section_statistics, dict)

    def test_findings_field_types_preserved(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert isinstance(ctx.findings, ValidationFindings)
        assert len(ctx.findings.findings) > 0
        assert isinstance(ctx.findings.findings[0], ValidationFinding)

    def test_evidence_not_altered_by_context(self) -> None:
        evidence = _make_minimal_evidence()
        original_rc = dict(evidence.row_classification)
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        # Evidence should be exactly the same object (not copied)
        assert ctx.evidence is evidence
        assert ctx.evidence.row_classification == original_rc

    def test_findings_not_altered_by_context(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        original_count = len(findings.findings)
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert ctx.findings is findings
        assert len(ctx.findings.findings) == original_count


class TestConfigurationPropagation:
    """Verify config values properly propagate to context."""

    def test_default_config(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        ctx = ApplicationContext(evidence=evidence, findings=findings)
        assert ctx.config.log_level == "INFO"
        assert ctx.config.validate_inputs is True
        assert ctx.config.enable_diagnostics is False
        assert ctx.config.max_errors == 10

    def test_custom_config(self) -> None:
        evidence = _make_minimal_evidence()
        findings = _make_minimal_findings()
        config = CheckMateConfig(
            log_level="WARNING",
            validate_inputs=False,
            enable_diagnostics=True,
            max_errors=5,
        )
        ctx = ApplicationContext(evidence=evidence, findings=findings, config=config)
        assert ctx.config.log_level == "WARNING"
        assert ctx.config.validate_inputs is False
        assert ctx.config.enable_diagnostics is True
        assert ctx.config.max_errors == 5
        assert ctx.enable_diagnostics is True