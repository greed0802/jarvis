# M5 Phase 2 – First CostX Parser Design Specification

> **Scope**: This document defines the design for the first CostX workbook parser.  
> It is based solely on evidence collected during M5 Phase 1 Engineering Discovery.  
> No implementation code, dataclasses, or runtime components are defined.

---

## 1. Purpose

The first CostX parser is responsible for **deterministic extraction** of workbook data.

It reads a CostX BOQ workbook and produces a structured sequence of row records. Each record contains the raw cell values, formulas, and formatting metadata as observed in the workbook.

---

## 2. Engineering Scope

The first parser is intentionally minimal.

Its responsibility is limited to deterministic extraction of workbook observations.

The parser does not attempt to normalize, classify, enrich, or interpret workbook contents.

The parser is considered an engineering component rather than a business component.

The parser remains independent of:

- Kernel
- Application
- Context
- Planner
- Workflow
- Skills

---

## 3. Supported Inputs

The first parser targets the **CostX BOQ workbook format** represented by:

`tests/fixtures/costx/full_boq.xlsx`

### Observed Characteristics

The reference workbook exhibits these characteristics:

| Characteristic | Evidence |
|----------------|----------|
| Single worksheet | M5: Workbook 1 metadata shows 1 sheet |
| Worksheet named "CostX" | M5: Sheet Names = `['CostX']` |
| Header row at Row 4 | M5: Header Row table identifies row 4 as header |
| Nine populated columns (A–I) | M5: Column Statistics shows cols A-I populated |
| Merged title rows present | M5: Merge ranges A1:I1, A2:I2 |
| No auto-filter, no freeze panes | M5: FREEZE/FILTER observations |
| Formulas in columns F and I | M5: Formula observations |

**Row count is not a format invariant.** The reference workbook has 6,354 data rows, but other BOQ workbooks may have different row counts while preserving the same structure.

### Not Supported

- `tests/fixtures/costx/formula_workbook.xlsx` — Contains unresolvable XGET formulas that return `#NAME?` externally
- `tests/fixtures/costx/dimensions_export.xlsx` — Contains ~90 worksheets with 40 columns each; raw measurement format differs from BOQ

---

## 4. Parser Responsibilities

The parser performs the following observable operations:

1. **Load workbook** — Opens the XLSX file for reading
2. **Validate structure** — Confirms expected worksheet exists (see Validation Sequence)
3. **Locate worksheet** — Identifies the "CostX" worksheet
4. **Read worksheet** — Accesses cell values, formulas, and formatting
5. **Iterate workbook rows in their original order** — Traverses rows as stored in the workbook
6. **Produce row records** — Emits observable data for each row

---

## 5. Parser Boundaries

The parser explicitly does **not**:

| Not Responsible | Reason |
|-----------------|--------|
| Classify BOQ rows | Row classification (Head1/Head2/Note/Item) is business logic, deferred |
| Infer hierarchy | Code hierarchy (A → A/1 → A/2) requires semantic interpretation |
| Calculate quantities | Quantities are observed values, not computed by parser |
| Interpret CostX semantics | XGET formulas, measurement references, UOM meaning are CostX-specific |
| Execute formulas | Formulas are preserved as text; calculated values are observed passively |
| Modify workbook contents | Parser is read-only |
| Interact with runtime | No Kernel, Context, Planner, Workflow, or Skill dependencies |

---

## 6. Observable Input Model

The parser operates on the following conceptual input structure:

- **Workbook** — An XLSX file containing one or more worksheets
- **Worksheet** — Named "CostX", with header row at Row 4
- **Rows** — An ordered sequence of worksheet rows. The reference workbook contains merged title rows followed by a header row and subsequent worksheet rows. The parser preserves workbook row order.
- **Cells** — Cells containing values, formulas, and formatting. The reference workbook contains the observed columns documented in the M5 reference.
- **Merged Cells** — Merged ranges are present and observable (M5: Merge ranges)

---

## 7. Observable Output

The parser exposes the following after reading the workbook:

- **Row order preserved** — Rows are returned in workbook order
- **Cell values** — Raw values from each populated cell
- **Formula expressions** — Formula strings from cells with formulas
- **Calculated values** — Pre-calculated values when formulas resolve (columns F, I in full_boq)
- **Formatting metadata** — Font attributes, alignment, number format per cell
- **Column positions** — Cells identifiable by column position

---

## 8. Parser Invariants

The parser shall maintain these invariants:

- **Read-only access** — Workbook shall not be modified
- **Row order preserved** — Output order matches workbook order
- **Formula text preserved** — Formulas are emitted as strings, not evaluated
- **Formatting preserved** — Style attributes are observable in output
- **Workbook readable** — Workbook shall be readable by the supported loader

---

## 9. Validation Sequence

Before row iteration, the parser shall verify:

1. **Workbook file exists** — Path resolves to an existing file
2. **Workbook readable** — File opens successfully (library compatibility handled by loader)
3. **Worksheet "CostX" exists** — Required worksheet present
4. **Worksheet structure valid** — Worksheet contains the observed workbook structure required by the supported workbook format. The validation mechanism is implementation-defined.

---

## 10. Failure Conditions

The parser shall fail under these conditions:

| Condition | Evidence |
|-----------|----------|
| Workbook file missing | M5: Basic file inspection requirement |
| Workbook unreadable/corrupt | M5: Library compatibility observations |
| Worksheet "CostX" missing | M5: Sheet names observed as `['CostX']` |
| Workbook structure differs from supported format | M5: Format-specific observations (merged title, header row, column structure) |

No recovery strategies are prescribed; failures are fatal.

---

## 11. Traceability

Every design decision traces to M5 Phase 1 evidence:

| Design Decision | Evidence |
|-----------------|----------|
| Support single worksheet BOQ | M5: Workbook 1 metadata (1 sheet) |
| Worksheet named "CostX" required | M5: Sheet Names = `['CostX']` |
| Header row at Row 4 | M5: Header Row table |
| Nine columns in reference | M5: Column Statistics (A-I) |
| Preserve merged title region | M5: Merge ranges A1:I1, A2:I2 |
| Preserve formulas in output | M5: Formula observations (57 in F, 62 in I) |
| Preserve formatting metadata | M5: Formatting observations (font, numfmt, alignment) |
| Ignore XGET formulas | M5: XGET formulas unresolvable externally |
| No hierarchy inference | M5: Engineering discovery scope |
| Row order invariant | M5: No sorting observed in workbook |

---

## 12. Future Milestones

| Milestone | Scope |
|-----------|-------|
| **M6** | First CostX Parser Implementation |
| **M7** | Row Classification |
| **M8** | BOQ Structure Reconstruction |
| **M9** | Semantic Interpretation |

---

## Files Generated

- `docs/design/M5_First_CostX_Parser_Specification.md` — This document

---

*This document follows: Documentation First, Evidence Before Promotion, YAGNI, Deterministic Engineering.*