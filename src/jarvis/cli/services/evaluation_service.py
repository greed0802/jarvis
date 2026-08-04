"""EvaluationService facade for EvaluationRunner (M11.0)."""

from __future__ import annotations

from jarvis.evaluation.registry import EvaluationRegistry
from jarvis.evaluation.runner import EvaluationRunner
from jarvis.evaluation.evaluators.grounding import GroundingEvaluator
from jarvis.evaluation.evaluators.navigation import NavigationEvaluator
from jarvis.evaluation.evaluators.projection import ProjectionEvaluator
from jarvis.evaluation.evaluators.retrieval import RetrievalEvaluator
from jarvis.evaluation.evaluators.workflow import WorkflowEvaluator

class EvaluationService:
    """Facade over EvaluationRunner for headless evaluation execution.

    Commands MUST import this service, NEVER the runner directly.
    """

    def __init__(self) -> None:
        registry = EvaluationRegistry()
        registry.register(RetrievalEvaluator())
        registry.register(GroundingEvaluator())
        registry.register(NavigationEvaluator())
        registry.register(ProjectionEvaluator())
        registry.register(WorkflowEvaluator())
        self._runner = EvaluationRunner(registry)

    def run_profile(self, profile_name: str = "smoke") -> dict:
        """Execute evaluation against a specific profile.

        Args:
            profile_name: One of smoke, regression, release, research.

        Returns:
            dict with run_id, profile_name, summary_score, promotion_gate_passed, and domain_results summary.

        Raises:
            ValueError: If profile_name is invalid (maps to exit code 2).
            RuntimeError: If dataset loading fails (maps to exit code 4).
        """
        try:
            report = self._runner.run(profile_name=profile_name)
        except ValueError as exc:
            raise ValueError(str(exc))
        except FileNotFoundError as exc:
            raise RuntimeError(f"Dataset load failed: {exc}")
        except Exception as exc:
            raise RuntimeError(f"Evaluation failed: {exc}")

        return {
            "run_id": report.run_id,
            "profile_name": report.profile_name,
            "summary_score": report.summary_score,
            "promotion_gate_passed": report.promotion_gate_passed,
            "evaluator_count": len(report.domain_results),
            "cases_evaluated": sum(len(v) for v in report.domain_results.values()),
            "provenance": {
                "framework_version": report.provenance.framework_version,
                "target_platform_version": report.provenance.target_platform_version,
            },
        }