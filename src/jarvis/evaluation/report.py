"""Report exporter for M11.0 — serializes EvaluationReports to JSON and Markdown."""

from __future__ import annotations

import json as _json
from pathlib import Path

from jarvis.evaluation.contracts import EvaluationReport


class ReportExporter:
    """Exports EvaluationReports to JSON and Markdown formats."""

    @staticmethod
    def to_json(report: EvaluationReport, output_path: Path | None = None) -> str:
        """Serialize an EvaluationReport to a JSON string.

        Args:
            report:      The EvaluationReport to serialize.
            output_path: Optional file path to write JSON to.

        Returns:
            JSON string representation of the report.
        """
        data = {
            "run_id": report.run_id,
            "profile_name": report.profile_name,
            "summary_score": report.summary_score,
            "promotion_gate_passed": report.promotion_gate_passed,
            "provenance": _provenance_to_dict(report.provenance),
            "domain_results": _results_to_dict(report.domain_results),
        }
        json_str = _json.dumps(data, indent=2, default=str)
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json_str, encoding="utf-8")
        return json_str

    @staticmethod
    def to_summary(report: EvaluationReport) -> str:
        """Return a human-readable one-line summary string."""
        status = "PASSED" if report.promotion_gate_passed else "FAILED"
        return (
            f"[{report.profile_name.upper()}] "
            f"Score: {report.summary_score:.2f} | "
            f"Gates: {status} | "
            f"Cases: {sum(len(v) for v in report.domain_results.values())}"
        )


def _dataclass_to_dict(obj: object) -> dict:
    """Internal: convert a frozen dataclass to dict for serialization."""
    if hasattr(obj, "__dict__"):
        return {k: _dataclass_to_dict(v) for k, v in vars(obj).items()}
    if isinstance(obj, (tuple, list)):
        return [_dataclass_to_dict(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    return str(obj)

def _provenance_to_dict(provenance) -> dict:
    return _dataclass_to_dict(provenance)

def _results_to_dict(domain_results: dict[str, tuple]) -> dict:
    return {
        eid: [_dataclass_to_dict(r) for r in results]
        for eid, results in domain_results.items()
    }