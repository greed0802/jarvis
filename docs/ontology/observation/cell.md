# Object: CellObservation

Category: Core Ontology / Epistemology / Spreadsheet

---

## Purpose

CellObservation is the final concrete specialization in the spreadsheet observation hierarchy. It represents the directly observable properties of a single spreadsheet cell, without any interpretation of the cell's value or meaning.

CellObservation completes the specialization chain: Workbook → Worksheet → Row → Cell.

---

## Definition

CellObservation is an Observation that records the directly observable properties of a spreadsheet cell source.

**CellObservation = Observation + Cell-specific observable properties.**

CellObservation inherits all guarantees, invariants, and provenance requirements defined in `observation.md` and `observation_acquisition.md`. It does not redefine Observation.

---

## Observable Properties

Every property of CellObservation MUST satisfy the following constraint:

> **CellObservation SHALL record only directly observable cell properties.**

The ownership test is:

> **Does this property describe the cell itself, or is it an interpretation of the cell's contents?**

Applying this test:

- **Coordinate**, **value**, **formula**, **data type** are intrinsic properties of the cell as stored in the source.
- **Number format**, **font**, **fill**, **alignment**, **border**, **protection** are presentation properties of the cell itself.
- **Merged** indicates whether the cell is part of a merged range — a structural fact about the cell's geometry.
- **Comment** records whether a comment or note is attached — a fact about the cell's annotation state.
- **Quantity**, **Description**, **Rate**, **Total**, **Unit** are interpretations of the cell's meaning. They are NOT observable cell properties.

The observable properties of a cell include:

### Coordinate

- Row (numeric position within the worksheet)
- Column (numeric position or column identifier within the worksheet)
- Reference (A1-style or equivalent coordinate reference)

### Value

- Raw value as stored in the source (string, number, boolean, date, error)

### Formula

- Formula expression, if present in the source
- Calculated value, if the source provides a pre-computed result

### Data Type

- The cell's data type as defined by the source (string, number, boolean, date, datetime, error)

### Number Format

- The display format mask applied to the cell's value (e.g., "#,##0.00", "mm/dd/yyyy", "0%")

### Presentation

- Font attributes (typeface, size, bold, italic, underline, color, strikethrough)
- Fill attributes (background color, pattern style, pattern color)
- Alignment attributes (horizontal alignment, vertical alignment, wrap text, indent, rotation)
- Border attributes (style and color for top, bottom, left, right, diagonal)

### Cell Behavior

- Protection state (locked, hidden)
- Merged state (whether the cell is part of a merged range)

### Annotations

- Comment or note present (binary indicator; the comment content itself is observable, not its meaning)

---

## Non-Responsibilities

CellObservation does **not** include:

- Interpretation of the cell's value (quantity, description, rate, total, unit, heading, subtotal)
- Classification of the cell's role (BOQ field, identifier, label, summary)
- Validation of the cell's value (correct, incorrect, missing, anomalous)
- Business semantics (cost, measurement, specification, reference)

These interpretations belong to downstream ontology families (Evidence, Validation, Knowledge) or to domain-specific semantic layers (CostX, BOQ, quantity surveying).

---

## Relationship to Observation

CellObservation is an Observation. It inherits:

- **Definition** — an immutable, deterministic record of observable properties
- **Guarantees** — fidelity, determinism, reproducibility, immutability, traceability, independence
- **Provenance** — Source, Observer, Procedure (from `observation_acquisition.md`)
- **Identity** — stable identity for reference throughout lifecycle
- **Lifecycle** — observed → recorded → stored → referenced → archived
- **Invariants** — all eight invariants from `observation.md`, plus acquisition invariants from `observation_acquisition.md`

CellObservation does **not** redefine any of these inherited concepts. It extends Observation only by specifying which observable properties are within scope for a cell source.

---

## Relationship to Acquisition

CellObservation is acquired through the Observation Acquisition pipeline defined in `observation_acquisition.md`:

```
Cell Source (possesses observable properties)
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
CellObservation (immutable result)
```

The Procedure for acquiring a CellObservation defines observable boundaries at the cell level. It specifies which cell-level properties are within acquisition scope and which are outside (i.e., interpretations of the cell's meaning).

---

## Relationship to RowObservation

CellObservation relates to RowObservation. It does **not** require RowObservation.

```
RowObservation
        │
        ├── relates to ──► CellObservation
        ├── relates to ──► CellObservation
        └── relates to ──► CellObservation
```

This relationship model preserves:

- **Independent observations** — CellObservation is complete without observing the row
- **Independent lifecycles** — Each observation type has its own lifecycle
- **Independent acquisition** — Cell observations may be acquired independently
- **Independent testing** — Each observation type can be validated independently
- **Independent reuse** — Observations can be referenced individually

An ObservationSet (defined in a future document) aggregates related observations from a single acquisition run. Aggregation is a container concern, not an observation concern.

**CellObservation SHALL NOT require RowObservation.** A valid CellObservation exists without any corresponding RowObservation.

---

## Examples

### Acquired CellObservation

| Property | Value |
|----------|-------|
| Source | `/data/export.xlsx` |
| Row | 4 |
| Column | 1 |
| Reference | A4 |
| Value | "Code" |
| Data type | string |
| Formula | None |
| Calculated value | None |
| Number format | General |
| Font | Calibri, 8pt, bold |
| Fill | None |
| Alignment | horizontal center |
| Border | None |
| Locked | True |
| Hidden | False |
| Merged | False |
| Comment | None |

### Acquired CellObservation (with formula)

| Property | Value |
|----------|-------|
| Source | `/data/export.xlsx` |
| Row | 10 |
| Column | 6 |
| Reference | F10 |
| Value | 1250.00 |
| Data type | number |
| Formula | "=C10*E10" |
| Calculated value | 1250.00 |
| Number format | "#,##0.00" |
| Font | Calibri, 8pt |
| Fill | None |
| Alignment | horizontal right |
| Border | None |

### What These Observations Do Not Contain

- Whether the value is a "Quantity" or "Rate"
- Whether the cell is a header or a data item
- Whether the formula is correct
- Whether the value is expected for a BOQ field

Those are not cell-level observable properties.

---

## Invariants

In addition to the invariants inherited from `observation.md` and `observation_acquisition.md`:

1. **CellObservation SHALL record only cell-level observable properties.**
2. **CellObservation SHALL NOT require RowObservation.**
3. **CellObservation SHALL NOT contain interpretations of the cell's value or meaning.**
4. **CellObservation SHALL identify the cell source through inherited provenance.**
5. **CellObservation SHALL be acquirable independently of row observations.**