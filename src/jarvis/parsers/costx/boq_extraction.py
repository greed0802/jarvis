"""Deterministic BOQ row extraction from validated CostX workbooks.

Engineering Question: EQ-0007

References:
- Engineering Spike #1 (tools/boq_row_analysis.py)
- EQ-0001 (Row Types)
- EQ-0002 (Sign Convention)
- EQ-0006 (Omission Anomalies)
- ADR-0025 (Observation Runtime rejection)
- M5 CostX Export Analysis (Row 6 first data row)
- Office standard: docs/reference/office_standards/12_Units of Measurements.docx
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from openpyxl.workbook.workbook import Workbook


# Column positions (from M5 analysis)
_COL_CODE = 1
_COL_DESC = 2
_COL_QTY = 3
_COL_UOM = 4

# Row 6 is first BOQ data row (M5: "Rows beginning around Row 6 exhibit recurring patterns")
_FIRST_DATA_ROW = 6

# UOM values for Item rows per office convention
# docs/reference/office_standards/12_Units of Measurements.docx
# Confirmed consistent with Engineering Spike #1 observation of full_boq.xlsx
_ITEM_UOMS = frozenset({"m", "m2", "m3", "no", "t", "Item", "item"})


@dataclass
class BOQRow:
    """Structured BOQ row extracted from a CostX workbook."""
    row_number: int
    code: str | None
    description: str | None
    quantity: float | None
    uom: str | None
    row_type: str
    section: Literal["OMISSION", "ADDITION"] | None = None


def extract_boq(workbook: Workbook) -> list[BOQRow]:
    """Extract structured BOQ rows from a validated CostX workbook.

    Implements the deterministic classification behavior established by
    Engineering Spike #1.

    Classification rules:
    - UOM='noidc' + Desc='OMISSION/ADDITION' -> Section boundaries
    - UOM='Note' -> Note rows
    - UOM matches 'Head\\d+' -> Head rows
    - UOM in Item UOM set -> Item rows
    - Otherwise -> Other rows

    Section context is preserved during extraction (EQ-0002).

    Args:
        workbook: A validated CostX BOQ workbook (validated by WorkbookParser.validate()).
                  Must contain a "CostX" worksheet.

    Returns:
        List of BOQRow objects representing the extracted BOQ rows.
        Each row includes section context derived from preceding section markers.

    Note:
        The workbook should be validated before calling this function.
        Validation ensures exactly one worksheet named "CostX" exists.
    """
    ws = workbook["CostX"]

    rows: list[BOQRow] = []
    current_section: Literal["OMISSION", "ADDITION"] | None = None

    for row_num in range(_FIRST_DATA_ROW, ws.max_row + 1):
        code = ws.cell(row=row_num, column=_COL_CODE).value
        desc = ws.cell(row=row_num, column=_COL_DESC).value
        qty = ws.cell(row=row_num, column=_COL_QTY).value
        uom = ws.cell(row=row_num, column=_COL_UOM).value

        # Capture section context before classification
        if uom == "noidc" and desc in ("OMISSION", "ADDITION"):
            current_section = desc

        row_type = _classify_row(uom)

        rows.append(BOQRow(
            row_number=row_num,
            code=str(code) if code else None,
            description=str(desc) if desc else None,
            quantity=float(qty) if isinstance(qty, (int, float)) else None,
            uom=str(uom) if uom else None,
            row_type=row_type,
            section=current_section,
        ))

    return rows


def _classify_row(uom: str | None) -> str:
    """Classify a BOQ row based on UOM value.

    Classification uses semantic UOM markers only.
    Column A is an opaque identifier (EQ-0001 Engineering Discovery).
    """
    # Section boundary detection
    if uom == "noidc":
        return "Section"

    # UOM-based classification
    if uom == "Note":
        return "Note"

    if uom in _ITEM_UOMS:
        return "Item"

    # Head rows (UOM matches Head<digits>)
    if re.fullmatch(r"Head\d+", str(uom) if uom else ""):
        return "Head"

    return "Other"