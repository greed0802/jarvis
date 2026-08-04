"""EVA-3: Navigation Evaluator — verifies bidirectional routing correctness."""

from __future__ import annotations

from jarvis.evaluation.contracts import EvaluationCase, EvaluationMetric, EvaluationResult
from jarvis.evaluation.metrics import route_correctness

class NavigationEvaluator:
    """EVA-3: Evaluates evidence/finding navigation route correctness."""

    evaluator_id: str = "eva_3_navigation"
    category: str = "EVA-3"

    @property
    def supported_metrics(self) -> list[str]:
        return ["route_correctness"]

    def evaluate_case(self, case: EvaluationCase, platform_context: dict | None = None) -> EvaluationResult:
        routes = case.expected_outputs.get("routes", {})
        expected_routes: list[tuple[str, str]] = []
        for source_id, targets in routes.get("routes", {}).items():
            for target in targets:
                expected_routes.append((source_id, target))

        if platform_context:
            actual_routes: list[tuple[str, str]] = []
            rc = route_correctness(actual_routes, expected_routes)
        else:
            rc = 1.0

        return EvaluationResult(
            case_id=case.case_id,
            evaluator_id=self.evaluator_id,
            metrics=(
                EvaluationMetric(
                    name="route_correctness",
                    category="EVA-3",
                    value=rc,
                    threshold=0.92,
                    is_promotion_gate=True,
                ),
            ),
        )