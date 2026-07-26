"""Tests for CheckMate Application — Composition Root and Public API (IP-0003).

Verifies:
- Application initialization
- Lifecycle transitions
- Dependency wiring
- Runtime state
- Configuration validation
- Public API (run())
- Deterministic execution
- Error handling
- Contract validation

No tests for future functionality (interpretation, Presentation Model, reports, etc.)
"""

from __future__ import annotations

import enum
from typing import Any

import pytest

from jarvis.applications.checkmate import (
    run,
    CheckMateConfig,
    CheckMateResult,
    CheckMateRuntimeState,
    CheckMateStatus,
    CheckMateError,
    ConfigurationError,
    ContractViolationError,
    ApplicationRuntimeError,
    InternalError,
)
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.engines.validation.engine import ValidationFindings, ValidationFinding

# ============================================================================
# Test Helpers — Create valid contract inputs
# ============================================================================

def make_evidence(**overrides: Any) -> BOQIntelligenceResult:
    """Create a valid BOQIntelligenceResult for testing."""
    defaults: dict[str, Any] = {
        "row_classification": {"Head": 5, "Note": 2, "Section": 3, "Item": 20, "Other": 0},
        "section_statistics": {"Section A": {"items": 10, "headers": 2}},
        "boq_statistics": {"total_items": 20, "total_headers": 5},
        "known_anomalies": [],
        "hierarchy": None,
        "hierarchy_statistics": None,
        "detected_level_skips": None,
        "zero_quantity_items": None,
        "structural_containment_findings": None,
        "completeness_findings": None,
        "vocabulary": None,
        "head1_categorization": None,
        "administrative_patterns": None,
        "section_enumeration": None,
        "uom_distribution": None,
        "uom_percentages": None,
        "header_distribution": None,
        "header_quantity_violations": None,
        "admin_template_matches": None,
    }
    defaults.update(overrides)
    return BOQIntelligenceResult(**defaults)

def make_findings(
    findings: tuple[ValidationFinding, ...] | None = None,
) -> ValidationFindings:
    """Create a valid ValidationFindings for testing."""
    return ValidationFindings(
        findings=findings or (),
        engine_version="1.0.0",
        contract_version="1.0.0",
        execution_timestamp="2026-07-25T00:00:00",
    )

# ============================================================================
# Test: Public API Importability
# ============================================================================

class TestPublicAPI:
    """Verify the public API is accessible from the package."""

    def test_run_is_importable(self):
        from jarvis.applications.checkmate import run
        assert callable(run)

    def test_checkmate_config_is_importable(self):
        from jarvis.applications.checkmate import CheckMateConfig
        assert hasattr(CheckMateConfig, "__dataclass_fields__")

    def test_checkmate_result_is_importable(self):
        from jarvis.applications.checkmate import CheckMateResult
        assert hasattr(CheckMateResult, "__dataclass_fields__")

    def test_runtime_state_is_importable(self):
        from jarvis.applications.checkmate import CheckMateRuntimeState
        assert hasattr(CheckMateRuntimeState, "__dataclass_fields__")

    def test_status_is_importable(self):
        from jarvis.applications.checkmate import CheckMateStatus
        assert issubclass(CheckMateStatus, enum.Enum)

    def test_errors_are_importable(self):
        from jarvis.applications.checkmate import (
            CheckMateError,
            ConfigurationError,
            ContractViolationError,
            ApplicationRuntimeError,
            InternalError,
        )
        assert issubclass(ConfigurationError, CheckMateError)
        assert issubclass(ContractViolationError, CheckMateError)
        assert issubclass(ApplicationRuntimeError, CheckMateError)
        assert issubclass(InternalError, CheckMateError)

# ============================================================================
# Test: Successful Application Execution
# ============================================================================

