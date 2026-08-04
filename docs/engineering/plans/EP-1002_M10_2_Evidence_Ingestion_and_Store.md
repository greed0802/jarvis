# EP-1002: M10.2 — Evidence Ingestion & Evidence Store

**Status:** OPEN
**Date:** 2026-07-29
**Milestone:** M10.2
**Authors:** Product Engineering
**Frozen ADR Baseline:** ADR-0027, ADR-0028, ADR-0029, ADR-0030, ADR-0031, ADR-0032
**Playbook Reference:** `docs/engineering/Engineering_Execution_Playbook.md`

---

## 1. Objective

Establish the deterministic Evidence Ingestion Layer that accepts validated
upstream BOQ Intelligence outputs and produces immutable `EvidenceReference`
records consumable by the CheckMate capability.

This EP does NOT implement an independent parser or re-evaluate raw
workbook files. Evidence ingestion consumes structured, validated outputs
per C1.1 (Evidence Primacy).

---

## 2. Scope & Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | `EvidenceImporter` protocol | Defines the contract for ingesting validated BOQ Intelligence evidence payloads |
| 2 | `EvidenceStore` class | Backs local workspace evidence storage (files in `workspace/evidence/`) |
| 3 | `EvidenceReference` factory | Creates canonical 7-field records from ingested payloads |
| 4 | 4-tier granularity tagger | Assigns ATOMIC, STRUCTURAL, AGGREGATE, or DERIVED level per C1.4 hierarchy |
| 5 | Immutability lock | Returns explicit error on post-ingestion write attempt at store level |

---

## 3. Architecture Traceability Matrix

| ADR Reference | Decision / Invariant | Planned Implementation | Verification |
|---------------|---------------------|----------------------|-------------|
| ADR-0030 | C1.1 — Evidence Primacy (consumer-only) | EvidenceImporter protocol accepts validated BOQ Intelligence payloads; no raw workbook parsing | Test: importer raises on non-validated payload |
| ADR-0031 | C1.2 — Evidence Grounding (7-field EvidenceReference) | EvidenceReference factory with all 7 canonical fields; source_type enum | Test: round-trip factory produces valid reference |
| ADR-0032 | C1.4 — Evidence Immutability | EvidenceStore.write seals on first import; subsequent write → EvidenceBindingFrozenError | Test: second write attempt raises frozen error |
| ADR-0032 | C1.5 — Deterministic Non-Evaluation | Imported evidence has explicit granularity level; absent evidence handled by downstream rule engine | Test: store lookup for missing evidence returns None |
| ADR-0032 | C1.12 — Contract Compatibility | Factory validates schema compliance; invalid input raises explicit ContractMismatchError | Test: invalid payload raises ContractMismatchError |

---

## 4. Out of Scope

| Excluded Concern | Reason |
|-----------------|--------|
| Independent parsing or reconstruction of raw Excel/PDF files | C1.1 consumer boundary; BOQ Intelligence owns parsing |
| Rule evaluation or Finding generation | Deferred to EP-1003 (CheckMate evaluation engine) |
| Direct LLM prompt integration | M10 Product Workbench concern |
| Modifying or amending ADR-0030 through ADR-0032 | EPS have zero architectural authority |

---

## 5. Acceptance Criteria

| # | Criterion | Pass Condition |
|---|-----------|---------------|
| AC-1 | EvidenceImporter imports validated payload | Imports produce EvidenceReference records |
| AC-2 | EvidenceStore accepts and persists evidence | Stored records survive store close/re-open |
| AC-3 | EvidenceReference factory produces all 7 fields | Factory output rounds to canonical schema |
| AC-4 | Granularity tagger classifies per 4-tier hierarchy | ATOMIC/STRUCTURAL/AGGREGATE/DERIVED assigned correctly |
| AC-5 | Immutability: writable write-blocked post-import | Error on second write to same evidence-id |
| AC-6 | Documentation verifier passes | Exit Code 0 from verify_documentation.py |

---

## 6. Quality Gates

**Tier 1 — Mandatory (MUST pass before promotion):**
- Documentation verifier (`tools/quality/verify_documentation.py`)
- Unit test suite (`pytest`)

**Tier 2 — Extended (DEFERRED during early milestone setup):**
- Static type checker (DEFERRED — Tier 2 not configured)
- Import boundary analysis (DEFERRED — Tier 2 not configured)

---

## 7. Engineering Debt

| ID | Description | Resolution Path |
|----|-------------|----------------|
| ED-004 | EvidenceImporter protocol awaits dependency on BOQ Intelligence output schema | Future CPI: define BOQ Intelligence evidence schema |
| ED-005 | EvidenceStore serialization to JSON; runtime file-based (not indexed DB) | M10.2 design OK; replace with SQLite index in M10.3 |

---

## 8. Completion Record

| Field | Value |
|-------|-------|
| **Completed Date** | |
| **ADR Baseline Verified** | ADR-0027 through ADR-0032 |
| **Quality Gate Result** | |