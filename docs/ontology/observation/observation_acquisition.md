# Observation Acquisition

Category: Core Ontology / Epistemology

---

## Purpose

Observation Acquisition defines the deterministic process by which Observations are produced from Sources. It establishes the acquisition pipeline — the transition from observable properties in a Source to an immutable Observation record.

Observation Acquisition is the bridge between the external world (Sources with observable properties) and the internal world (Observations that downstream subsystems may consume as evidence).

---

## The Acquisition Pipeline

Observation Acquisition follows a deterministic sequence:

```
Source (possesses observable properties)
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
Observation (immutable result)
```

### Source

A Source is the origin of observable properties. Sources possess information that may be acquired but never perform acquisition themselves.

*Referenced from `observation.md` — Provenance.*

### Observer

An Observer is the entity that performs acquisition. Observers execute Procedures to acquire observable properties from Sources.

*Referenced from `observation.md` — Provenance.*

### Procedure

A Procedure is a deterministic method executed by an Observer to acquire observable properties from a Source and produce an Observation.

Procedure is the third element of Provenance, alongside Source and Observer.

---

## Procedure

### Definition

A Procedure is a deterministic method, independently describable, that specifies:

- Which observable properties are within acquisition scope
- How those properties are acquired from a Source
- Under what conditions acquisition occurs

### Independence

A Procedure SHALL be specified independently of any concrete Observer implementation.

Multiple Observer implementations may execute the same Procedure while producing equivalent Observations.

For example:

```
Procedure: Read Cell Value
    Input:  Worksheet, Row, Column
    Output: Cell value, Cell type, Cell format

Observer A:  WorkbookParser (Python)
Observer B:  WorkbookParser (Rust)
Observer C:  WorkbookParser (.NET)
```

All three Observers execute the same Procedure. The resulting Observations are equivalent.

### Observable Boundaries

A Procedure SHALL define precisely which observable properties are within its scope and which are outside its scope.

Within scope:

- Cell values
- Cell types
- Cell formats
- Worksheet names
- Row counts

Outside scope:

- Whether a value represents a quantity
- Whether a heading identifies a BOQ section
- Whether data is valid

The latter are interpretations and belong to downstream processes.

### Determinism

A Procedure SHALL be deterministic. Given equivalent Source state, equivalent Procedure, and equivalent execution conditions, a Procedure SHALL produce an equivalent Observation.

---

## Relationship to Provenance

Provenance in `observation.md` defines:

- **Source** — the origin of observed information
- **Observer** — the entity that acquires observable properties

Observation Acquisition adds:

- **Procedure** — the deterministic method executed by the Observer

Together, these three elements form the complete provenance of every Observation. An Observation is fully traceable when its Source, Observer, and Procedure are identifiable.

---

## Observation Acquisition SHALL NOT Perform Interpretation

Observation Acquisition records observable properties only.

Classification, inference, validation, explanation, and semantic interpretation belong to downstream ontology families and shall not be performed during acquisition.

This constraint is the defining boundary of the acquisition process. It preserves fidelity and ensures that Observations remain interpretation-free evidence.

---

## Architectural Invariants

In addition to the invariants defined in `observation.md`, the following invariants govern Observation Acquisition:

1. **Observation SHALL originate from exactly one Source.**
2. **Observation SHALL be produced by exactly one Observer executing exactly one Procedure.**
3. **Procedure SHALL be specified independently of any concrete Observer implementation.**
4. **Procedure SHALL define observable boundaries** — which properties are within acquisition scope and which are outside.
5. **Observers SHALL NOT modify the Source during acquisition** unless explicitly defined by the Source's protocol.
6. **Observation Acquisition SHALL NOT perform interpretation.**

---

## Acquisition Lifecycle

The Acquisition Lifecycle is distinct from the Observation Lifecycle defined in `observation.md`:

```
Source
    │
    ▼
Observation Acquisition
    │
    ▼
Observation
    │
    └── may be aggregated into
            ▼
      ObservationSet
    │
    ▼
Consumers
```

One or more Observations may be aggregated into an ObservationSet for consumption by downstream systems. ObservationSet is a container, not a transformation stage.

### Layer Separation

Acquisition belongs to the Acquisition Layer. Consumers — including Memory, Evidence, and Knowledge — belong to the Knowledge Layer.

```
Acquisition Layer
────────────────────────
Source
Observer
Procedure
Observation

Knowledge Layer
────────────────────────
Memory
Evidence
Knowledge
Validation
```

This separation ensures that acquisition remains independent of interpretation and validation.

---

## Examples

### Excel Workbook Acquisition

| Element | Instance |
|---------|----------|
| Source | Excel workbook file |
| Observer | WorkbookParser |
| Procedure | Open workbook → Locate worksheet → Iterate rows → Read cells |
| Observation | WorkbookObservation containing cell values, types, and formats |

### OCR Document Acquisition

| Element | Instance |
|---------|----------|
| Source | PDF document |
| Observer | OCR Engine |
| Procedure | Load image → Detect text regions → Recognize characters → Emit text |
| Observation | OCRObservation containing recognized text with positions |

### API Response Acquisition

| Element | Instance |
|---------|----------|
| Source | HTTP endpoint |
| Observer | HTTP Client |
| Procedure | Construct request → Perform GET → Parse response → Extract fields |
| Observation | APIObservation containing response data |

---

## Non-Responsibilities

Observation Acquisition does **not** define:

- How Observations are stored (belongs to Memory)
- How Observations become evidence (belongs to Evidence)
- How Observations are validated (belongs to Validation)
- How Observations become knowledge (belongs to Learning)
- How Procedures are implemented (belongs to concrete Observers)
- How Sources are discovered or accessed (belongs to the platform's resource acquisition mechanisms)