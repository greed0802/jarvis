"""Renderer Protocol (IP-0007, Part C).

All renderers implement exactly the same contract:
render(RenderContext) → RenderedDocument.

Authority:
  - EQ-0021 (Permanently Frozen)
  - IP-0007 — CheckMate Rendering Layer
"""

from __future__ import annotations

from typing import Protocol

from jarvis.applications.checkmate.rendering.context import RenderContext, RenderedDocument

class Renderer(Protocol):
    """Protocol for all CheckMate renderers.

    Every renderer accepts a RenderContext and returns a RenderedDocument.
    No side effects. No filesystem. No persistence.
    """

    def render(self, context: RenderContext) -> RenderedDocument: ...