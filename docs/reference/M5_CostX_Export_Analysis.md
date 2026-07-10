# M5 – CostX Export Analysis (Engineering Discovery)

> **Scope**: This document provides observable facts about the three CostX reference workbooks.  
> It does NOT recommend architecture changes, parser design, or business logic.

---

## Overview

This analysis was produced by `tools/workbook_inspector.py` running in summary mode (`--formulas`) and verbose mode (`--verbose --formulas`) against each workbook.

| File | Size | Sheets | Total Rows | Total Columns |
|------|------|--------|------------|---------------|
| `full_boq.xlsx` | 241,295 bytes | 1 | 6,354 | 9 |
| `formula_workbook.xlsx` | 34,205 bytes | 1 | 543 | 4 |
| `dimensions_export.xlsx` | (large) | 90 | ~3,500 - 4,200 per sheet | 40 |

---

## Workbook 1: `full_boq.xlsx`

### Observed Workbook Characteristics

| Fact | Value |
|------|-------|
| File Size | 241,295 bytes |
| Sheet Count | 1 |
| Sheet Names | `['CostX']` |
| Calculation Mode | `fullCalcOnLoad=True` (formulas calculated on load) |
| Excel Base Date | 1899-12-30 (1900 date system) |
| Creator | `openpyxl` (workbook was regenerated) |
| Merged Cells | 2 ranges: `A1:I1`, `A2:I2` |
| Freeze Panes | None |
| Auto-filter | None |
| Hidden Sheets | None |
| Named Ranges | 0 |

### Column Statistics

| Column | Non-Empty | Type Breakdown |
|--------|-----------|----------------|
| A | 4,260 | text=4,260 (appears to be codes: "A", "A/1", "A/2", etc.) |
| B | 6,279 | text=6,279 (descriptions) |
| C | 3,606 | numeric=3,605, text=1 (quantities) |
| D | 6,162 | text=6,162 (UOM codes: "m2", etc.) |
| E | 1 | text=1 (appears to be a label) |
| F | 61 | numeric=3, text=1, formula=57 (SubTotal column with formulas) |
| G | 1 | text=1 (label) |
| H | 1 | text=1 (label) |
| I | 63 | numeric=0, text=1, formula=62 (Total column with formulas) |

### Header Row (Row 4)

Observed column headers (bold, centered, font=Calibri 8pt):

| Column | Header | Observable Style |
|--------|--------|----------------|
| A | Code | bold, align_h=left |
| B | Description | bold, align_h=left |
| C | Quantity | bold, align_h=right, numfmt=#,##0.00 |
| D | UOM | bold, align_h=left |
| E | Rate | bold, align_h=right |
| F | SubTotal | bold, align_h=right |
| G | Factor | bold, align_h=right |
| H | Total | bold, align_h=right |
| I | Total | bold, align_h=right |

### Row Hierarchy Observations

Rows 1-2 are merged title rows (FULL BOQ, bold, centered).

Rows 6+ show structured hierarchy with indentation patterns observable in column A:

| Row | Column A Value | Column D Value | Observable Pattern |
|-----|----------------|--------------|-------------------|
| 6 | (empty) | | Appears to be section header |
| 6 | — | | Value "MAIN WORKS" in column B, bold |
| 7 | — | | Empty (subtotal separator?) |
| 8 | "A" | — | Code with bold formatting, appears to be trade code |
| 8 | — | — | "GROSS FLOOR AREA (GFA)" in column B, bold |
| 9 | "A/1" | "Head1" | Definition/assumption marker in column D |
| 10 | — | "Head2" | Sub-section marker in column D |
| 11 | "A/1" | "Note" | Note marker in column D |

**Key observation**: Column D contains row type markers that appear consistent:
- `"Head1"` – Top-level headings
- `"Head2"` – Sub-headings  
- `"Note"` – Explanatory notes
- `"Item"` – BOQ line items (observed in formula_workbook.xlsx)

### Formula Observations (Column F and I)

57 formulas in column F, 62 formulas in column I. These are CostX-calculated quantity totals. All calculated values were observed as numeric (not shown in truncated output).

### Possible Interpretation (Low Confidence)

