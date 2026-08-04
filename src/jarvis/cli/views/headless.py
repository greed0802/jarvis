"""HeadlessConsoleView — implements WorkbenchView protocol for headless CLI."""

from __future__ import annotations

from typing import Any

class HeadlessConsoleView:
    """Implements the WorkbenchView protocol for the headless CLI adapter.

    Captures projected WorkbenchViewModel snapshots for rendering.
    Zero GUI framework dependencies.
    """

    def __init__(self) -> None:
        self._last_rendered: dict[str, Any] = {}

    def render(self, view_model: dict[str, Any] | object) -> dict[str, Any]:
        """Capture a WorkbenchViewModel projection for rendering.

        Args:
            view_model: The projection result from WorkbenchProjector.

        Returns:
            Captured view model snapshot as a dict for renderers.
        """
        if isinstance(view_model, dict):
            snapshot = dict(view_model)
        elif isinstance(view_model, tuple) and hasattr(view_model, "_fields"):
            snapshot = view_model._asdict()
        elif hasattr(view_model, "__dict__"):
            snapshot = vars(view_model).copy()
        else:
            snapshot = {"value": str(view_model)}
        self._last_rendered = snapshot
        return snapshot

    @property
    def last_rendered(self) -> dict[str, Any]:
        """Return the most recently rendered view model snapshot."""
        return self._last_rendered