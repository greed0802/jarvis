"""Handler for `jarvis datasets` — golden dataset listing."""

from __future__ import annotations

from jarvis.cli.exitcodes import ExitCode
from jarvis.cli.services.dataset_service import DatasetService

class DatasetsCommand:
    """Thin command: delegates to DatasetService ONLY."""

    def __init__(self, service: DatasetService) -> None:
        self._service = service

    def execute(self) -> tuple[int, dict]:
        """List and validate datasets.

        Returns:
            Tuple of (exit_code, result_dict).
        """
        try:
            result = self._service.list_datasets()
            if not result["datasets"]:
                return ExitCode.EXIT_DATASET_INVALID, {"error": "No datasets found"}
            return ExitCode.EXIT_SUCCESS, result
        except RuntimeError:
            return ExitCode.EXIT_DATASET_INVALID, {"error": "Dataset validation failed"}
        except Exception:
            return ExitCode.EXIT_INTERNAL_ERROR, {"error": "Internal datasets error"}