"""Handler for `jarvis workbench` — workbench pipeline execution."""

from __future__ import annotations

from jarvis.cli.exitcodes import ExitCode
from jarvis.cli.services.workbench_service import WorkbenchService

class WorkbenchCommand:
    """Thin command: delegates to WorkbenchService ONLY."""

    def __init__(self, service: WorkbenchService) -> None:
        self._service = service

    def execute(self, project_data: dict | None = None) -> tuple[int, dict]:
        """Execute workbench pipeline headlessly.

        Args:
            project_data: Optional project context.

        Returns:
            Tuple of (exit_code, result_dict).
        """
        try:
            result = self._service.run_pipeline(project_data)
            return ExitCode.EXIT_SUCCESS, result
        except RuntimeError:
            return ExitCode.EXIT_PROJECT_LOAD_FAILED, {"error": "Project load or workbench execution failed"}
        except Exception:
            return ExitCode.EXIT_INTERNAL_ERROR, {"error": "Internal workbench error"}