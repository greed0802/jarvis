# Object: RowObservation

Category: Core Ontology / Epistemology / Spreadsheet

---

## Purpose

RowObservation is a concrete specialization of the Observation concept. It represents the observable properties of a spreadsheet row at the row level, without requiring cell observations or any interpretation of row contents.

RowObservation applies the specialization pattern established by `workbook.md` and `worksheet.md`.

---

## Definition

RowObservation is an Observation that records the directly observable properties of a spreadsheet row source.

**RowObservation = Observation + Row-specific observable properties.**

RowObservation inherits all guarantees, invariants, and provenance requirements defined in `observation.md` and `observation_acquisition.md`. It does not redefine Observation.

---

## Observable Properties

Every property of RowObservation MUST satisfy the following constraint:

> **RowObservation SHALL NOT require CellObservation.**

Row-level properties are observable independently of cell-level observations. Whether a parser acquires them by inspecting row metadata, reading dimension records, or any other mechanism is an implementation detail outside the ontology.

### Determining Row-Level Properties

Row-level observable properties describe the **position and presentation of the row itself**. They do not constitute interpretations of row contents.

The ownership test is:

> **Does this property describe the row itself, or does it describe subordinate observed objects?**

Applying this test:

- **Row number** identifies the row's position within the worksheet. It is a fact about the row itself.
- **Visibility** and **height** describe the row's presentation state. They are facts about the row itself.
- **Cell count** is ambiguous across formats (allocated, non-empty, physical, or logical). The row's column extent is already defined by the worksheet's column count. Cell count per row is not an intrinsic row property; it is either a worksheet dimension or a derived summary of CellObservations.
- **"Header", "Item", "Heading", "Note"** are interpretations of row contents. They are NOT observable row properties. Classification belongs to downstream ontology families.

The observable properties of a row include:

### Source Identity (via inherited Provenance)

- Source path or identifier
- Worksheet identifier (name or index within the workbook)
- Row identifier (row number within the worksheet)

### Row Identity

- Row number (position within the worksheet, zero-based or one-based as defined by the source format)

### Row Presentation

- Visibility state (visible, hidden)
- Height (row height, where applicable)

---

## Non-Responsibilities

RowObservation does **not** include:

- Cell values (belong to CellObservation)
- Cell formatting (font, fill, alignment, border, number format)
- Cell count (ambiguous across formats; not an intrinsic row property)
- Classification of the row (Header, Item, Heading, Note, or any other semantic label)
- BOQ sections or any domain-specific classification
- Validation results
- Business semantics or interpretation

These belong to lower-level specializations (CellObservation) or to downstream ontology families (Evidence, Validation, Knowledge, semantic layers).

---

## Relationship to Observation

RowObservation is an Observation. It inherits:

- **Definition** — an immutable, deterministic record of observable properties
- **Guarantees** — fidelity, determinism, reproducibility, immutability, traceability, independence
- **Provenance** — Source, Observer, Procedure (from `observation_acquisition.md`)
- **Identity** — stable identity for reference throughout lifecycle
- **Lifecycle** — observed → recorded → stored → referenced → archived
- **Invariants** — all eight invariants from `observation.md`, plus acquisition invariants from `observation_acquisition.md`

RowObservation does **not** redefine any of these inherited concepts. It extends Observation only by specifying which observable properties are within scope for a row source.

---

## Relationship to Acquisition

RowObservation is acquired through the Observation Acquisition pipeline defined in `observation_acquisition.md`:

```
Row Source (possesses observable properties)
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
RowObservation (immutable result)
```

The Procedure for acquiring a RowObservation defines observable boundaries at the row level. It specifies which row-level properties are within acquisition scope and which are outside (i.e., cell-level).

---

## Relationship to WorksheetObservation

RowObservation relates to WorksheetObservation. It does **not** require WorksheetObservation.

```
WorksheetObservation
        │
        ├── relates to ──► RowObservation
        ├── relates to ──► RowObservation
        └── relates to ──► RowObservation
```

This relationship model preserves:

- **Independent observations** — RowObservation is complete without observing the worksheet or any cell
- **Independent lifecycles** — Each observation type has its own lifecycle
- **Independent acquisition** — Row observations may be acquired separately from worksheet or cell observations
- **Independent testing** — Each observation type can be validated independently
- **Independent reuse** — Observations can be referenced individually

An ObservationSet (defined in a future document) aggregates related observations from a single acquisition run. Aggregation is a container concern, not an observation concern.

**RowObservation SHALL NOT require WorksheetObservation or CellObservation.** A valid RowObservation exists without any corresponding WorksheetObservation or CellObservation.

---

## Examples

### Acquired RowObservation

| Property | Value |
|----------|-------|
| Source | `/data/export.xlsx` |
| Worksheet name | "CostX" |
| Row number | 6 |
| Visibility | visible |
| Height | 15.0 |

### What This Observation Does Not Contain

- Cell values or formulas
- Cell count (ambiguous; format-dependent)
- Whether the row is a "Header" or "Item"
- Whether the data is valid

Those are not row-level observable properties.

---

## Invariants

In addition to the invariants inherited from `observation.md` and `observation_acquisition.md`:

1. **RowObservation SHALL record only row-level observable properties.**
2. **RowObservation SHALL NOT require WorksheetObservation or CellObservation.**
3. **RowObservation SHALL NOT contain cell contents or row classifications.**
4. **RowObservation SHALL identify the row source through inherited provenance.**
5. **RowObservation SHALL be acquirable independently of worksheet or cell observations.**