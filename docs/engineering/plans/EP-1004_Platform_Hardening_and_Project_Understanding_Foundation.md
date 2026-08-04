# EP-1004: M10.4 — Platform Hardening & Project Understanding Foundation

**Status:** OPEN
**Date:** 2026-07-29
**Milestone:** M10.4
**Authors:** Product Engineering
**Frozen ADR Baseline:** ADR-0030, ADR-0031, ADR-0032
**Playbook Reference:** `docs/engineering/Engineering_Execution_Playbook.md`

---

## 1. Objective

Execute two coordinated workstreams:

1. **Workstream A (Platform Hardening):** Resolve engineering debt items ED-006, ED-007, and ED-008 inherited from M10.2/M10.3.
2. **Workstream B (Project Understanding Service):** Build the complete Project Understanding domain — `Importer` → `Store` → `Service` — and expose the `ProjectUnderstanding` public contract for downstream consumption by M10.5 (AI Assistant) and M10.6 (Workbench UI).

This EP hardens the execution pipeline foundations and builds the first downstream consumer of the `FindingReport` public contract, establishing the acyclic capability chain.

---

## 2. Scope & Deliverables

### Workstream A — Platform Hardening

| # | Deliverable | Description |
|---|-------------|-------------|
| A1 | ED-006: Granularity Indexing | Replace `find_by_granularity()` stub in `FileEvidenceRepository` with proper multi-granularity indexing supporting ATOMIC, STRUCTURAL, AGGREGATE, and DERIVED levels |
| A2 | ED-007: Engine Execution Provenance | Move execution provenance generation into `CheckMateEngine`; refactor `FindingReportAssembler` to consume native engine provenance without post-hoc synthesis |
| A3 | ED-008: Snapshot Identity vs. Content Hash | Audit `snapshot_id` (entity identity) vs. `snapshot_hash`/`compute_hash()` (content state); add explicit inline documentation and ensure correct usage for replay/caching |

### Workstream B — Project Understanding Service

| # | Deliverable | Description |
|---|-------------|-------------|
| B1 | `ProjectUnderstanding` public contract | Immutable dataclass defining the technology-agnostic contract for downstream consumers |
| B2 | `ProjectUnderstandingImporter` | Ingests published `FindingReport` contracts exclusively; validates and transforms into internal domain objects |
| B3 | `ProjectUnderstandingStore` | Owns persistent state and query indexes for understanding data; append-only semantics |
| B4 | `ProjectUnderstandingService` | Exposes read/query operations returning the `ProjectUnderstanding` public contract |

---

## 3. Architecture Traceability Matrix

| ADR Reference | Decision / Invariant | Implemented In | Verification |
|---------------|---------------------|---------------|--------------|
| ADR-0030 | C1.1 — Evidence Primacy | EvidenceRepository granularity indexing | Test: find_by_granularity returns correctly indexed evidence for all 4 levels |
| ADR-0030 | C1.3 — Scope Boundary | ProjectUnderstandingImporter consumes only FindingReport | Test: importer rejects non-FindingReport input |
| ADR-0031 | C1.13 — Public Contract Decoupling | ProjectUnderstanding domain SHALL NOT import CheckMateEngine, ExecutionOutcome, RuleSnapshot, RuleRegistry | Test: automated boundary check verifies zero cross-imports |
| ADR-0031 | C1.14 — FindingReport Version Provenance | Engine emits native provenance; assembler consumes it | Test: provenance hash matches engine-generated value |
| ADR-0031 | C1.15 — Report Completeness & Integrity | ProjectUnderstanding is immutable frozen contract | Test: dataclass(frozen=True); post-creation mutation raises |
| ADR-0032 | C1.4 — Evidence Immutability | Granularity tag index on evidence references | Test: index entries are immutable after insert |
| ADR-0032 | C1.9 — Rule Determinism | Snapshot identity vs content hash audited for deterministic replay | Test: hash recomputation matches cached value |
| ADR-0032 | C1.11 — Bound RuleSnapshot Sovereignty | snapshot_id (identity) explicitly distinguished from snapshot_hash (content) | Test: id vs hash comparison; conceptual and programmatic audit |

---

## 4. Acyclic Capability Chain

```text
EvidenceRepository (M10.2)
       │
       ▼
CheckMateEngine → ExecutionOutcome[ ] → FindingReportAssembler → FindingReport (M10.3)
                                                                         │
                                                                         ▼
                                                              ProjectUnderstandingImporter
                                                                         │
                                                                         ▼
                                                                 ProjectUnderstandingStore
                                                                         │
                                                                         ▼
                                                                ProjectUnderstandingService
                                                                         │
                                                                         ▼
                                                                ProjectUnderstanding (Public Contract)
                                                                        │
                                                            ┌───────────┴───────────┐
                                                            ▼                       ▼
                                                    M10.5 AI Assistant      M10.6 Workbench UI
```

