# Object: WorkbookObservation

Category: Core Ontology / Epistemology / Spreadsheet

---

## Purpose

WorkbookObservation is the first concrete specialization of the Observation concept. It represents the observable properties of a spreadsheet workbook at the workbook level, without requiring worksheet observations or any interpretation of workbook contents.

WorkbookObservation establishes the pattern for all subsequent Observation specializations.

---

## Definition

WorkbookObservation is an Observation that records the directly observable properties of a spreadsheet workbook source.

**WorkbookObservation = Observation + Workbook-specific observable properties.**

WorkbookObservation inherits all guarantees, invariants, and provenance requirements defined in `observation.md` and `observation_acquisition.md`. It does not redefine Observation.

---

## Observable Properties

Every property of WorkbookObservation MUST satisfy the following constraint:

> **WorkbookObservation SHALL NOT require WorksheetObservation.**

Workbook-level properties are observable independently of worksheet-level observations. Whether a parser acquires them by inspecting workbook metadata, reading the worksheet stream, or any other mechanism is an implementation detail outside the ontology.

### Determining Workbook-Level Properties

Workbook-level observable properties describe the **organization and metadata of the workbook itself**. They do not constitute observations of individual worksheets.

This distinction is based on the **level of the source being observed**, not the implementation required to acquire the property.

For example:

- **Worksheet names** are part of the workbook's organizational structure. A workbook organizes its worksheets by name and order, and those names belong to the workbook's description of itself.
- **Row count** belongs to the worksheet being observed. A worksheet contains rows; a workbook does not.

The observable properties of a workbook include:

### Source Identity (via inherited Provenance)

- Source path or identifier
- Source type

### Workbook Format

- File format (e.g., .xlsx, .xls, .xlsb)
- Format version, where applicable

### Workbook Metadata

- Creator or author
- Creation timestamp
- Last modified timestamp
- Application that produced the workbook

### Workbook-Level Settings

- Calculation mode (automatic, manual, automatic except data tables)
- Date system (1900 or 1904)

### Workbook Structure

- Worksheet count
- Worksheet names, in workbook order
- Worksheet ordering (the sequence of worksheets as stored)

These describe the workbook's organization. They do not describe worksheet contents.

### Workbook Protection

- Workbook structure protection state
- Workbook window protection state

### Workbook Visibility

- Workbook visibility state (visible, hidden, very hidden)

---

## Non-Responsibilities

WorkbookObservation does **not** include:

- Worksheet contents (rows, cells, values, formulas)
- Worksheet-level properties (merged ranges, freeze panes, filters, hidden rows/columns, row counts, column counts)
- Named ranges
- BOQ sections or any domain-specific classification
- Validation results
- Business semantics or interpretation

These belong to lower-level specializations (WorksheetObservation, RowObservation, CellObservation) or to downstream ontology families (Evidence, Validation, Knowledge).

---

## Relationship to Observation

WorkbookObservation is an Observation. It inherits:

- **Definition** — an immutable, deterministic record of observable properties
- **Guarantees** — fidelity, determinism, reproducibility, immutability, traceability, independence
- **Provenance** — Source, Observer, Procedure (from `observation_acquisition.md`)
- **Identity** — stable identity for reference throughout lifecycle
- **Lifecycle** — observed → recorded → stored → referenced → archived
- **Invariants** — all eight invariants from `observation.md`, plus acquisition invariants from `observation_acquisition.md`

WorkbookObservation does **not** redefine any of these inherited concepts. It extends Observation only by specifying which observable properties are within scope for a workbook source.

---

## Relationship to Acquisition

WorkbookObservation is acquired through the Observation Acquisition pipeline defined in `observation_acquisition.md`:

```
Workbook Source (possesses observable properties)
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
WorkbookObservation (immutable result)
```

The Procedure for acquiring a WorkbookObservation defines observable boundaries at the workbook level. It specifies which workbook-level properties are within acquisition scope and which are outside (i.e., worksheet-level or lower).

---

## Relationship to WorksheetObservation

WorkbookObservation relates to WorksheetObservation. It does **not** contain WorksheetObservation.

```
WorkbookObservation
        │
        ├── relates to ──► WorksheetObservation
        ├── relates to ──► WorksheetObservation
        └── relates to ──► WorksheetObservation
```

This relationship model preserves:

- **Independent observations** — WorkbookObservation is complete without reading any worksheet
- **Independent lifecycles** — Each observation type has its own lifecycle
- **Independent acquisition** — Workbook and worksheet observations may be acquired separately
- **Independent testing** — Each observation type can be validated independently
- **Independent reuse** — Observations can be referenced individually

An ObservationSet (defined in a future document) aggregates related observations from a single acquisition run. Aggregation is a container concern, not an observation concern.

**WorkbookObservation SHALL NOT require WorksheetObservation.** A valid WorkbookObservation exists without any corresponding WorksheetObservation.

---

## Examples

### Acquired WorkbookObservation

| Property | Value |
|----------|-------|
| Source | `/data/export.xlsx` |
| Format | .xlsx |
| Creator | CostX |
| Worksheets | 1 |
| Worksheet names | ["CostX"] |
| Worksheet ordering | ["CostX"] |
| Calculation mode | fullCalcOnLoad |
| Date system | 1900 |
| Structure protection | False |
| Window protection | False |
| Visibility | visible |

### What This Observation Does Not Contain

- Cell values or formulas
- Row data
- Merged ranges
- Whether the workbook represents a BOQ
- Whether the data is valid

Those are not workbook-level observable properties.

---

## Invariants

In addition to the invariants inherited from `observation.md` and `observation_acquisition.md`:

1. **WorkbookObservation SHALL record only workbook-level observable properties.**
2. **WorkbookObservation SHALL NOT require WorksheetObservation.**
3. **WorkbookObservation SHALL NOT contain worksheet contents.**
4. **WorkbookObservation SHALL identify the workbook source through inherited provenance.**
5. **WorkbookObservation SHALL be acquirable independently of worksheet or lower-level observations.**