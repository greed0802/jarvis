# Object: WorksheetObservation

Category: Core Ontology / Epistemology / Spreadsheet

---

## Purpose

WorksheetObservation is a concrete specialization of the Observation concept. It represents the observable properties of a spreadsheet worksheet at the worksheet level, without requiring row observations, cell observations, or any interpretation of worksheet contents.

WorksheetObservation applies the specialization pattern established by `workbook.md`.

---

## Definition

WorksheetObservation is an Observation that records the directly observable properties of a spreadsheet worksheet source.

**WorksheetObservation = Observation + Worksheet-specific observable properties.**

WorksheetObservation inherits all guarantees, invariants, and provenance requirements defined in `observation.md` and `observation_acquisition.md`. It does not redefine Observation.

---

## Observable Properties

Every property of WorksheetObservation MUST satisfy the following constraint:

> **WorksheetObservation SHALL NOT require RowObservation or CellObservation.**

Worksheet-level properties are observable independently of row-level or cell-level observations. Whether a parser acquires them by inspecting worksheet metadata, reading dimension records, or any other mechanism is an implementation detail outside the ontology.

### Determining Worksheet-Level Properties

Worksheet-level observable properties describe the **organization and structure of the worksheet itself**. They do not constitute observations of individual rows or cells.

This distinction is based on the **level of the source being observed**, not the implementation required to acquire the property.

The ownership test is:

> **Does this property describe the worksheet itself, or does it describe subordinate observed objects?**

Applying this test:

- **Row count** and **column count** describe the worksheet's dimensions — the extent of the grid the worksheet defines. They are facts about the worksheet itself.
- **Hidden rows** and **hidden columns** are structural lists of *positions* that are hidden. They describe the worksheet's visibility configuration, expressed as coordinates — not the contents of those rows or columns. This is the same reasoning that admits `merged_ranges`: a coordinate list is a worksheet-level structural descriptor, not an observation of the cells it references.
- **Cell value** belongs to the cell being observed. Individual cell values do not define the worksheet's structure.

The observable properties of a worksheet include:

### Source Identity (via inherited Provenance)

- Source path or identifier
- Worksheet identifier (name or index within the workbook)

### Worksheet Identity

- Worksheet name
- Worksheet index (position within the workbook, zero-based or one-based as defined by the source format)

### Worksheet Visibility

- Visibility state (visible, hidden, very hidden)

### Worksheet Dimensions

- Row count
- Column count

### Worksheet Structure

- Merged ranges (coordinate ranges that are merged)
- Freeze panes (frozen row and/or column boundaries)
- Auto filter range (if an auto-filter is applied)
- Print area (the designated print region)
- Hidden rows (row indices that are hidden)
- Hidden columns (column indices that are hidden)

---

## Non-Responsibilities

WorksheetObservation does **not** include:

- Cell values (belong to CellObservation)
- Cell formatting (font, fill, alignment, border, number format)
- Row contents (belong to RowObservation)
- BOQ sections or any domain-specific classification
- Validation results
- Business semantics or interpretation

These belong to lower-level specializations (RowObservation, CellObservation) or to downstream ontology families (Evidence, Validation, Knowledge).

---

## Relationship to Observation

WorksheetObservation is an Observation. It inherits:

- **Definition** — an immutable, deterministic record of observable properties
- **Guarantees** — fidelity, determinism, reproducibility, immutability, traceability, independence
- **Provenance** — Source, Observer, Procedure (from `observation_acquisition.md`)
- **Identity** — stable identity for reference throughout lifecycle
- **Lifecycle** — observed → recorded → stored → referenced → archived
- **Invariants** — all eight invariants from `observation.md`, plus acquisition invariants from `observation_acquisition.md`

WorksheetObservation does **not** redefine any of these inherited concepts. It extends Observation only by specifying which observable properties are within scope for a worksheet source.

---

## Relationship to Acquisition

WorksheetObservation is acquired through the Observation Acquisition pipeline defined in `observation_acquisition.md`:

```
Worksheet Source (possesses observable properties)
      │
      │ observable properties are acquired
      ▼
Observer (executes Procedure)
      │
      │ executes
      ▼
Procedure (deterministic method)
      │
      │ acquires
      ▼
WorksheetObservation (immutable result)
```

The Procedure for acquiring a WorksheetObservation defines observable boundaries at the worksheet level. It specifies which worksheet-level properties are within acquisition scope and which are outside (i.e., row-level or cell-level).

---

## Relationship to WorkbookObservation

WorksheetObservation relates to WorkbookObservation. It does **not** require WorkbookObservation.

```
WorkbookObservation
        │
        ├── relates to ──► WorksheetObservation
        ├── relates to ──► WorksheetObservation
        └── relates to ──► WorksheetObservation
```

This relationship model preserves:

- **Independent observations** — WorksheetObservation is complete without observing the workbook or any row
- **Independent lifecycles** — Each observation type has its own lifecycle
- **Independent acquisition** — Worksheet observations may be acquired separately from workbook or row observations
- **Independent testing** — Each observation type can be validated independently
- **Independent reuse** — Observations can be referenced individually

An ObservationSet (defined in a future document) aggregates related observations from a single acquisition run. Aggregation is a container concern, not an observation concern.

**WorksheetObservation SHALL NOT require WorkbookObservation or RowObservation.** A valid WorksheetObservation exists without any corresponding WorkbookObservation, RowObservation, or CellObservation.

---

## Examples

### Acquired WorksheetObservation

| Property | Value |
|----------|-------|
| Source | `/data/export.xlsx` |
| Worksheet name | "CostX" |
| Worksheet index | 0 |
| Visibility | visible |
| Row count | 6354 |
| Column count | 9 |
| Merged ranges | ["A1:I1", "A2:I2"] |
| Freeze panes | None |
| Auto filter | None |
| Print area | None |
| Hidden rows | [] |
| Hidden columns | [] |

### What This Observation Does Not Contain

- Cell values or formulas
- Row data
- Font or fill formatting
- Whether the worksheet represents a BOQ
- Whether the data is valid

Those are not worksheet-level observable properties.

---

## Invariants

In addition to the invariants inherited from `observation.md` and `observation_acquisition.md`:

1. **WorksheetObservation SHALL record only worksheet-level observable properties.**
2. **WorksheetObservation SHALL NOT require WorkbookObservation, RowObservation, or CellObservation.**
3. **WorksheetObservation SHALL NOT contain cell contents or row contents.**
4. **WorksheetObservation SHALL identify the worksheet source through inherited provenance.**
5. **WorksheetObservation SHALL be acquirable independently of workbook, row, or cell observations.**