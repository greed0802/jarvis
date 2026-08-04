"""Immutable evaluation contracts for M11.0 Capability Evaluation Framework.

Defines the EvaluationMetric, EvaluationCase, EvaluationResult,
EvaluationProvenance, and EvaluationReport frozen dataclasses along with
the Evaluator Protocol interface.

Per AC-4: EvaluationProvenance is embedded in every EvaluationReport.
Per AC-9: No production runtime module may import this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

# =============================================================================
# EvaluationMetric
# =============================================================================

@dataclass(frozen=True)
class EvaluationMetric:
    """A single measured metric from an evaluation run.

    Attributes:
        name:              Human-readable metric name.
        category:          Evaluator domain (e.g., "EVA-1" through "EVA-5").
        value:             Observed numeric value.
        threshold:         Minimum acceptable threshold for promotion gates.
        is_promotion_gate: True if this metric is a pass/fail promotion gate.
        passed:            True if value meets threshold (or is not a gate).
    """

    name: str
    category: str
    value: float
    threshold: float = 0.0
    is_promotion_gate: bool = False
    passed: bool = True

    def __post_init__(self) -> None:
        """Derive pass status after construction on a frozen dataclass."""
        if self.is_promotion_gate:
            object.__setattr__(self, "passed", self.value >= self.threshold)

# =============================================================================
# EvaluationCase
# =============================================================================

@dataclass(frozen=True)
class EvaluationCase:
    """A single golden evaluation case.

    Each case carries explicit input artifacts and expected outputs
    for metric comparison.

    Attributes:
        case_id:           Unique case identifier.
        dataset_name:      Parent dataset name (e.g., "boq_baseline").
        input_artifacts:   Arbitrary input data for evaluation.
        expected_outputs:  Expected outputs for metric comparison.
    """

    case_id: str
    dataset_name: str
    input_artifacts: dict[str, Any] = field(default_factory=dict)
    expected_outputs: dict[str, Any] = field(default_factory=dict)

# =============================================================================
# EvaluationResult
# =============================================================================

@dataclass(frozen=True)
class EvaluationResult:
    """Result of a single evaluation case executed by a specific evaluator.

    Attributes:
        case_id:           The case identifier.
        evaluator_id:      Unique ID of the producing evaluator.
        metrics:           Tuple of all metrics measured for this case.
        passed:            True if all promotion-gate metrics passed.
        execution_time_ms: Wall-clock evaluation time in milliseconds.
    """

    case_id: str
    evaluator_id: str
    metrics: tuple[EvaluationMetric, ...] = field(default_factory=tuple)
    passed: bool = True
    execution_time_ms: float = 0.0

    def __post_init__(self) -> None:
        """Derive overall pass from promotion gate metrics."""
        gates = [m for m in self.metrics if m.is_promotion_gate]
        if gates:
            all_passed = all(m.passed for m in gates)
            object.__setattr__(self, "passed", all_passed)

# =============================================================================
# EvaluationProvenance
# =============================================================================

@dataclass(frozen=True)
class EvaluationProvenance:
    """Provenance metadata embedded in every EvaluationReport.

    Attributes:
        framework_version:       Evaluation framework version string.
        specification_version:  ES-1100 specification version.
        dataset_version:        Golden dataset version.
        target_platform_version: Target platform version (e.g., M10.6).
        execution_timestamp:    ISO-8601 timestamp of execution start.
    """

    framework_version: str
    specification_version: str
    dataset_version: str
    target_platform_version: str
    execution_timestamp: str = ""

# =============================================================================
# EvaluationReport
# =============================================================================

@dataclass(frozen=True)
class EvaluationReport:
    """Complete evaluation report for a single evaluation run.

    Attributes:
        run_id:               Unique hex string identifying this run.
        provenance:           Complete version and provenance metadata.
        profile_name:         Quality profile used (smoke, regression, release, research).
        Summary_score:        Aggregate score across all evaluators.
        promotion_gate_passed: True if all promotion gates passed.
        domain_results:        Per-domain per-case EvaluationResult tuples keyed by evaluator_id.
        report_metadata:       Extended metadata for exporters.
    """

    run_id: str
    provenance: EvaluationProvenance
    profile_name: str
    summary_score: float = 0.0
    promotion_gate_passed: bool = True
    domain_results: dict[str, tuple[EvaluationResult, ...]] = field(default_factory=dict)
    report_metadata: dict[str, Any] = field(default_factory=dict)

# =============================================================================
# Evaluator Protocol
# =============================================================================

@runtime_checkable
class Evaluator(Protocol):
    """Protocol for evaluator plugins discoverable by the EvaluationRegistry.

    Each evaluator is identified by an evaluator_id and category (EVA-1 through
    EVA-5). The evaluate_case method evaluates a single golden case against
    platform context and returns an immutable EvaluationResult.

    Properties:
        evaluator_id:        Unique stable identifier.
        category:            Domain category ("EVA-1" through "EVA-5").
        supported_metrics:   Names of metrics this evaluator measures.
    """

    @property
    def evaluator_id(self) -> str:
        """Return the unique stable identifier for this evaluator."""
        ...

    @property
    def category(self) -> str:
        """Return the domain category (EVA-1 through EVA-5)."""
        ...

    @property
    def supported_metrics(self) -> list[str]:
        """Return the list of metric names this evaluator measures."""
        ...

    def evaluate_case(
        self,
        case: EvaluationCase,
        platform_context: dict[str, Any] | None = None,
    ) -> EvaluationResult:
        """Evaluate a single golden case against the platform context.

        Args:
            case: The golden EvaluationCase to evaluate.
            platform_context: Optional pre-built platform components.

        Returns:
            EvaluationResult with metrics, thresholds, and pass/fail status.
        """
        ...