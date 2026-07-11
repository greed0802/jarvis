# M5 – CostX Export Analysis (Engineering Discovery)

> **Scope**: This document records observable facts gathered from three CostX reference workbooks using `tools/workbook_inspector.py`.
>
> It does **not** recommend parser implementation, architecture changes, business logic, or runtime design.

---

# Overview

This analysis was produced by `tools/workbook_inspector.py` using summary mode (`--formulas`) and verbose mode (`--verbose --formulas`) against each reference workbook.

| File                     | Size          | Sheets | Total Rows             | Total Columns |
| ------------------------ | ------------- | ------ | ---------------------- | ------------- |
| `full_boq.xlsx`          | 241,295 bytes | 1      | 6,354                  | 9             |
| `formula_workbook.xlsx`  | 34,205 bytes  | 1      | 543                    | 4             |
| `dimensions_export.xlsx` | (large)       | 90     | ~3,500–4,200 per sheet | 40            |

---

# Workbook 1 — `full_boq.xlsx`

## Workbook Metadata

| Property         | Observation                   |
| ---------------- | ----------------------------- |
| File Size        | 241,295 bytes                 |
| Sheet Count      | 1                             |
| Sheet Name       | `CostX`                       |
| Calculation Mode | `fullCalcOnLoad=True`         |
| Excel Base Date  | 1899-12-30 (1900 date system) |
| Creator          | `openpyxl`                    |
| Merged Cells     | `A1:I1`, `A2:I2`              |
| Freeze Panes     | None                          |
| Auto-filter      | None                          |
| Hidden Sheets    | None                          |
| Named Ranges     | None observed                 |

---

## Column Statistics

| Column | Non-empty | Observation                          |
| ------ | --------- | ------------------------------------ |
| A      | 4,260     | Text values                          |
| B      | 6,279     | Text values                          |
| C      | 3,606     | Predominantly numeric values         |
| D      | 6,162     | Text values                          |
| E      | 1         | Text                                 |
| F      | 61        | Formula cells with calculated values |
| G      | 1         | Text                                 |
| H      | 1         | Text                                 |
| I      | 63        | Formula cells with calculated values |

---

## Header Row

Observed at Row 4.

| Column | Header      |
| ------ | ----------- |
| A      | Code        |
| B      | Description |
| C      | Quantity    |
| D      | UOM         |
| E      | Rate        |
| F      | SubTotal    |
| G      | Factor      |
| H      | Total       |
| I      | Total       |

Formatting observations:

* Bold
* Calibri 8 pt
* Horizontal alignment applied
* Numeric formatting on quantity-related columns

---

## Row Structure Observations

Rows 1–2 are merged title rows.

Rows beginning around Row 6 exhibit recurring formatting and value patterns.

Examples observed:

| Row | Observation                                                         |
| --- | ------------------------------------------------------------------- |
| 6   | Column B contains bold text `"MAIN WORKS"` while Column A is empty. |
| 8   | Column A contains value `"A"` with bold formatting.                 |
| 9   | Column A contains `"A/1"` while Column D contains `"Head1"`.        |
| 10  | Column D contains `"Head2"`.                                        |
| 11  | Column D contains `"Note"`.                                         |

Observation:

Column D contains recurring text values throughout the workbook, including:

* `Head1`
* `Head2`
* `Note`
* `Item`

The semantic meaning of these values has not been established by this analysis.

---

## Formula Observations

Columns F and I contain Excel formulas.

When loaded using `data_only=True`, these cells return numeric calculated values.

Observed counts:

* Column F: 57 formulas
* Column I: 62 formulas

---

## Additional Observations

Observed patterns include:

* Column A contains hierarchical identifiers such as `A`, `A/1`, `A/2`.
* Numeric values are predominantly located in Column C.
* Formula cells are concentrated in Columns F and I.
* Column D contains recurring textual markers.

No semantic interpretation is assigned.

---

# Workbook 2 — `formula_workbook.xlsx`

## Workbook Metadata

| Property         | Observation           |
| ---------------- | --------------------- |
| File Size        | 34,205 bytes          |
| Sheet Name       | `Sheet1`              |
| Dimensions       | 543 rows × 4 columns  |
| Creator          | Excel 365             |
| Calculation Mode | `fullCalcOnLoad=True` |
| Merged Cells     | None                  |
| Freeze Panes     | None                  |
| Auto-filter      | None                  |
| Hidden Sheets    | None                  |
| Named Ranges     | None observed         |

---

## Column Statistics

| Column | Observation                      |
| ------ | -------------------------------- |
| A      | Text identifiers                 |
| B      | Text descriptions                |
| C      | Numeric values and XGET formulas |
| D      | Recurring text values            |

---

## Observed Recurring Values

Column D contains recurring values including:

* `Head1`
* `Head2`
* `Note`
* `Item`

The semantic meaning of these values has not been established by this analysis.

