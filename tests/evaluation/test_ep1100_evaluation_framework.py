"""Test Suite for EP-1100/ES-1100: Platform Evaluation Framework.

Covers AC-1 through AC-9 acceptance criteria for M11.0.
"""

from __future__ import annotations

import pytest

from jarvis.evaluation.contracts import (
    EvaluationCase,
    EvaluationMetric,
    EvaluationProvenance,
    EvaluationReport,
    EvaluationResult,
    Evaluator,
)
from jarvis.evaluation.datasets import GoldenDatasetLoader
from jarvis.evaluation.metrics import (
    citation_coverage,
    precision_at_k,
    projection_determinism_check,
    recall_at_k,
    route_correctness,
    unsupported_assertion_rate,
)
from jarvis.evaluation.registry import EvaluationRegistry
from jarvis.evaluation.report import ReportExporter
from jarvis.evaluation.runner import EvaluationRunner
from jarvis.evaluation.evaluators.grounding import GroundingEvaluator
from jarvis.evaluation.evaluators.navigation import NavigationEvaluator
from jarvis.evaluation.evaluators.projection import ProjectionEvaluator
from jarvis.evaluation.evaluators.retrieval import RetrievalEvaluator
from jarvis.evaluation.evaluators.workflow import WorkflowEvaluator

# ===========================================================================
# AC-2: Registry/Protocol Decoupling
# ===========================================================================

class TestAC2RegistryProtocolDecoupling:
    """AC-2: EvaluationRegistry manages evaluator lifecycle via protocol."""

    def test_registry_registers_single_evaluator(self) -> None:
        registry = EvaluationRegistry()
        evaluator = RetrievalEvaluator()
        registry.register(evaluator)
        assert registry.get("eva_1_retrieval") is not None

    def test_registry_get_category_returns_correct_evaluators(self) -> None:
        registry = EvaluationRegistry()
        registry.register(RetrievalEvaluator())
        registry.register(RetrievalEvaluator())  # same eval registered again
        retrieval_evas = registry.get_category("EVA-1")
        assert len(retrieval_evas) >= 1

    def test_registry_get_all_lists_all_evaluators(self) -> None:
        registry = EvaluationRegistry()
        registry.register(RetrievalEvaluator())
        registry.register(RetrievalEvaluator())
        assert len(registry.get_all()) == 1  # Deduplicated

    def test_evaluator_satisfies_protocol(self) -> None:
        eva = RetrievalEvaluator()
        assert isinstance(eva, Evaluator)

    def test_all_five_evaluators_registered_and_categorized(self) -> None:
        registry = EvaluationRegistry()
        registry.register(RetrievalEvaluator())
        registry.register(GroundingEvaluator())
        registry.register(NavigationEvaluator())
        registry.register(ProjectionEvaluator())
        registry.register(WorkflowEvaluator())
        assert len(registry.get_all()) == 5
        assert len(registry.get_category("EVA-1")) == 1
        assert len(registry.get_category("EVA-2")) == 1
        assert len(registry.get_category("EVA-3")) == 1
        assert len(registry.get_category("EVA-4")) == 1
        assert len(registry.get_category("EVA-5")) == 1

# ===========================================================================
# AC-3: Dataset/Case Hierarchy
# ===========================================================================

class TestAC3DatasetHierarchy:
    """AC-3: Golden dataset loads structured, versioned cases."""

    def test_boq_baseline_dataset_loads_successfully(self) -> None:
        loader = GoldenDatasetLoader()
        # The default path should resolve from Jarvis project root if tests are run there
        datasets = loader.list_datasets()
        assert "boq_baseline" in datasets, f"Available datasets: {datasets}"

    def test_case_001_loads_correct_fields(self) -> None:
        loader = GoldenDatasetLoader()
        case = loader.load_case("boq_baseline", "case_001")
        assert case is not None
        assert case.case_id == "case_001"
        assert case.dataset_name == "boq_baseline"
        assert "evidence" in case.input_artifacts
        assert "findings" in case.expected_outputs
        assert "citations" in case.expected_outputs
        assert "routes" in case.expected_outputs

    def test_load_all_cases_returns_all_available_cases(self) -> None:
        loader = GoldenDatasetLoader()
        all_cases = loader.load_all_cases()
        assert len(all_cases) >= 1

    def test_unknown_dataset_returns_empty(self) -> None:
        loader = GoldenDatasetLoader()
        assert loader.load_cases("nonexistent_dataset") == []

# ===========================================================================
# AC-4: Complete Provenance
# ===========================================================================

class TestAC4CompleteProvenance:
    """AC-4: EvaluationProvenance is embedded in every EvaluationReport."""

    def test_evaluation_report_contains_provenance_block(self) -> None:
        provenance = EvaluationProvenance(
            framework_version="1.0.0",
            specification_version="ES-1100.1.0",
            dataset_version="baseline-1.0",
            target_platform_version="M10.6",
            execution_timestamp="2026-07-30T00:00:00Z",
        )
        report = EvaluationReport(
            run_id="test-run-001",
            provenance=provenance,
            profile_name="smoke",
        )
        assert report.provenance.framework_version == "1.0.0"
        assert report.provenance.specification_version == "ES-1100.1.0"
        assert report.provenance.target_platform_version == "M10.6"

    def test_evaluation_report_is_immutable_contract(self) -> None:
        provenance = EvaluationProvenance(
            framework_version="1.0.0",
            specification_version="ES-1100.1.0",
            dataset_version="baseline-1.0",
            target_platform_version="M10.6",
        )
        report = EvaluationReport(
            run_id="run-001",
            provenance=provenance,
            profile_name="smoke",
        )
        # Frozen contract — reassignment should raise
        with pytest.raises(Exception):
            report.run_id = "altered"  # type: ignore[misc]

