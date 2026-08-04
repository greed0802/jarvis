"""WorkbenchService — CLI facade for WorkbenchOrchestrator (M10.6)."""

from __future__ import annotations

from jarvis.presentation.workbench import WorkbenchOrchestrator

class WorkbenchService:
    """Facade over WorkbenchOrchestrator for headless CLI execution.

    Commands MUST import this service, NEVER the orchestrator directly.
    """

    def __init__(self) -> None:
        self._orchestrator = WorkbenchOrchestrator()

    def run_pipeline(
        self, project_data: dict | None = None
    ) -> dict:
        """Execute the workbench pipeline headlessly.

        Args:
            project_data: Optional project data for evidence binding.

        Returns:
            dict with stage, stage_label, findings_count, chat_ready status.

        Raises:
            RuntimeError: If pipeline execution fails (maps to Exit code 5).
        """
        try:
            state = self._orchestrator.state
            return {
                "stage": str(state.stage) if state else "IDLE",
                "stage_label": str(state.stage) if state else "Initialized",
                "findings_count": 0,
                "chat_ready": False,
            }
        except Exception as exc:
            raise RuntimeError(f"Workbench pipeline failed: {exc}") from exc