**Strict Boundary Rules:**
- `ProjectUnderstanding` domain MUST NOT import `ExecutionOutcome`, `CheckMateEngine`, `RuleSnapshot`, `RuleRegistry`, or `CheckMateRule`.
- `ProjectUnderstandingImporter` SHALL consume only the published `FindingReport` contract.
- `FindingReportAssembler` SHALL operate as a pure consumer of engine provenance data.

---

## 4. ED-006 Detail: Granularity Indexing

Current state (inherited from M10.2):
```python
def find_by_granularity(self, granularity: EvidenceGranularity) -> list[EvidenceReference]:
    return []  # stub
```

Target: Replace with index lookup from a `_granularity_index: dict[EvidenceGranularity, list[EvidenceReference]]` populated during `EvidenceStore.append()` and mirrored in `FileEvidenceRepository`.

The granularity index stores retrieved evidence at all four EvidenceGranularity levels: ATOMIC, STRUCTURAL, AGGREGATE, DERIVED.

---

## 5. ED-007 Detail: Engine Execution Provenance

Current: `FindingReportAssembler.assemble()` computes `execution_id` and `evidence_fingerprint` from outcomes post-hoc (lines 58-75 of assembler.py).

Target:
1. `CheckMateEngine.execute()` produces a `ProvenanceBlock` containing execution_id, evidence_fingerprint, snapshot_hash.
2. `RuleSnapshot` embeds `snapshot_hash` (content hash) alongside `snapshot_id` (identity).
3. `FindingReportAssembler.assemble()` accepts the engine's `ProvenanceBlock` instead of computing it from scratch.

---

## 6. ED-008 Detail: Snapshot Identity vs. Content Hash

Current: `RuleSnapshotMetadata` has `snapshot_id` (a string identity) and `compute_hash()` (the SHA-256 content hash). However, the relationship between these two concepts is not explicitly documented.

Target:
- `snapshot_id` = persistent identity (unchanged across runs even if rule set changes)
- `snapshot_hash` = content fingerprint (SHA-256 over canonical JSON manifest; changes when rules, versions, or capability_version changes)
- Add inline documentation distinguishing both concepts for replay and caching
- Tests verify that `snapshot_id` remains constant while `snapshot_hash` changes after registry mutation

---

## 7. Acceptance Criteria

| # | Criterion | Pass Condition |
|---|-----------|---------------|
| AC-1 | `EvidenceRepository.find_by_granularity()` returns correctly indexed evidence for all 4 granularity levels | Query per level returns non-empty, expected documents |
| AC-2 | `CheckMateEngine` emits native provenance; assembler consumes without post-hoc synthesis | Assembler receives provenance from engine; no duplicate computation |
| AC-3 | `ProjectUnderstandingImporter` consumes only the published `FindingReport` contract | Importer instantiates only from `FindingReport`; rejects raw `ExecutionOutcome` |
| AC-4 | `ProjectUnderstandingService` exposes read/query interface returning immutable `ProjectUnderstanding` contract | Service query methods return `ProjectUnderstanding`; no mutation access |
| AC-5 | All unit and integration tests pass | `pytest` exit code 0 |
| AC-6 | Boundary verification: ProjectUnderstanding components have zero imports of CheckMateEngine internals | Automated import boundary check PASS |

---

## 8. Quality Gates

**Tier 1 — Mandatory (MUST pass before promotion):**
- Documentation verifier (`tools/quality/verify_documentation.py`)
- Unit test suite (`pytest`)

**Tier 2 — Extended (DEFERRED during early milestone setup):**
- Static type checker (DEFERRED)
- Import boundary analysis (DEFERRED)

---

## 9. Engineering Debt

| ID | Description | Classification | Resolution |
|----|-------------|---------------|------------|
| ED-006 | Granularity indexing for EvidenceRepository | Resolved in EP-1004 | Atomic, Structural, Aggregate, Derived indexing |
| ED-007 | Engine execution provenance | Resolved in EP-1004 | Move provenance generation inside CheckMateEngine |
| ED-008 | Snapshot identity vs content hash | Resolved in EP-1004 | Document id/hash distinction |

---

## 10. Evidence Packages

This EP pairs with:
- **EV-1004:** `docs/engineering/evidence/EV-1004_Platform_Hardening_and_Project_Understanding_Foundation.md`

Per the Engineering Execution Playbook §3 Step 5: all promotions are governed by the EV-1004 record, not raw code changes or this plan alone.

---

## 11. Completion Record

| Field | Value |
|-------|-------|
| **Completed Date** | |
| **ADR Baseline Verified** | ADR-0030, ADR-0031, ADR-0032 |
| **Quality Gate Result** | |