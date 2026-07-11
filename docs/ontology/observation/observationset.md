# Object: ObservationSet

Category: Core Ontology / Epistemology / Aggregation

---

## Purpose

ObservationSet is an aggregation construct that groups related Observations produced by a single Observation Acquisition process. It serves as the output contract between acquisition and consumption.

ObservationSet is **not** an Observation. It does not inherit Observation guarantees, provenance, or invariants. It is a container, not a specialization.

---

## Definition

An ObservationSet is an immutable container that aggregates one or more Observations produced by a single Observation Acquisition process.

**ObservationSet = Container of Observations produced by one acquisition run.**

ObservationSet does not redefine Observation. It does not extend Observation. It is a separate construct with its own purpose and lifecycle.

---

## Responsibilities

ObservationSet is responsible for:

- Grouping related Observations from a single acquisition run
- Owning acquisition session metadata (acquisition identifier, timestamp)
- Providing a single output unit for consumers (Memory, Evidence, Validation)
- Maintaining the ordering of Observations as produced

---

## Non-Responsibilities

ObservationSet does **not**:

- Duplicate Observation provenance (Source, Observer, Procedure are owned by each Observation)
- Perform interpretation or inference
- Validate or verify contained Observations
- Transform or modify Observations
- Classify or categorize Observations
- Act as an Observation itself

---

## Acquisition Session Metadata

ObservationSet owns metadata that characterizes the acquisition run as a whole:

- **Acquisition identifier** — a unique identifier for the acquisition session
- **Timestamp** — when the acquisition occurred

These are properties of the acquisition session, not of the individual Observations. Each Observation retains its own provenance (Source, Observer, Procedure) as defined in `observation.md` and `observation_acquisition.md`.

---

## Relationship to Observation

ObservationSet contains Observations. It does **not** extend Observation.

```
ObservationSet
        │
        ├── contains ──► Observation
        ├── contains ──► Observation
        └── contains ──► Observation
```

Each Observation within an ObservationSet retains its own identity, provenance, guarantees, and lifecycle. ObservationSet does not modify or wrap Observations; it aggregates them.

---

## Relationship to Acquisition

ObservationSet is the output of a single Observation Acquisition process, as defined in `observation_acquisition.md`:

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

ObservationSet captures acquisition session metadata (acquisition identifier, timestamp). Individual Observations within the set retain their own provenance (Source, Observer, Procedure).

---

## Contents

An ObservationSet may contain any combination of Observation types:

- WorkbookObservation
- WorksheetObservation
- RowObservation
- CellObservation
- Future specializations (OCRObservation, APIObservation, etc.)

Observations within an ObservationSet are ordered as produced by the acquisition process. Consumers may process them in any order; the ordering is informational, not semantic.

---

## Lifecycle

```
Acquisition Complete
        │
        ▼
ObservationSet Created
        │
        ▼
ObservationSet Delivered
        │
        ▼
Consumers Process
        │
        ▼
ObservationSet Archived
```

ObservationSet is immutable once created. Observations within it are immutable. The set itself is immutable.

---

## Examples

### Parser Output

```
ObservationSet
├── Acquisition Session
│   ├── Acquisition ID: acq-20260711-001
│   └── Timestamp: 2026-07-11T08:00:00Z
│
├── WorkbookObservation
│   ├── Source: /data/export.xlsx (via provenance)
│   ├── Format: .xlsx
│   ├── Worksheets: 1
│   └── ...
│
├── WorksheetObservation
│   ├── Name: "CostX" (via provenance)
│   ├── Row count: 6354
│   └── ...
│
├── RowObservation (×6354)
│   └── ...
│
└── CellObservation (×57186)
    └── ...
```

Note: Source, Observer, and Procedure are owned by each Observation's provenance, not by the ObservationSet. The ObservationSet owns only the acquisition session identifier and timestamp.

---

## Invariants

1. **ObservationSet SHALL contain at least one Observation.**
2. **ObservationSet SHALL NOT modify contained Observations.**
3. **ObservationSet SHALL NOT interpret contained Observations.**
4. **ObservationSet SHALL own acquisition session metadata only** — provenance (Source, Observer, Procedure) belongs to individual Observations.
5. **ObservationSet SHALL be immutable once created.**
6. **ObservationSet SHALL NOT act as an Observation.**