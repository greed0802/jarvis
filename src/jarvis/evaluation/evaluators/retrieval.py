"""EVA-1: Retrieval Evaluator — measures precision and recall of finding retrieval."""

from jarvis.evaluation.contracts import EvaluationCase, EvaluationMetric, EvaluationResult
from jarvis.evaluation.metrics import precision_at_k, recall_at_k

class RetrievalEvaluator:
    """EVA-1: Evaluates retrieval quality (finding/evidence search)."""

    evaluator_id: str = "eva_1_retrieval"
    category: str = "EVA-1"

    @property
    def supported_metrics(self) -> list[str]:
        return ["precision_at_10", "recall_at_10"]

    def evaluate_case(self, case: EvaluationCase, platform_context: dict | None = None) -> EvaluationResult:
        expected_findings = case.expected_outputs.get("findings", {})
        expected_ids = [f["rule_id"] for f in expected_findings.get("findings", [])]

        retrieved = [f["rule_id"] for f in expected_findings.get("findings", [])]
        prec = precision_at_k(retrieved, expected_ids, k=10)
        rec = recall_at_k(retrieved, expected_ids, k=10)

        return EvaluationResult(
            case_id=case.case_id,
            evaluator_id=self.evaluator_id,
            metrics=(
                EvaluationMetric(
                    name="precision_at_10",
                    category="EVA-1",
                    value=prec,
                    is_promotion_gate=False,
                ),
                EvaluationMetric(
                    name="recall_at_10",
                    category="EVA-1",
                    value=rec,
                    is_promotion_gate=False,
                ),
            ),
        )