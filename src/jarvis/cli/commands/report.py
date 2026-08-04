"""Handler for `jarvis report` — evaluation report export."""

from __future__ import annotations

from jarvis.cli.exitcodes import ExitCode
from jarvis.cli.services.report_service import ReportService

class ReportCommand:
    """Thin command: delegates to ReportService ONLY."""

    def __init__(self, service: ReportService) -> None:
        self._service = service

    def execute(self, profile_name: str = "smoke", output_format: str = "json") -> tuple[int, dict]:
        """Generate and export an evaluation report.

        Args:
            profile_name: Quality profile name.
            output_format: json or markdown.

        Returns:
            Tuple of (exit_code, result_dict).
        """
        try:
            result = self._service.generate_report(profile_name)
            return ExitCode.EXIT_SUCCESS, result
        except Exception:
            return ExitCode.EXIT_INTERNAL_ERROR, {"error": "Report generation failed"}