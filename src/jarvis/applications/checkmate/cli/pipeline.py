"""Pipeline orchestration for CheckMate CLI (CP-0001).

Invokes the frozen CheckMate application pipeline.
No interpretation. No rendering. No export.
Consumes the architecture. Does not modify it.

Authority:
  - Architecture Freeze v1.0
  - Capability Roadmap v2.0
  - CP-0001 — CheckMate CLI Application
"""

from __future__ import annotations

from typing import Any

from jarvis.applications.checkmate.rendering.context import (
    RenderContext,
    RenderOptions,
    RenderMetadata,
    RenderedDocument,
)
from jarvis.applications.checkmate.rendering.protocol import Renderer
from jarvis.applications.checkmate.rendering.markdown import MarkdownRenderer
from jarvis.applications.checkmate.rendering.html import HTMLRenderer
from jarvis.applications.checkmate.rendering.json_renderer import JSONRenderer
from jarvis.applications.checkmate.rendering.terminal import TerminalRenderer

from jarvis.applications.checkmate.export.protocol import Exporter
from jarvis.applications.checkmate.export.request import ExportRequest, ExportOptions, ExportResult
from jarvis.applications.checkmate.export.markdown import MarkdownExporter
from jarvis.applications.checkmate.export.html import HTMLExporter
from jarvis.applications.checkmate.export.json_exporter import JSONExporter
from jarvis.applications.checkmate.export.text import TextExporter

from jarvis.applications.checkmate.review.session import ReviewSession

from jarvis.applications.checkmate.presentation.models import PresentationModel

# ============================================================================
# Renderer Registry
# ============================================================================
_RENDERERS: dict[str, Renderer] = {
    "markdown": MarkdownRenderer(),
    "html": HTMLRenderer(),
    "json": JSONRenderer(),
    "terminal": TerminalRenderer(),
}

# ============================================================================
# Exporter Registry
# ============================================================================
_EXPORTERS: dict[str, Exporter] = {
    "md": MarkdownExporter(),
    "html": HTMLExporter(),
    "json": JSONExporter(),
    "txt": TextExporter(),
}

# ============================================================================
# Renderer Selection
# ============================================================================

def get_renderer(name: str) -> Renderer:
    """Resolve a renderer by name.

    Args:
        name: Renderer name ('markdown', 'html', 'json', 'terminal').

    Returns:
        The registered Renderer instance.

    Raises:
        ValueError: If the renderer name is unknown.
    """
    renderer = _RENDERERS.get(name)
    if renderer is None:
        raise ValueError(
            f"Unknown renderer: '{name}'. Valid: {', '.join(sorted(_RENDERERS.keys()))}"
        )
    return renderer

def get_exporter(name: str) -> Exporter:
    """Resolve an exporter by format name.

    Args:
        name: Exporter format ('md', 'html', 'json', 'txt').

    Returns:
        The registered Exporter instance.

    Raises:
        ValueError: If the exporter name is unknown.
    """
    exporter = _EXPORTERS.get(name)
    if exporter is None:
        raise ValueError(
            f"Unknown exporter: '{name}'. Valid: {', '.join(sorted(_EXPORTERS.keys()))}"
        )
    return exporter

# ============================================================================
# Pipeline Interface
# ============================================================================

class PipelineRunner:
    """Executes the frozen CheckMate pipeline.

    Provides a clean interface for:
    - Rendering a PresentationModel through a specified renderer
    - Exporting a RenderedDocument through a specified exporter

    This is NOT a new architectural layer.
    It is a capability consumer that wires together existing components.
    """

    def render(
        self,
        presentation: PresentationModel,
        renderer_name: str = "terminal",
        review: ReviewSession | None = None,
        include_review: bool = True,
        include_navigation: bool = True,
        include_metadata: bool = True,
    ) -> RenderedDocument:
        """Render a PresentationModel into a RenderedDocument.

        Args:
            presentation: The immutable PresentationModel to render.
            renderer_name: Name of the renderer to use.
            review: Optional ReviewSession to include.
            include_review: Whether to include review state.
            include_navigation: Whether to include navigation indexes.
            include_metadata: Whether to include metadata.

        Returns:
            RenderedDocument from the selected renderer.

        Raises:
            ValueError: If the renderer name is unknown.
        """
        renderer = get_renderer(renderer_name)
        context = RenderContext(
            presentation=presentation,
            review=review,
            options=RenderOptions(
                include_review=include_review,
                include_navigation=include_navigation,
                include_metadata=include_metadata,
            ),
            metadata=RenderMetadata(
                renderer_name=renderer_name,
                renderer_version="1.0.0",
            ),
        )
        return renderer.render(context)

    def export(
        self,
        document: RenderedDocument,
        exporter_name: str = "txt",
        filename_base: str = "report",
    ) -> ExportResult:
        """Export a RenderedDocument into an ExportResult.

        Args:
            document: The RenderedDocument to export.
            exporter_name: Name of the exporter format.
            filename_base: Base filename (without extension).

        Returns:
            ExportResult with bytes and checksum.

        Raises:
            ValueError: If the exporter name is unknown.
        """
        exporter = get_exporter(exporter_name)
        request = ExportRequest(
            document=document,
            options=ExportOptions(
                target_format=exporter_name,
                filename_base=filename_base,
            ),
        )
        return exporter.export(request)

    def render_and_export(
        self,
        presentation: PresentationModel,
        renderer_name: str = "terminal",
        exporter_name: str = "txt",
        review: ReviewSession | None = None,
        filename_base: str = "report",
        include_review: bool = True,
    ) -> ExportResult:
        """Render and export in a single call.

        Args:
            presentation: The PresentationModel to render.
            renderer_name: Renderer to use.
            exporter_name: Exporter format to use.
            review: Optional ReviewSession.
            filename_base: Base filename for export.
            include_review: Whether to include review state.

        Returns:
            ExportResult from the exporter.
        """
        doc = self.render(
            presentation=presentation,
            renderer_name=renderer_name,
            review=review,
            include_review=include_review,
        )
        return self.export(
            document=doc,
            exporter_name=exporter_name,
            filename_base=filename_base,
        )