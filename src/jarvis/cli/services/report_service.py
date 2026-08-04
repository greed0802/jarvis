"""ReportService facade for evaluation report export."""

from __future__ import annotations

from jarvis.evaluation.registry import EvaluationRegistry
from jarvis.evaluation.runner import EvaluationRunner
from jarvis.evaluation.report import ReportExporter
from jarvis.evaluation.evaluators.grounding import GroundingEvaluator
from jarvis.evaluation.evaluators.navigation import NavigationEvaluator
from jarvis.evaluation.evaluators.projection import ProjectionEvaluator
from jarvis.evaluation.evaluators.retrieval import RetrievalEvaluator
from jarvis.evaluation.evaluators.workflow import WorkflowEvaluator

class ReportService:
    """Facade over evaluation ReportExporter for report rendering."""

    def generate_report(self, profile_name: str = "smoke") -> dict:
        """Generate and export an evaluation report.

        Args:
            profile_name: Quality profile to run.

        Returns:
            dict with report JSON string.
        """
        registry = EvaluationRegistry()
        registry.register(RetrievalEvaluator())
        registry.register(GroundingEvaluator())
        registry.register(NavigationEvaluator())
        registry.register(ProjectionEvaluator())
        registry.register(WorkflowEvaluator())
        runner = EvaluationRunner(registry)
        report = runner.run(profile_name=profile_name)
        json_report = ReportExporter.to_json(report)
        return {"format": "json", "content": json_report}