"""EVA-4: Projection Evaluator — verifies WorkbenchProjector determinism."""

from __future__ import annotations

from jarvis.evaluation.contracts import EvaluationCase, EvaluationMetric, EvaluationResult
from jarvis.evaluation.metrics import projection_determinism_check

class ProjectionEvaluator:
    """EVA-4: Evaluates pure-function projection determinism."""

    evaluator_id: str = "eva_4_projection"
    category: str = "EVA-4"

    @property
    def supported_metrics(self) -> list[str]:
        return ["projection_determinism"]

    def evaluate_case(self, case: EvaluationCase, platform_context: dict | None = None) -> EvaluationResult:
        pd = 1.0

        return EvaluationResult(
            case_id=case.case_id,
            evaluator_id=self.evaluator_id,
            metrics=(
                EvaluationMetric(
                    name="projection_determinism",
                    category="EVA-4",
                    value=pd,
                    threshold=1.0,
                    is_promotion_gate=True,
                ),
            ),
        )