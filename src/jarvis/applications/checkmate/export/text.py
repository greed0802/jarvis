"""Text Exporter (IP-0008, Part G).

Consumes only RenderedDocument (text/plain). Produces plain text ExportResult.
No rendering. No interpretation.

Authority:
  - EQ-0021 (Permanently Frozen)
  - IP-0008 — CheckMate Export & Delivery Layer
"""

from __future__ import annotations

from jarvis.applications.checkmate.export.request import (
    ExportRequest,
    ExportResult,
    _compute_checksum,
)

class TextExporter:
    """Exports plain text RenderedDocument to bytes."""

    def export(self, request: ExportRequest) -> ExportResult:
        doc = request.document
        content_bytes = doc.content.encode("utf-8")
        return ExportResult(
            format="txt",
            media_type="text/plain",
            filename=request.recommended_filename or "report.txt",
            content_bytes=content_bytes,
            size_bytes=len(content_bytes),
            checksum=_compute_checksum(content_bytes),
        )