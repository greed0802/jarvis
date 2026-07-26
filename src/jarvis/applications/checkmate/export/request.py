"""Export Request and Result (IP-0008, Parts A & B).

Immutable containers for export input and output. No rendering,
no interpretation, no filesystem handles.

Authority:
  - EQ-0021 (Permanently Frozen)
  - IP-0008 — CheckMate Export & Delivery Layer
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from jarvis.applications.checkmate.rendering.context import RenderedDocument

@dataclass(frozen=True)
class OutputPolicy:
    """Output policy for the export.

    Attributes:
        directory: Output directory path (no trailing slash).
        create_directory: Whether to create the directory if missing.
        overwrite: Whether to overwrite existing files.
    """

    directory: str = "."
    create_directory: bool = True
    overwrite: bool = True

@dataclass(frozen=True)
class ExportOptions:
    """Export options.

    Attributes:
        target_format: The target format identifier.
        filename_base: Base filename (without extension).
        output: Output policy.
    """

    target_format: str = ""
    filename_base: str = ""
    output: OutputPolicy = field(default_factory=OutputPolicy)

@dataclass(frozen=True)
class ExportMetadata:
    """Export metadata.

    Attributes:
        exporter_name: Name of the exporter.
        exporter_version: Version of the exporter.
        source_format: Original MIME type of the RenderedDocument.
    """

    exporter_name: str = ""
    exporter_version: str = "1.0.0"
    source_format: str = ""

@dataclass(frozen=True)
class ExportRequest:
    """Immutable export request.

    Contains only a RenderedDocument. Never accesses application state,
    never performs rendering or interpretation.

    Attributes:
        document: The rendered document to export.
        options: Export options.
        metadata: Export metadata.
    """

    document: RenderedDocument
    options: ExportOptions = field(default_factory=ExportOptions)
    metadata: ExportMetadata = field(default_factory=ExportMetadata)

    @property
    def recommended_filename(self) -> str:
        """Return a recommended filename based on options and document title."""
        base = self.options.filename_base or self.document.title.replace(" ", "_").lower()
        if self.options.target_format:
            return f"{base}.{self.options.target_format}"
        return base

def _compute_checksum(content: bytes) -> str:
    """Compute a deterministic SHA-256 checksum."""
    return hashlib.sha256(content).hexdigest()

@dataclass(frozen=True)
class ExportResult:
    """Immutable export result.

    Contains the exported content as bytes. No filesystem handles,
    no open streams.

    Attributes:
        format: Target format identifier.
        media_type: MIME type of the exported content.
        filename: Recommended filename (without directory).
        content_bytes: The exported content.
        size_bytes: Size of the content in bytes.
        checksum: SHA-256 checksum of the content.
        warnings: Any export warnings (not errors).
    """

    format: str
    media_type: str
    filename: str
    content_bytes: bytes
    size_bytes: int
    checksum: str
    warnings: tuple[str, ...] = ()