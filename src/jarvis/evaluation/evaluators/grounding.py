"""EVA-2: Grounding Evaluator — measures citation coverage and unsupported assertions."""

from __future__ import annotations

from jarvis.evaluation.contracts import EvaluationCase, EvaluationMetric, EvaluationResult
from jarvis.evaluation.metrics import citation_coverage, unsupported_assertion_rate

class GroundingEvaluator:
    """EVA-2: Evaluates citation grounding quality against golden data."""

    evaluator_id: str = "eva_2_grounding"
    category: str = "EVA-2"

    @property
    def supported_metrics(self) -> list[str]:
        return ["citation_coverage", "unsupported_assertion_rate"]

    def evaluate_case(
        self, case: EvaluationCase, platform_context: dict | None = None
    ) -> EvaluationResult:
        citations_data = case.expected_outputs.get("citations", {})
        cites = citations_data.get("citations", [])
        claim_texts = [c["claim_text"] for c in cites]
        cite_ids = [c["evidence_id"] for c in cites]

        cc = citation_coverage(claim_texts, cite_ids)
        uar = unsupported_assertion_rate(claim_texts, cite_ids)

        return EvaluationResult(
            case_id=case.case_id,
            evaluator_id=self.evaluator_id,
            metrics=(
                EvaluationMetric(
                    name="citation_coverage",
                    category="EVA-2",
                    value=cc,
                    threshold=0.85,
                    is_promotion_gate=False,
                ),
                EvaluationMetric(
                    name="unsupported_assertion_rate",
                    category="EVA-2",
                    value=uar,
                    threshold=0.15,
                    is_promotion_gate=True,
                ),
            ),
        )