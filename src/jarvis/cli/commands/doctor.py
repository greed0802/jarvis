"""Handler for `jarvis doctor` — platform diagnostic report."""

from __future__ import annotations

import sys

from jarvis.cli.exitcodes import ExitCode

class DoctorCommand:
    """Thin command: produces structured diagnostic report.

    Sections: Platform, Presentation, Evaluation, Datasets, Python, Configuration, Status.
    """

    def execute(self) -> tuple[int, dict]:
        """Generate diagnostic report.

        Returns:
            Tuple of (exit_code, report_dict).
        """
        try:
            from jarvis.version import __version__ as platform_version
        except ImportError:
            platform_version = "Unknown"

        try:
            from jarvis.evaluation.registry import EvaluationRegistry
            from jarvis.evaluation.evaluators.retrieval import RetrievalEvaluator
            from jarvis.evaluation.evaluators.grounding import GroundingEvaluator
            from jarvis.evaluation.evaluators.navigation import NavigationEvaluator
            from jarvis.evaluation.evaluators.projection import ProjectionEvaluator
            from jarvis.evaluation.evaluators.workflow import WorkflowEvaluator
            registry = EvaluationRegistry()
            registry.register(RetrievalEvaluator())
            registry.register(GroundingEvaluator())
            registry.register(NavigationEvaluator())
            registry.register(ProjectionEvaluator())
            registry.register(WorkflowEvaluator())
            evaluator_ids = registry.evaluator_ids
            eval_version = "1.0.0"
        except Exception:
            evaluator_ids = ["evaluation module unavailable"]
            eval_version = "Unavailable"

        try:
            from jarvis.evaluation.datasets import GoldenDatasetLoader
            loader = GoldenDatasetLoader()
            dataset_names = loader.list_datasets()
            dataset_status = ", ".join(dataset_names) if dataset_names else "No datasets found"
        except Exception:
            dataset_status = "Dataset loader error"

        try:
            from jarvis.presentation.workbench import WorkbenchOrchestrator
            _ = WorkbenchOrchestrator()
            presentation_status = "WORKBENCH_READY"
        except Exception:
            presentation_status = "PRESENTATION_UNAVAILABLE"

        platform_ok = True
        eval_ok = len(evaluator_ids) == 5
        presentation_ok = presentation_status == "WORKBENCH_READY"
        dataset_ok = "No datasets found" not in dataset_status

        if platform_ok and eval_ok and presentation_ok and dataset_ok:
            status = "HEALTHY"
            exit_code = ExitCode.EXIT_SUCCESS
        elif platform_ok:
            status = "DEGRADED"
            exit_code = ExitCode.EXIT_INTERNAL_ERROR
        else:
            status = "ERROR"
            exit_code = ExitCode.EXIT_INTERNAL_ERROR

        report = {
            "Platform": {
                "version": platform_version,
                "boot_status": "ACTIVE" if platform_ok else "UNAVAILABLE",
            },
            "Presentation": {
                "version": "M10.6",
                "protocol_status": presentation_status,
            },
            "Evaluation": {
                "version": eval_version,
                "evaluators": evaluator_ids,
                "profiles": ["smoke", "regression", "release", "research"],
            },
            "Datasets": {
                "status": dataset_status,
                "baseline_verified": dataset_ok,
            },
            "Python": {
                "version": sys.version.split()[0],
                "executable": sys.executable,
                "platform": sys.platform,
            },
            "Configuration": {
                "python_prefix": sys.prefix,
            },
            "Status": status,
        }
        return (exit_code, report)