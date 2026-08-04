"""Shell history — persisted via WorkspaceMemoryService."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)

HISTORY_CATEGORY = "shell_history"


class ShellHistory:
    """Records command history into WorkspaceMemoryService.

    If no memory service is available, history is still tracked
    in-memory for the current session.
    """

    def __init__(self, memory_service: Optional[Any] = None) -> None:
        self._memory_service = memory_service
        self._session_history: list[str] = []

    def record(self, command: str, workspace_id: str = "default") -> None:
        """Record a command invocation."""
        self._session_history.append(command)
        if self._memory_service is not None:
            try:
                self._memory_service.store_entry(
                    workspace_id=workspace_id,
                    category=HISTORY_CATEGORY,
                    content={
                        "command": command,
                        "timestamp": datetime.now().isoformat(),
                    },
                )
            except Exception:
                logger.debug("Failed to persist history entry.", exc_info=True)

    @property
    def entries(self) -> list[str]:
        """Return session history (most recent last)."""
        return list(self._session_history)

    @property
    def count(self) -> int:
        return len(self._session_history)