---

## Formula Observations

Column C contains 409 CostX `XGET(...)` formulas.

Example pattern:

```text
XGET(...)
```

When the workbook is loaded with `data_only=True`, these cells evaluate to `#NAME?`.

This behavior was consistently observed using openpyxl and indicates that the function is not evaluated outside the originating CostX environment.

---

## Additional Observations

Compared with `full_boq.xlsx`:

* Formula expressions are retained rather than replaced with stored numeric values.
* Workbook structure differs while preserving recurring identifiers and formatting patterns.

---

# Workbook 3 — `dimensions_export.xlsx`

## Workbook Metadata

| Property           | Observation                    |
| ------------------ | ------------------------------ |
| Sheet Count        | 90                             |
| Typical Dimensions | ~3,500–4,200 rows × 40 columns |
| Freeze Panes       | None observed                  |
| Auto-filter        | None observed                  |
| Hidden Sheets      | None observed                  |
| Named Ranges       | None observed                  |

---

## Worksheet Naming Patterns

Observed worksheet names combine descriptive labels with drawing or reference identifiers.

Examples include:

* Ceiling Finishes
* Doors
* Floor Finish
* Wall Types

Several worksheet names also include codes and underscore-delimited identifiers.

No semantic interpretation is assigned.

---

## Column Observations

Across inspected worksheets:

* Approximately 40 populated columns were observed.
* Column AN consistently contained approximately 58 populated text cells.

The purpose of Column AN was not determined during this analysis.

---

# Cross-Workbook Comparison

| Aspect           | `full_boq.xlsx`              | `formula_workbook.xlsx`      | `dimensions_export.xlsx` |
| ---------------- | ---------------------------- | ---------------------------- | ------------------------ |
| Sheets           | 1                            | 1                            | 90                       |
| Rows             | 6,354                        | 543                          | ~3,500–4,200             |
| Columns          | 9                            | 4                            | 40                       |
| Excel formulas   | Yes                          | Yes                          | None observed            |
| XGET formulas    | No                           | Yes                          | No                       |
| Calculation Mode | fullCalcOnLoad               | fullCalcOnLoad               | fullCalcOnLoad           |
| Merged Cells     | Yes                          | None observed                | None observed            |
| Row markers      | Recurring values in Column D | Recurring values in Column D | None observed            |

---

# Library Compatibility Observations

## openpyxl Compatibility

| Observation                          | Result                                             |
| ------------------------------------ | -------------------------------------------------- |
| Named style entries with `name=None` | Requires compatibility patch                       |
| ArrayFormula handling                | Returns ArrayFormula objects                       |
| XGET evaluation                      | Returns `#NAME?` when loaded with `data_only=True` |
| Style preservation                   | Formatting preserved                               |

---

## Workbook Loading Behavior

Observed behavior:

* `data_only=False` returns formula expressions.
* `data_only=True` returns calculated values where available.
* CostX `XGET(...)` formulas remain unresolved outside CostX.

---

# Recurring Workbook Patterns

Observed recurring characteristics include:

* Hierarchical identifiers such as `A`, `A/1`, `A/2`
* Recurring values `Head1`, `Head2`, `Note`, and `Item`
* Quantity-related numeric columns
* Consistent worksheet naming patterns
* CostX `XGET(...)` formulas in formula workbooks
* Excel 1900 date system

These observations describe recurring workbook characteristics only.

---

# Parser Considerations (Evidence-Based)

The following characteristics were consistently observed and may require consideration during future parser design:

| Observation                         |
| ----------------------------------- |
| Hierarchical identifier patterns    |
| Recurring values in Column D        |
| CostX-specific `XGET(...)` formulas |
| Large multi-sheet workbooks         |
| Merged title rows                   |
| Theme-based formatting              |
| Wrapped description cells           |

This section documents observable workbook characteristics and does not prescribe implementation.

---

# Deterministic QA Opportunities

Observable characteristics suitable for deterministic validation include:

* Workbook readability
* Sheet count
* Worksheet existence
* Column count
* Merge ranges
* Presence of recurring values
* Formula presence
* Hidden sheet detection
* Workbook calculation properties
* Numeric column validation

No validation algorithms are proposed in this document.

---

# Generated Engineering Artifacts

* `tools/workbook_inspector.py`
* `docs/reference/M5_CostX_Export_Analysis.md`

---

# Summary

Engineering discovery identified three structurally distinct CostX workbook types:

* A workbook containing stored calculated values.
* A workbook containing CostX-specific `XGET(...)` formulas.
* A large multi-sheet workbook containing measurement-related data.

Recurring workbook characteristics, workbook metadata, formatting, formulas, worksheet structures, and compatibility observations were documented using direct inspection.

No parser design, business interpretation, architectural decisions, or runtime implementation are included in this document.

This document serves as the evidence base for subsequent parser design work.
