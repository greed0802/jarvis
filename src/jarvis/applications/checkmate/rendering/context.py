"""Render Context and Rendered Document (IP-0007, Parts A & B).

Immutable containers for rendering input and output. No business logic,
no interpretation, no persistence, no filesystem.

Authority:
  - EQ-0021 (Permanently Frozen)
  - Application Architecture Principles v1.0
  - IP-0007 — CheckMate Rendering Layer
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from jarvis.applications.checkmate.presentation.models import PresentationModel
from jarvis.applications.checkmate.review.session import ReviewSession

@dataclass(frozen=True)
class RenderOptions:
    """Immutable rendering options.

    Attributes:
        include_review: Whether to include ReviewSession state.
        include_navigation: Whether to include navigation indexes.
        include_metadata: Whether to include metadata section.
    """

    include_review: bool = True
    include_navigation: bool = True
    include_metadata: bool = True

@dataclass(frozen=True)
class RenderMetadata:
    """Immutable metadata about the render operation.

    Attributes:
        renderer_name: Name of the renderer that produced the document.
        renderer_version: Version of the renderer.
    """

    renderer_name: str = ""
    renderer_version: str = "1.0.0"

@dataclass(frozen=True)
class RenderContext:
    """Immutable input for all renderers.

    Contains only the PresentationModel and optional ReviewSession.
    No business logic. No interpretation.

    Attributes:
        presentation: The immutable PresentationModel.
        review: Optional ReviewSession (None if no review).
        options: Rendering options.
        metadata: Render operation metadata.
        timestamp: UTC timestamp of render request.
    """

    presentation: PresentationModel
    review: ReviewSession | None = None
    options: RenderOptions = field(default_factory=RenderOptions)
    metadata: RenderMetadata = field(default_factory=RenderMetadata)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

@dataclass(frozen=True)
class RenderedDocument:
    """Immutable rendering output.

    Contains the rendered content with metadata. No persistence,
    no file path, no filesystem operations.

    Attributes:
        mime_type: MIME type of the rendered content.
        content: The rendered content string.
        title: Document title.
        metadata: Key-value metadata about the document.
        warnings: Any rendering warnings (not errors).
    """

    mime_type: str
    content: str
    title: str = ""
    metadata: tuple[tuple[str, str], ...] = ()
    warnings: tuple[str, ...] = ()