"""BOQ Intelligence — Increment 1.

Pure functions that analyze extracted BOQ rows to produce structured
intelligence: classification summary, statistics, section analysis,
and known anomaly reporting.

Operates entirely over list[BOQRow]. No parser modifications, no runtime
integration, no kernel changes.

Authority:
- Capability Evaluation 001 (Approved for Implementation)
- EQ-0007 Production Extraction Report
- EQ-0009 Context Discovery Report
"""

from __future__ import annotations

from dataclasses import dataclass

from jarvis.parsers.costx.boq_extraction import BOQRow

_VALID_ROW_TYPES = frozenset({"Head", "Note", "Section", "Item", "Other"})


@dataclass(frozen=True)
class BOQIntelligenceResult:
    """Immutable analysis result from BOQ Intelligence Increment 1.

    Frozen dataclass provides shallow immutability. Deep immutability
    may be revisited if a future consumer requires it.
    """

    row_classification: dict[str, int]
    section_statistics: dict[str, dict[str, int]]
    boq_statistics: dict[str, int | float]
    known_anomalies: list[dict[str, int | str | float]]


def analyze_boq(rows: list[BOQRow]) -> BOQIntelligenceResult:
    """Analyze extracted BOQ rows and produce intelligence result.

    Args:
        rows: Extracted BOQ rows from extract_boq().

    Returns:
        Immutable BOQIntelligenceResult with classification, statistics,
        section analysis, and known anomalies.
    """
    return BOQIntelligenceResult(
        row_classification=_count_row_types(rows),
        section_statistics=_compute_section_stats(rows),
        boq_statistics=_compute_boq_stats(rows),
        known_anomalies=_detect_anomalies(rows),
    )


def _count_row_types(rows: list[BOQRow]) -> dict[str, int]:
    counts: dict[str, int] = {"Head": 0, "Note": 0, "Section": 0, "Item": 0, "Other": 0}
    for row in rows:
        if row.row_type not in _VALID_ROW_TYPES:
            raise ValueError(f"Unknown row type: {row.row_type!r}")
        counts[row.row_type] += 1
    return counts


def _compute_boq_stats(rows: list[BOQRow]) -> dict[str, int | float]:
    total = len(rows)
    code_rows = sum(1 for r in rows if r.code is not None)
    description_rows = sum(1 for r in rows if r.description is not None)
    quantity_rows = sum(1 for r in rows if r.quantity is not None)
    uom_rows = sum(1 for r in rows if r.uom is not None)
    section_rows = sum(1 for r in rows if r.section is not None)

    return {
        "total_rows": total,
        "code_rows": code_rows,
        "description_rows": description_rows,
        "quantity_rows": quantity_rows,
        "uom_rows": uom_rows,
        "section_rows": section_rows,
    }


def _compute_section_stats(rows: list[BOQRow]) -> dict[str, dict[str, int]]:
    sections: dict[str, dict[str, int]] = {}

    for row in rows:
        if row.section is None:
            continue
        if row.section not in sections:
            sections[row.section] = {"negative_qty": 0, "positive_qty": 0}
        if row.quantity is not None:
            if row.quantity < 0:
                sections[row.section]["negative_qty"] += 1
            elif row.quantity > 0:
                sections[row.section]["positive_qty"] += 1

    return dict(sorted(sections.items()))


def _detect_anomalies(rows: list[BOQRow]) -> list[dict[str, int | str | float]]:
    anomalies: list[dict[str, int | str | float]] = []
    for row in rows:
        if (
            row.section == "OMISSION"
            and row.quantity is not None
            and row.quantity > 0
        ):
            anomalies.append({
                "row_number": row.row_number,
                "code": row.code,
                "quantity": row.quantity,
                "section": row.section,
            })
    return sorted(anomalies, key=lambda a: a["row_number"])