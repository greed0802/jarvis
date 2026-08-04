"""Subcommand dispatcher and exception-to-exit-code mapping."""

from __future__ import annotations

from jarvis.cli.exitcodes import ExitCode
from jarvis.cli.commands.eval import EvalCommand
from jarvis.cli.commands.workbench import WorkbenchCommand
from jarvis.cli.commands.datasets import DatasetsCommand
from jarvis.cli.commands.report import ReportCommand
from jarvis.cli.commands.doctor import DoctorCommand

from jarvis.cli.services.evaluation_service import EvaluationService
from jarvis.cli.services.workbench_service import WorkbenchService
from jarvis.cli.services.dataset_service import DatasetService
from jarvis.cli.services.report_service import ReportService

class CommandDispatcher:
    """Routes subcommand strings to their handlers."""

    def __init__(self) -> None:
        self._eval_service = EvaluationService()
        self._workbench_service = WorkbenchService()
        self._dataset_service = DatasetService()
        self._report_service = ReportService()

    def dispatch_eval(self, profile_name: str = "smoke") -> tuple[ExitCode, dict]:
        cmd = EvalCommand(self._eval_service)
        code, result = cmd.execute(profile_name)
        return (code, result)

    def dispatch_workbench(self, project_data: dict | None = None) -> tuple[ExitCode, dict]:
        cmd = WorkbenchCommand(self._workbench_service)
        code, result = cmd.execute(project_data)
        return (code, result)

    def dispatch_datasets(self) -> tuple[ExitCode, dict]:
        cmd = DatasetsCommand(self._dataset_service)
        code, result = cmd.execute()
        return (code, result)

    def dispatch_report(self, profile_name: str = "smoke") -> tuple[ExitCode, dict]:
        cmd = ReportCommand(self._report_service)
        code, result = cmd.execute(profile_name)
        return (code, result)

    def dispatch_doctor(self) -> tuple[ExitCode, dict]:
        cmd = DoctorCommand()
        code, result = cmd.execute()
        return (code, result)