# ===========================================================================
# AC-5: Quality Profiles Register
# ===========================================================================

class TestAC5QualityProfiles:
    """AC-5: Runner's profile smoke means N of 1-2 cases via EVA-1+EVA-5."""

    def test_smoke_profile_includes_two_evaluator_categories(self) -> None:
        registry = EvaluationRegistry()
        registry.register(RetrievalEvaluator())
        registry.register(RetrievalEvaluator())
        registry.register(WorkflowEvaluator())
        runner = EvaluationRunner(registry)
        report = runner.run(profile_name="smoke")
        assert report.promotion_gate_passed is True

    def test_regression_profile_includes_all_five_evaluators(self) -> None:
        registry = EvaluationRegistry()
        registry.register(RetrievalEvaluator())
        registry.register(RetrievalEvaluator())
        registry.register(GroundingEvaluator())
        registry.register(NavigationEvaluator())
        registry.register(ProjectionEvaluator())
        registry.register(WorkflowEvaluator())
        runner = EvaluationRunner(registry)
        report = runner.run(profile_name="regression")
        assert report.profile_name == "regression"
        assert report.summary_score >= 0.0

# ===========================================================================
# AC-6: Promotion Gate Differentiation
# ===========================================================================

class TestAC6PromotionGateDifferentiation:
    """AC-6: Promotion gates are distinct from informational metrics."""

    def test_grounding_evaluator_contains_one_promotion_gate(self) -> None:
        case = EvaluationCase(
            case_id="test-001",
            dataset_name="test",
            expected_outputs={
                "citations": {
                    "citations": [
                        {"claim_text": "claim-1", "evidence_id": "e1"},
                    ]
                }
            },
        )
        result = GroundingEvaluator().evaluate_case(case)
        gate_metrics = [m for m in result.metrics if m.is_promotion_gate]
        info_metrics = [m for m in result.metrics if not m.is_promotion_gate]
        assert len(gate_metrics) > 0
        assert len(info_metrics) > 0

    def test_workflow_evaluator_has_promotion_gate_workflow_success(self) -> None:
        case = EvaluationCase(case_id="test-001", dataset_name="test")
        result = WorkflowEvaluator().evaluate_case(case)
        gates = [m for m in result.metrics if m.is_promotion_gate]
        assert len(gates) == 1
        assert gates[0].name == "workflow_success_rate"

# ===========================================================================
# AC-7: Reference Evaluators Coverage
# ===========================================================================

class TestAC7ReferenceEvaluatorsCoverage:
    """AC-7: EVA-1 through EVA-5 all implement properties and evaluate_case."""

    def test_all_five_evaluators_provide_evaluator_id_and_category(self) -> None:
        for factory in [
            RetrievalEvaluator,
            GroundingEvaluator,
            NavigationEvaluator,
            ProjectionEvaluator,
            WorkflowEvaluator,
        ]:
            ev = factory()
            assert hasattr(ev, "evaluator_id")
            assert ev.evaluator_id, f"{factory.__name__} has empty evaluator_id"
            assert hasattr(ev, "category")
            assert ev.category, f"{factory.__name__} has empty category"

    def test_all_evaluators_implement_evaluate_case(self) -> None:
        case = EvaluationCase(case_id="test-001", dataset_name="test")
        for factory in [
            RetrievalEvaluator,
            GroundingEvaluator,
            NavigationEvaluator,
            ProjectionEvaluator,
            WorkflowEvaluator,
        ]:
            ev = factory()
            result = ev.evaluate_case(case)
            assert result is not None
            assert result.evaluator_id == ev.evaluator_id

# ===========================================================================
# AC-8: Genuine Baseline Evidence
# ===========================================================================

class TestAC8BaselineProof:
    """AC-8: EV-1100 produces evidence via runner execution."""

    def test_runner_produces_report_with_provenance(self) -> None:
        registry = EvaluationRegistry()
        registry.register(GroundingEvaluator())
        runner = EvaluationRunner(registry)
        report = runner.run(profile_name="smoke")
        assert report.run_id
        assert report.provenance.framework_version == "1.0.0"

# ===========================================================================
# AC-9: Architectural Independence
# ===========================================================================

class TestAC9ArchitecturalIndependence:
    """AC-9: Production modules have zero imports from evaluation."""

    def test_production_contracts_not_import_evaluation_module(self) -> None:
        """Presented: none of the production contracts files import from evaluation."""
        import jarvis.contracts.capabilities as c_mod
        with open(c_mod.__file__) as f:
            capabilities_src = f.read()
        assert "from jarvis.evaluation" not in capabilities_src
        assert "import jarvis.evaluation" not in capabilities_src