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

| Capability | Lifecycle State | Classification | Evidence Ready | Implementation Ready | Dependency | Notes |
|------------|:---------------:|:-------------:|:--------------:|:-------------------:|------------|-------|
| **BOQ Intelligence** | Active | Strategic | ✅ Yes | ✅ Yes (further increments pending) | None | Increments 1–3 complete. Evidence Contract v1.0 Frozen. Active strategic capability. |
| **Validation Engine** | Frozen Sub-capability | Supporting | ✅ Yes | ✅ Yes (Consumer Ready) | BOQ Intelligence (evidence dependency) | EQ-0013 Frozen — Gate 3 Approved — 2026-07-15. Consumption-ready. |
| **Formatter** | Deferred | Deferred | Partial | No | BOQ Intelligence (prerequisite) | Distinct product capability — export formatting |
| **CheckMate** | Active | Strategic Consumer Application | ✅ Yes | ✅ Yes (IP-0002 Implementation Complete) | BOQ Intelligence (Evidence Contract v1.0) | Distinct product capability — QA validation |
| **Cubit Parser** | Deferred | Deferred | No | No | Fixtures + Engineering Question | Awaiting Cubit export fixtures |
| **PDF Parser** | Deferred | Deferred | No | No | None | Insufficient evidence; fundamentally different extraction problem |
| **AI-Assisted Estimation** | Deferred | Deferred | No | No | BOQ Intelligence + Context Engine + training data | Long-term strategic |
| **Observation Runtime (M6)** | Historical | Historical | N/A | N/A | None | Architectural evaluation by ADR-0025; production rejected; artifacts preserved as Historical Engineering |

---

## Capability Relationships

```
BOQ Intelligence (Implemented)
        │
        ├── evidence for ──▶ Validation Engine (Implemented)
        │
        ├── prerequisite for ──▶ Formatter (Deferred)
        │
        ├── consumed by ──▶ CheckMate (Implemented)
        │
        └── foundation for ──▶ AI-Assisted Estimation (Deferred)
```

---

## Active Capabilities

### BOQ Intelligence

| Property | Value |
|----------|-------|
| **Lifecycle State** | Active |
| **Classification** | Active |
| **Evidence Ready** | Yes |
| **Implementation Ready** | Yes (Next increments pending) |
| **Approved** | 2026-07-13 |
| **Increments Delivered** | Increments 1–4 (2026-07-25) |
| **Evidence Contract** | v1.1.0 Frozen (2026-07-25) |
| **Implementation Package** | IP-0001 — Permanently Frozen |
| **IP Freeze Date** | 2026-07-25 |
| **Approval Reference** | `docs/planning/Capability_Evaluation_001.md` |
| **Discovery Reference** | `docs/planning/Capability_Discovery_001.md` |
| **Scope** | Validation, analysis, summaries, exports, and anomaly detection over `list[BOQRow]` |
| **Constraint** | No architectural expansion. Pure functions over existing production types. |

### Validation Engine
### CheckMate

| Property | Value |
|----------|-------|
| **Lifecycle State** | Active |
| **Classification** | Strategic Consumer Application |
| **Evidence Ready** | Yes |
| **Implementation Ready** | Yes (IP-0002 Complete) |
| **Approved** | 2026-07-26 |
| **Implementation Package** | IP-0002 — CheckMate Application — Consumer Architecture |
| **Engineering Questions** | EQ-0020 (Consumer Arch), EQ-0021 (App Arch) |
| **Scope** | First BOQ Intelligence consumer. Star-topology architecture. Standalone Application consuming `BOQIntelligenceResult` via Evidence Contract. |
| **Constraint** | No Kernel registration. No lifecycle management. Pure consumer. |



| Property | Value |
|----------|-------|
| **Lifecycle State** | Frozen Sub-capability |
| **Classification** | Frozen Sub-capability |
| **Evidence Ready** | Yes |
| **Implementation Ready** | Yes (Consumer Ready) |
| **Approved** | 2026-07-15 |
| **Engineering Question** | EQ-0013 |
| **Contract** | `docs/contracts/Validation_Findings_Contract_v1.0.md` |
| **Scope** | Deterministic validation engine consuming BOQ Intelligence evidence; produces immutable `ValidationFindings` |
| **Constraint** | Observes and Detects only. Does NOT Assess, Judge, or Recommend (EQ-0011 boundary). |

### BOQ Intelligence — Semantic Capabilities (Increment 4 — IP-0001)

The following 8 semantic sub-capabilities were implemented under IP-0001 (PERMANENTLY FROZEN) and are governed by EQ-0019:

| ID | Capability | Status | Evidence Source |
|----|-----------|--------|-----------------|
| SEM-PROD-01 | Vocabulary Extraction | Implemented — Frozen | EQ-0019 Spike 3 |
| SEM-PROD-02 | Head1 Text Categorization | Implemented — Frozen | EQ-0019 Spike 3 |
| SEM-PROD-04 | Administrative Pattern Detection | Implemented — Frozen | EQ-0019 Spike 3 |
| SEM-PROD-05 | Section Code Enumeration | Implemented — Frozen | EQ-0019 Spike 3 |
| SEM-PROD-06 | UOM Distribution Reporting | Implemented — Frozen | EQ-0019 Spike 3 |
| SEM-PROD-07 | Header Level Count Distribution | Implemented — Frozen | EQ-0019 Spike 3 |
| SEM-PROD-09 | "Items Always Quantify" Enforcement | Implemented — Frozen | EQ-0019 Spike 3 |
| SEM-PROD-12 | Administrative Sub-Template Recognition | Implemented — Frozen | EQ-0019 Spike 3 |

**Deferred (not implemented):** SEM-PROD-03, SEM-PROD-08, SEM-PROD-10, SEM-PROD-11

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
| 2026-07-14 | BOQ Intelligence | Approved | Active | Increments 1–3 complete — 73 tests passed, 0 failures |
| 2026-07-15 | Validation Engine | Proposed | Frozen Sub-capability | EQ-0013 Frozen — 4 spikes complete — Gate 3 Approved |
| 2026-07-22 | BOQ Intelligence | Implemented → Active | Refined classification. Increments frozen, capability still evolving. CB-0001. |
| 2026-07-22 | Validation Engine | Implemented → Frozen Sub-capability | Refined classification. Contract-frozen consumer. CB-0001. |
| 2026-07-22 | Observation Runtime (M6) | Unlisted → Historical | Added as Historical artifact. ADR-0025 rejected. CB-0001. |
| 2026-07-26 | CheckMate | Deferred → Active | CP-0001 Sprint Complete. CheckMate approved as BOQ Consumer Application. IP-0002 Frozen. |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-13 | Initial creation. Records first Project Owner decisions from Capability Evaluation 001. |
| 1.1 | 2026-07-14 | BOQ Intelligence moves from Approved to Active. Increment 1 delivered. |
| 1.2 | 2026-07-22 | CB-0001 baseline alignment. Introduced Classification column, Frozen Sub-capability state, Historical entries. BOQ Intelligence reclassified as Active. Validation Engine reclassified as Frozen Sub-capability. Observation Runtime (M6) added as Historical. |