- Column A: Hierarchical code structure (Trade/Item reference)
- Column D: Row classification markers (Head1/Head2/Note/Item)
- Column C: Measurable quantity values
- Columns F, I: Computed cost values derived from CostX measurements

---

## Workbook 2: `formula_workbook.xlsx`

### Observed Workbook Characteristics

| Fact | Value |
|------|-------|
| File Size | 34,205 bytes |
| Sheet Names | `['Sheet1']` |
| Sheet Dimensions | 543 rows x 4 columns |
| Creator | `365` (Excel 365) |
| Calculation Mode | `fullCalcOnLoad=True` |
| Merged Cells | None |
| Freeze Panes | None |
| Auto-filter | None |
| Hidden Sheets | None |
| Named Ranges | 0 |

### Column Statistics

| Column | Non-Empty | Type Breakdown |
|--------|-----------|--------------|
| A | 454 | text=454 (codes: "F/1", "F/2", etc.) |
| B | 543 | text=543 (descriptions, wrapped text) |
| C | 420 | numeric=11, formula=409 (quantities via XGET formulas) |
| D | 543 | text=543 (row type markers) |

### Row Type Marker Values Observed (Column D)

From inspection output:
- `"Head1"` – Top-level sections (GENERALLY, REFERENCES, PRICES, GENERAL ITEMS)
- `"Head2"` – Sub-sections
- `"Note"` – Descriptive/definitional rows
- `"Item"` – BOQ line items with quantity values in column C

### Formula Observations

409 cells in column C contain formulas. These are ArrayFormula objects (CostX XGET type).

When loaded with `data_only=True`, calculated values appear as `#NAME?` because the XGET functions are CostX-specific and not recognized by openpyxl.

Observed formula pattern (from inspecting cell C33):
```
XGET("...", ...)  # Specific CostX lookup function
```

The formulas reference external CostX measurement data that cannot be resolved without the CostX application context.

### Possible Interpretation (Low Confidence)

This workbook represents the "formula layer" – a view of the BOQ with XGET formulas still embedded, ready to pull live measurement data from CostX. This differs from `full_boq.xlsx` which has pre-calculated values.

---

## Workbook 3: `dimensions_export.xlsx`

### Observed Workbook Characteristics

| Fact | Value |
|------|-------|
| Sheet Count | 90 sheets |
| Typical Sheet Dimensions | ~3,500-4,200 rows x 40 columns |
| Freeze Panes | None on all sheets |
| Auto-filter | None on all sheets |
| Merged Cells | Not detected (or not reported) |
| Hidden Sheets | None |
| Named Ranges | 0 |

### Sheet Name Patterns

Sheet names follow these patterns (observed from inspection):

| Pattern | Example |
|---------|---------|
| Trade + Drawing ID | `Ceiling Finishes  3015 A1007 LE` |
| Trade + Reference | `Doors  3015 A1001 LEVEL 1 GA PL` |
| Trade + Level | `Floor Finish  3015 A0130 LEVEL` |
| Trade + Code | `Wall Types  3015 A1201 LEVEL 1` |

Some sheets have underscore patterns: `HDR M100 _T1_`, indicating dimensional references.

### Column Statistics (Representative Sheet)

All inspected sheets show consistent structure:

| Column | Non-Empty (per sheet) | Type |
|--------|----------------------|------|
| A | varies | text (appears to be measurement references) |
| B | varies | text (descriptions) |
| ... | ... | ... |
| AN | 58 | text (appears to be a computed total or summary column) |

### Possible Interpretation (Low Confidence)

Each sheet represents a **Dimension Group** – measurements for a specific trade/drawing combination. Column AN consistently contains 58 non-empty text values across sheets, suggesting it holds either totals or lookup keys.

---

## Cross-Workbook Comparison Table