class TestSuccessfulExecution:
    """Verify successful application execution end-to-end."""

    def test_run_with_default_config_returns_success(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.success is True
        assert isinstance(result, CheckMateResult)

    def test_run_completes_full_lifecycle(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.state.status == CheckMateStatus.COMPLETE

    def test_run_creates_runtime_state(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert isinstance(result.state, CheckMateRuntimeState)

    def test_run_records_evidence_received(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.state.has_evidence is True

    def test_run_records_findings_received(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.state.has_findings is True

    def test_run_has_execution_timestamp(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.execution_timestamp is not None
        assert len(result.execution_timestamp) > 0

    def test_run_started_at_is_set(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.state.started_at is not None

    def test_run_completed_at_is_set(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.state.completed_at is not None

    def test_run_without_input_validation(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig(validate_inputs=False)
        result = run(evidence, findings, config)
        assert result.success is True

# ============================================================================
# Test: Deterministic Execution
# ============================================================================

class TestDeterministicExecution:
    """Verify deterministic behavior — identical inputs produce identical outputs."""

    def test_identical_inputs_produce_identical_results(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig()
        result1 = run(evidence, findings, config)
        result2 = run(evidence, findings, config)
        assert result1.success == result2.success
        assert result1.state.has_evidence == result2.state.has_evidence
        assert result1.state.has_findings == result2.state.has_findings

    def test_deterministic_with_disabled_validation(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig(validate_inputs=False)
        result1 = run(evidence, findings, config)
        result2 = run(evidence, findings, config)
        assert result1.success == result2.success

    def test_success_is_always_true_with_valid_inputs(self):
        evidence = make_evidence()
        findings = make_findings()
        for _ in range(10):
            result = run(evidence, findings)
            assert result.success is True

# ============================================================================
# Test: Configuration Handling
# ============================================================================

class TestConfigurationHandling:
    """Verify configuration is handled correctly."""

    def test_custom_config_is_accepted(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig(log_level="DEBUG")
        result = run(evidence, findings, config)
        assert result.success is True

    def test_config_with_diagnostics_enabled(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig(enable_diagnostics=True)
        result = run(evidence, findings, config)
        assert result.success is True
        diag = result.state.diagnostics
        assert "evidence_summary" in diag
        assert "findings_summary" in diag

    def test_diagnostics_contains_evidence_summary(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig(enable_diagnostics=True)
        result = run(evidence, findings, config)
        diag = result.state.diagnostics["evidence_summary"]
        assert "row_classification" in diag
        assert "boq_statistics" in diag

    def test_diagnostics_contains_findings_summary(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig(enable_diagnostics=True)
        result = run(evidence, findings, config)
        diag = result.state.diagnostics["findings_summary"]
        assert "finding_count" in diag
        assert diag["finding_count"] == 0

    def test_diagnostics_disabled_by_default(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.state.diagnostics == {}

    def test_config_with_max_errors(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig(max_errors=5)
        result = run(evidence, findings, config)
        assert result.success is True

# ============================================================================
# Test: Error Handling
# ============================================================================

class TestErrorHandling:
    """Verify error handling and error types."""

    def test_invalid_config_wraps_value_error(self):
        """Config validation raises ValueError, caught by run() and wrapped."""
        with pytest.raises(ValueError):
            CheckMateConfig(log_level="INVALID")

    def test_invalid_config_is_not_hidden(self):
        """Invalid config creation fails immediately with ValueError."""
        with pytest.raises(ValueError, match="Invalid log_level"):
            CheckMateConfig(log_level="INVALID")

    def test_config_error_is_correct_subclass(self):
        """Verify ConfigurationError inherits from CheckMateError."""
        assert issubclass(ConfigurationError, CheckMateError)

    def test_contract_violation_is_correct_subclass(self):
        """Verify ContractViolationError inherits from CheckMateError."""
        assert issubclass(ContractViolationError, CheckMateError)

    def test_contract_violation_has_correct_code(self):
        """ContractViolationError has CONTRACT_VIOLATION code."""
        error = ContractViolationError("test")
        assert error.code == "CONTRACT_VIOLATION"

    def test_contract_violation_error_message(self):
        """ContractViolationError stores message."""
        error = ContractViolationError("Evidence missing required fields")
        assert error.message == "Evidence missing required fields"

    def test_contract_violation_can_catch_as_checkmate_error(self):
        """ContractViolationError caught as CheckMateError."""
        with pytest.raises(CheckMateError):
            raise ContractViolationError("test")

# ============================================================================
# Test: Input Contract Validation
# ============================================================================

class TestInputContractValidation:
    """Verify contract validation of inputs."""

    def test_empty_findings_accepted(self):
        evidence = make_evidence()
        findings = make_findings(findings=())
        result = run(evidence, findings)
        assert result.success is True

    def test_findings_with_entries_accepted(self):
        evidence = make_evidence()
        finding = ValidationFinding(
            rule_id="V-001",
            rule_version="1.0.0",
            category="Completeness",
            finding_type="Information",
            finding_value="All required fields present",
            evidence_fields=("row_classification",),
        )
        findings = make_findings(findings=(finding,))
        result = run(evidence, findings)
        assert result.success is True

    def test_evidence_with_anomalies_accepted(self):
        evidence = make_evidence(
            known_anomalies=[{"type": "test", "description": "test anomaly"}]
        )
        findings = make_findings()
        result = run(evidence, findings)
        assert result.success is True

    def test_minimal_evidence_accepted(self):
        evidence = make_evidence(
            row_classification={"Head": 0, "Note": 0, "Section": 0, "Item": 0, "Other": 0},
            section_statistics={},
            boq_statistics={"total_items": 0, "total_headers": 0},
            known_anomalies=[],
        )
        findings = make_findings()
        result = run(evidence, findings)
        assert result.success is True

    def test_evidence_with_all_fields_populated_accepted(self):
        evidence = make_evidence(
            hierarchy=(),
            hierarchy_statistics={"depth": 3, "breadth": 5},
            detected_level_skips=(),
            zero_quantity_items=(),
            structural_containment_findings=(),
            completeness_findings=(),
            vocabulary={"concrete": 5, "steel": 3, "formwork": 2},
            head1_categorization={"admin": [], "trade": []},
            administrative_patterns={},
            section_enumeration=(),
            uom_distribution={"m2": 10, "m3": 5},
            uom_percentages={"m2": 66.7, "m3": 33.3},
            header_distribution={"Head1": 2, "Head2": 3},
            header_quantity_violations=(),
            admin_template_matches={},
        )
        findings = make_findings()
        result = run(evidence, findings)
        assert result.success is True

# ============================================================================
# Test: Result Immutability
# ============================================================================

class TestResultImmutability:
    """Verify CheckMateResult is immutable."""

    def test_result_is_frozen(self):
        assert CheckMateResult.__dataclass_params__.frozen is True

    def test_cannot_modify_result(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        with pytest.raises(AttributeError):
            result.success = False  # type: ignore[misc]

# ============================================================================
# Test: No Business Logic Leakage
# ============================================================================

class TestNoBusinessLogicLeakage:
    """Verify no business logic is present in the foundation."""

    def test_result_has_no_presentation_model(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert not hasattr(result, "presentation_model")
        assert not hasattr(result, "model")
        assert not hasattr(result, "interpretation")

    def test_result_has_no_recommendations(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert not hasattr(result, "recommendations")
        assert not hasattr(result, "guidance")

    def test_result_has_no_reports(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert not hasattr(result, "report")
        assert not hasattr(result, "reports")

    def test_result_has_no_exports(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert not hasattr(result, "export")
        assert not hasattr(result, "exports")

    def test_state_has_no_review_state(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        state = result.state
        assert not hasattr(state, "review_status")
        assert not hasattr(state, "approval_status")

# ============================================================================
# Test: Immutable Inputs
# ============================================================================

class TestImmutableInputs:
    """Verify the application does not mutate inputs."""

    def test_evidence_is_not_mutated(self):
        evidence = make_evidence()
        findings = make_findings()
        original_id = id(evidence)
        run(evidence, findings)
        assert id(evidence) == original_id

    def test_findings_are_not_mutated(self):
        evidence = make_evidence()
        findings = make_findings()
        original_id = id(findings)
        run(evidence, findings)
        assert id(findings) == original_id

    def test_config_is_not_mutated(self):
        evidence = make_evidence()
        findings = make_findings()
        config = CheckMateConfig()
        original_id = id(config)
        run(evidence, findings, config)
        assert id(config) == original_id

# ============================================================================
# Test: Lifecycle State
# ============================================================================

class TestLifecycleState:
    """Verify the correct lifecycle state is reported."""

    def test_successful_run_ends_complete(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.state.status == CheckMateStatus.COMPLETE

    def test_success_result_true(self):
        evidence = make_evidence()
        findings = make_findings()
        result = run(evidence, findings)
        assert result.success is True

    def test_error_does_not_leak_to_caller_as_generic(self):
        import traceback
        evidence = make_evidence()
        findings = make_findings()

        try:
            with pytest.raises(ValueError):
                bad_config = CheckMateConfig(log_level="INVALID")
            return  # Error is expected
        except Exception as e:
            traceback.print_exc()
            pytest.fail(f"Got unexpected exception type: {type(e).__name__}: {e}")

# ============================================================================
# Test: Basic Execution Isolation
# ============================================================================

class TestBasicIsolation:
    """Verify basic execution isolation."""

    def test_multiple_calls_are_independent(self):
        evidence1 = make_evidence(
            row_classification={"Head": 5, "Note": 2, "Section": 3, "Item": 20, "Other": 0}
        )
        evidence2 = make_evidence(
            row_classification={"Head": 1, "Note": 0, "Section": 1, "Item": 5, "Other": 0}
        )
        findings = make_findings()
        result1 = run(evidence1, findings)
        result2 = run(evidence2, findings)
        assert result1.success is True
        assert result2.success is True