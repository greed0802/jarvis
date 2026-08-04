"""EvaluationRunner for M11.0 — profile-driven execution of evaluators.

Per AC-5: Runner executes named quality profiles (smoke, regression, release, research).
Per AC-6: Runner distinguishes promotion gates from informational metrics.
"""

from __future__ import annotations

import time
from uuid import uuid4

from jarvis.evaluation.contracts import (
    EvaluationCase,
    EvaluationProvenance,
    EvaluationReport,
    EvaluationResult,
    Evaluator,
)
from jarvis.evaluation.datasets import GoldenDatasetLoader
from jarvis.evaluation.registry import EvaluationRegistry

# Quality profile configuration map
_PROFILES: dict[str, dict] = {
    "smoke": {
        "categories": ["EVA-1", "EVA-5"],
        "max_cases": 2,
        "gate_threshold": 0.95,
    },
    "regression": {
        "categories": ["EVA-1", "EVA-2", "EVA-3", "EVA-4", "EVA-5"],
        "max_cases": 10,
        "gate_threshold": 0.90,
    },
    "release": {
        "categories": ["EVA-1", "EVA-2", "EVA-3", "EVA-4", "EVA-5"],
        "max_cases": None,
        "gate_threshold": 0.92,
    },
    "research": {
        "categories": ["EVA-1", "EVA-2", "EVA-3", "EVA-4", "EVA-5"],
        "max_cases": None,
        "gate_threshold": 0.0,
    },
}

class EvaluationRunner:
    """Profile-driven evaluation runner.

    Args:
        registry: Social EvaluatorRegistry containing evaluator plugins.
        loader:   Optional GoldenDatasetLoader (uses defaults if not provided).
    """

    def __init__(
        self,
        registry: EvaluationRegistry,
        loader: GoldenDatasetLoader | None = None,
    ) -> None:
        self._registry = registry
        self._loader = loader or GoldenDatasetLoader()

    def run(
        self,
        profile_name: str = "smoke",
        platform_context: dict | None = None,
    ) -> EvaluationReport:
        """Execute evaluation using the named quality profile.

        Args:
            profile_name:      "smoke", "regression", "release", or "research".
            platform_context:  Pre-instantiated platform components.

        Returns:
            Immutable EvaluationReport.
        """
        if profile_name not in _PROFILES:
            raise ValueError(f"Unknown quality profile: {profile_name}. Available: {list(_PROFILES)}")

        profile = _PROFILES[profile_name]
        run_id = uuid4().hex[:12]

        # Collect evaluators matching profile categories
        evaluators: list[Evaluator] = []
        for category in profile["categories"]:
            evaluators.extend(self._registry.get_category(category))

        # Load and trim cases
        all_cases = self._loader.load_all_cases()
        max_cases = profile["max_cases"]
        cases = all_cases[:max_cases] if max_cases else all_cases

        # Build provenance
        provenance = EvaluationProvenance(
            framework_version="1.0.0",
            specification_version="ES-1100.1.0",
            dataset_version="baseline-1.0",
            target_platform_version="M10.6",
            execution_timestamp="2026-07-30T00:00:00Z",
        )

        # Execute evaluators per case
        import time
        domain_results: dict[str, tuple[EvaluationResult, ...]] = {}

        for evaluator in evaluators:
            results: list[EvaluationResult] = []
            for case in cases:
                start = time.time()
                result = evaluator.evaluate_case(case, platform_context)
                elapsed_ms = (time.time() - start) * 1000

                # Reconstruct to inject timing
                result_with_time = EvaluationResult(
                    case_id=result.case_id,
                    evaluator_id=result.evaluator_id,
                    metrics=result.metrics,
                    passed=result.passed,
                    execution_time_ms=elapsed_ms,
                )
                results.append(result_with_time)

            domain_results[evaluator.evaluator_id] = tuple(results)

        # Compute summary score
        all_passed: list[bool] = []
        for evaluator_results in domain_results.values():
            for r in evaluator_results:
                all_passed.append(r.passed)

        summary_score = sum(1 for p in all_passed if p) / max(len(all_passed), 1) if all_passed else 0.0
        gate_passed = summary_score >= profile["gate_threshold"]

        return EvaluationReport(
            run_id=run_id,
            provenance=provenance,
            profile_name=profile_name,
            summary_score=summary_score,
            promotion_gate_passed=gate_passed,
            domain_results={
                eid: tuple(results)
                for eid, results in domain_results.items()
            },
        )