# Observation Ontology Family

## Purpose

The Observation ontology family defines how Jarvis acquires raw observable properties from external sources. It establishes a trustworthy, reproducible boundary between information acquisition and internal reasoning.

Observation is the foundational ontology through which externally acquired information enters the Jarvis reasoning pipeline. Any component responsible for acquiring information from external sources — including information originating from parsers, sensors, scanners, importers, APIs, and human interactions — shall emit observations rather than interpreted data.

---

## Design Principles

The Observation ontology family is governed by the following principles:

- **Documentation First** — Specifications precede implementation.
- **Evidence Before Promotion** — Observations are facts; interpretation requires evidence.
- **Acquisition Before Interpretation** — Observation records; downstream processes interpret.
- **Provenance Preservation** — Every observation shall be traceable to its source.
- **Deterministic Engineering** — Observation processes shall be repeatable and predictable.
- **Separation of Observation from Knowledge** — Observation is the input; Knowledge is the validated output.

---

## Inheritance

Every specialization in the Observation ontology family SHALL satisfy the normative requirements defined in `observation.md`.

Specializations may extend the observable properties defined for a particular source type but SHALL NOT weaken or redefine the guarantees established by the root Observation concept.

## Exclusive Observable Property Ownership

Every observable property in the Observation ontology family SHALL belong to exactly one specialization level.

A property observable at the workbook level SHALL NOT be observable at the worksheet, row, or cell level. A property observable at the worksheet level SHALL NOT be observable at the row or cell level. A property observable at the row level SHALL NOT be observable at the cell level.

This rule ensures:

- **No ambiguity** — Every property has a single, well-defined home.
- **No duplication** — The same fact is never recorded at multiple levels.
- **Clear delegation** — Lower-level specializations know exactly which properties they own and which they delegate upward.

Enforcement: If a property appears to belong to multiple levels, the ownership test (does it describe the source at this level or a subordinate level?) determines the single correct placement.

---

## Scope

This ontology family defines:

- The abstract Observation concept
- Observation acquisition semantics
- Observation specializations
- Observation containers
- Relationships between observation concepts

It does not define:

- Memory
- Knowledge
- Evidence
- Validation
- Business semantics

---

## Directory Layout

```
observation/
│
├── README.md                     ← This file. Family overview.
├── observation.md                ← Root concept. Normative (v1.0).
├── observation_acquisition.md    ← Acquisition pipeline and Procedure concept. Normative (v1.0).
├── workbook.md                   ← Normative (v1.0). Spreadsheet workbook specialization.
├── worksheet.md                  ← Normative (v1.0). Spreadsheet worksheet specialization.
├── row.md                        ← Normative (v1.0). Spreadsheet row specialization.
├── cell.md                       ← Normative (v1.0). Spreadsheet cell specialization.
└── observationset.md             ← Normative (v1.0). Container for Observations produced by a single acquisition run.
```

---

## Concepts

| Document | Status | Description |
|----------|--------|-------------|
| `observation.md` | Normative (v1.0) | Root concept defining the Observation abstraction. |
| `observation_acquisition.md` | Normative (v1.0) | Acquisition pipeline and Procedure concept. |
| `workbook.md` | Normative (v1.0) | Spreadsheet workbook specialization. |
| `worksheet.md` | Normative (v1.0) | Spreadsheet worksheet specialization. |
| `row.md` | Normative (v1.0) | Spreadsheet row specialization. |
| `cell.md` | Normative (v1.0) | Spreadsheet cell specialization. |
| `observationset.md` | Normative (v1.0) | Container for Observations produced by a single acquisition run. |

---

## Relationship to Other Ontology Families

Observation is the entry point to Jarvis's evidence pipeline:

```
Observation
      │
      ▼
Memory
      │
      ▼
Evidence
      │
      ▼
Validation
      │
      ▼
Knowledge
```

Observation does **not** depend on Memory, Context, Knowledge, Planner, Workflow, or Skills. It remains valid even when consumed by no other subsystem.

---

## Core Guarantees

All specializations in this family inherit these guarantees and shall not weaken them:

- **Fidelity** — Represents exactly what was recorded, whether or not the observer was correct
- **Determinism** — No nondeterministic differences in equivalent observations
- **Reproducibility** — Same procedure under equivalent conditions produces equivalent results
- **Immutability** — Never modified after creation
- **Traceability** — Source, observer, timestamp, and method are identifiable
- **Independence** — No interpretation, inference, or business meaning

---

## Observation Pipeline

The acquisition pipeline is defined in `observation_acquisition.md`:

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

Everything after Observation belongs to downstream ontology families.

---

## Non-Goals

This ontology family does **not** define:

- How observations are stored (belongs to Memory)
- How observations become evidence (belongs to Evidence)
- How observations become knowledge (belongs to Validation and Knowledge)
- How specific sources are observed (belongs to implementation)
- How observations are serialized or transmitted (belongs to implementation)
- Business interpretation (belongs to domain-specific parsers and semantic layers)