"""Exporter Protocol (IP-0008, Part C).

All exporters implement the same contract:
export(ExportRequest) → ExportResult

Exporters never perform rendering, review, interpretation, or validation.

Authority:
  - EQ-0021 (Permanently Frozen)
  - IP-0008 — CheckMate Export & Delivery Layer
"""

from __future__ import annotations

from typing import Protocol

from jarvis.applications.checkmate.export.request import ExportRequest, ExportResult

class Exporter(Protocol):
    """Protocol for all CheckMate exporters.

    Every exporter accepts an ExportRequest and returns an ExportResult.
    No side effects. No rendering. No interpretation.
    """

    def export(self, request: ExportRequest) -> ExportResult: ...