"""JSON Exporter (IP-0008, Part F).

Consumes only RenderedDocument (application/json). Produces JSON ExportResult.
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

class JSONExporter:
    """Exports JSON RenderedDocument to bytes."""

    def export(self, request: ExportRequest) -> ExportResult:
        doc = request.document
        content_bytes = doc.content.encode("utf-8")
        return ExportResult(
            format="json",
            media_type="application/json",
            filename=request.recommended_filename or "report.json",
            content_bytes=content_bytes,
            size_bytes=len(content_bytes),
            checksum=_compute_checksum(content_bytes),
        )