# Capability Register

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Active |
| **Owner** | Project Owner |
| **Effective** | 2026-07-13 |
| **Supersedes** | None |

---

## Purpose

This document is the single source of truth for the current state of all capabilities in the Jarvis Platform.

It is a **living document**. It is updated whenever a capability's lifecycle state changes.

It is not a historical record. Historical records are preserved in:

- `docs/planning/Capability_Discovery_001.md` — immutable snapshot of Discovery 001
- `docs/planning/Capability_Evaluation_001.md` — immutable record of Evaluation 001 and Project Owner decision

---

## Document Classification

| Document Type | Examples | Mutable? |
|---------------|----------|:--------:|
| **Historical artifacts** | Discovery 001, Evaluation 001, ADRs, Engineering Questions | No |
| **Operational artifacts** | Capability Register, Capability Roadmap, Implementation Status | Yes |

Historical artifacts preserve what was known or decided at a point in time. Operational artifacts reflect the current state.

---

## Capability States

| Capability | Lifecycle State | Evidence Ready | Implementation Ready | Dependency | Notes |
|------------|:---------------:|:--------------:|:--------------------:|------------|-------|
| **BOQ Intelligence** | Implemented | Yes | Yes | None | Increment 1 complete — 2026-07-14 |
| **Formatter** | Deferred | Partial | No | BOQ Intelligence (prerequisite) | Distinct product capability |
| **CheckMate** | Deferred | Partial | No | BOQ Intelligence (baseline) | Distinct product capability |
| **Cubit Parser** | Deferred | No | No | Fixtures + Engineering Question | Awaiting fixtures |
| **PDF Parser** | Deferred | No | No | None | Insufficient evidence |
| **AI-Assisted Estimation** | Deferred | No | No | BOQ Intelligence + Context Engine + training data | Long-term strategic |

---

## Capability Relationships

```
BOQ Intelligence (Implemented)
        │
        ├── prerequisite for ──▶ Formatter (Deferred)
        │
        ├── baseline for ──▶ CheckMate (Deferred)
        │
        └── foundation for ──▶ AI-Assisted Estimation (Deferred)
```

---

## Active Capability

### BOQ Intelligence

| Property | Value |
|----------|-------|
| **Lifecycle State** | Implemented |
| **Evidence Ready** | Yes |
| **Implementation Ready** | Yes |
| **Approved** | 2026-07-13 |
| **Implemented** | 2026-07-14 |
| **Approval Reference** | `docs/planning/Capability_Evaluation_001.md` |
| **Discovery Reference** | `docs/planning/Capability_Discovery_001.md` |
| **Scope** | Validation, analysis, summaries, exports, and anomaly detection over `list[BOQRow]` |
| **Constraint** | No architectural expansion. Pure functions over existing production types. |

---

## Change Log

| Date | Capability | Previous State | New State | Reason |
|------|------------|:--------------:|:---------:|--------|
| 2026-07-13 | BOQ Intelligence | Proposed | Approved | Capability Evaluation 001 — Project Owner decision |
| 2026-07-13 | Formatter | Proposed | Deferred | Capability Evaluation 001 — depends on BOQ Intelligence |
| 2026-07-13 | CheckMate | Proposed | Deferred | Capability Evaluation 001 — depends on BOQ Intelligence |
| 2026-07-13 | Cubit Parser | Proposed | Deferred | Capability Evaluation 001 — awaiting fixtures |
| 2026-07-13 | PDF Parser | Proposed | Deferred | Capability Evaluation 001 — insufficient evidence |
| 2026-07-13 | AI-Assisted Estimation | Proposed | Deferred | Capability Evaluation 001 — long-term strategic |
| 2026-07-14 | BOQ Intelligence | Approved | Implemented | Increment 1 complete — 73 tests passed, 0 failures |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-13 | Initial creation. Records first Project Owner decisions from Capability Evaluation 001. |
| 1.1 | 2026-07-14 | BOQ Intelligence moves from Approved to Implemented. Increment 1 delivered. |