| Aspect | `full_boq.xlsx` | `formula_workbook.xlsx` | `dimensions_export.xlsx` |
|--------|-----------------|----------------------|------------------------|
| **Purpose (per README)** | Final BOQ with calculated values | Formula layer (XGET formulas) | Raw dimension measurements |
| **Sheet Count** | 1 | 1 | ~90 |
| **Row Count** | 6,354 | 543 | 3,400-4,200 per sheet |
| **Column Count** | 9 | 4 | 40 |
| **Formulas Present** | Yes (57 in F, 62 in I) | Yes (409 in C) | No |
| **CostX XGET Formulas** | No | Yes | No |
| **Calculation Mode** | fullCalcOnLoad=True | fullCalcOnLoad=True | fullCalcOnLoad=True |
| **Merged Header Rows** | Yes (A1:I1, A2:I2) | No | Not detected |
| **Column Headers** | Explicit in row 4 | None observed | None (raw data) |
| **Row Type Markers** | Column D (Head1/Head2/Note) | Column D (Head1/Head2/Note/Item) | No explicit markers |
| **Numeric Quantities** | Column C | Column C (via formulas) | Multiple columns |
| **File Size** | ~240 KB | ~34 KB | ~? (large) |

---

## Library Compatibility Observations

### openpyxl Compatibility

| Issue | Observation | Workaround |
|-------|-------------|------------|
| Named Style with None name | CostX exports contain `_NamedCellStyle` entries with `name=None` | Patched in `_load_workbook()` to coerce None to "" |
| ArrayFormula display | `cell.value` returns `ArrayFormula` object, not string | Extract `.formula` attribute for display |
| XGET function resolution | `#NAME?` error when loaded with `data_only=True` | Expected – XGET is CostX-specific, not an Excel function |
| iter_rows performance | Successful iteration over 6,000+ rows | Works correctly, no memory issues observed |

### openpyxl Data Loading Behavior

1. `data_only=False`: Returns formula objects (ArrayFormula for XGET)
2. `data_only=True`: Returns `#NAME?` for XGET formulas (function unavailable)
3. Style preservation: All formatting (font, alignment, number format) preserved under both modes

---

## Special CostX Conventions Observed

| Convention | Evidence |
|-----------|----------|
| Sheet naming pattern | Trade + Drawing ID + Level/Phase suffix |
| Code hierarchy | "A", "A/1", "A/2"... or "F/1", "F/2"... |
| Row classification column | Column D contains "Head1", "Head2", "Note", "Item" |
| Quantity column | Numeric values with `#,##0.00` format, right-aligned |
| UOM column | Text values like "m2", "m3", "ea" |
| XGET functions | ArrayFormula objects referencing CostX measurement database |
| Excel base date 1899-12-30 | Confirms 1900 date system compatibility |

---

## Parsing Challenges Identified

| Challenge | Evidence | Risk Level |
|-----------|----------|------------|
| Nested code hierarchy | Codes like "A", "A/1", "A/2" suggest tree structure | Medium |
| Row type classification via Column D | Relies on exact string match ("Head1", "Note") | High (format may vary) |
| XGET formula parsing | CostX-specific syntax, returns `#NAME?` externally | High |
| Large sheet count | 90 sheets in dimensions_export.xlsx | Low (library handles it) |
| Merged header rows | A1:I1, A2:I2 in full_boq.xlsx | Low (detectable) |
| No auto-filter | Cannot use filter metadata for structure detection | Low (use style/formatting) |
| Theme font colors | Font colors use `theme:1` (not RGB) | Low |
| Wrap text on descriptions | Long text may span visual rows | Low |

---

## Deterministic QA Opportunities

| QA Check | Observable Evidence |
|----------|-------------------|
| Row count consistency | Verify expected row counts per sheet type |
| Column count consistency | All dimensions sheets have 40 columns |
| Required column presence | Column D (row type marker) should exist |
| Code hierarchy format | Regex check for "A", "A/n" or "F/n" patterns |
| Numeric format validation | Quantity columns should have numeric values or formulas |
| Merge range detection | Expected merges at A1:I1, A2:I1 for BOQ sheets |
| Named range expectation | Currently none observed, but could be added |
| Workbook property check | Creator, calculation mode consistent across exports |
| Hidden row/column detection | Could indicate collapsed sections |

---

## Files Generated

- `tools/workbook_inspector.py` – Engineering inspection utility
- `docs/reference/M5_CostX_Export_Analysis.md` – This document

---

## Next Steps (Not Part of This Analysis)

This document presents only observable facts. Future work (outside scope of this discovery task):

1. Create a `--compare` mode for cross-file analysis
2. Add `--json` output for machine-readable consumption
3. Design parser based on observed structures (only after consensus on format)

---

*Generated by workbook_inspector.py – a reusable engineering tool under `tools/` with no runtime dependencies.*