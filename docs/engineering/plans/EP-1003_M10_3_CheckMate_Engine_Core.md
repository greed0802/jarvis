# EP-1003: M10.3 — CheckMate Engine Core & Vertical Slice

**Status:** OPEN
**Date:** 2026-07-29
**Milestone:** M10.3
**Authors:** Product Engineering
**Frozen ADR Baseline:** ADR-0030, ADR-0031, ADR-0032
**Playbook Reference:** `docs/engineering/Engineering_Execution_Playbook.md`

---

## 1. Objective

Build the deterministic CheckMate rule evaluation engine, rule registry,
`RuleSnapshot` execution manifest, internal `ExecutionOutcome` model,
`FindingReportAssembler`, and a 5-category vertical slice exercising all 16
invariants from ADR-0030 through ADR-0032.

This EP implements the frozen CheckMate architecture. It does NOT create new
capability boundaries, amend invariant wording, or produce any output outside
the `FindingReport` public contract.

---

## 2. Scope & Deliverables

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | `Rule` protocol | Self-contained evaluation unit with domain category, min evidence threshold, parameter schema, version, contract compatibility assertions (C1.10) |
| 2 | `ExecutionOutcome` (internal) | Immutable per-rule result: `rule_id`, `status` (PASS/FAIL/NOT_APPLICABLE/UNEVALUABLE_MISSING_EVIDENCE), `evidence` references, telemetry, `optional_finding` (C1.7) |
| 3 | `RuleRegistry` | Canonical registry for registering self-contained rules and compiling immutable `RuleSnapshot` (C1.11) |
| 4 | `RuleSnapshot` manifest | Immutable execution manifest: rule list, rule versions, capability version, execution order, deterministic hash (C1.11, C1.14) |
| 5 | `CheckMateEngine` | Runner that executes a `RuleSnapshot` against `EvidenceRepository` producing `ExecutionOutcome[]` (C1.5, C1.9, C1.12) |
| 6 | `FindingReportAssembler` | Processes `ExecutionOutcome[]` into the public 4-tier `FindingReport` with provenance block (C1.13, C1.14, C1.15) |
| 7 | 5 Vertical-Slice Rules | Representative rules across canonical QS domain categories exercising all 16 invariants |

---

## 3. Architecture Traceability Matrix

| ADR Reference | Decision / Invariant | Planned Implementation | Verification |
|---------------|---------------------|----------------------|-------------|
| ADR-0030 | C1.1 — Evidence Primacy (consumer-only) | CheckMateEngine reads from EvidenceRepository; no raw workbook parsing | Test: engine rejects non-EvidenceRepository inputs |
| ADR-0030 | C1.3 — Scope Boundary | FindingReportAssembler produces only FindingReport; no summary, chat, or rendering logic | Test: assembler output is exactly FindingReport type |
| ADR-0030 | C1.8 — Domain Rule Taxonomy (6 categories) | All 5 vertical-slice rules declare domain category at registration; RuleRegistry validates classification | Test: registry rejects unclassified rules |
| ADR-0030 | C1.16 — Vertical Slice Completeness (min 5 rules, 4 categories) | 5 rules across MEASUREMENT/COMPLIANCE/SPECIFICATION/COORDINATION/DOCUMENTATION_INTEGRITY | Test: vertical slice FindingReport covers all 5 outcomes |
| ADR-0031 | C1.2 — Evidence Grounding (7-field EvidenceReference per Finding) | Every FAIL-generated Finding references ≥1 EvidenceReference | Test: FAIL Finding evidence non-empty |
| ADR-0031 | C1.6 — Finding Actionability & Provenance | FindingReportAssembler attaches severity, evidence provenance, and remediation to every Finding | Test: all FAIL findings have severity and remediation fields populated |
| ADR-0031 | C1.7 — Execution Outcome Separation | ExecutionOutcome records all outcomes; FindingReportAssembler filters only FAIL → Findings | Test: PASS/UNEQUIVABLE outcomes produce zero Findings |
| ADR-0031 | C1.13 — Public Contract Decoupling | FindingReportAssembler exposes FindingReport; internal engine state, registry internals, and outcome vectors are never in the public contract | Test: FindingReport schema matches defined sections only |
| ADR-0031 | C1.14 — FindingReport Version Provenance | Provenance block: execution_id, evidence_fingerprint, rule_snapshot_hash, capability_version | Test: provenance block populated and hash-verifiable |
| ADR-0031 | C1.15 — Report Completeness & Integrity | Assembler produces a single, immutable report; no partial or incremental composition | Test: report is frozen dataclass; no post-creation mutation |
| ADR-0032 | C1.4 — Evidence Immutability | RuleSnapshot binds evidence at execution start; no evidence mutation during rule evaluation | Test: snapshot bound evidence cannot be changed |
| ADR-0032 | C1.5 — Deterministic Non-Evaluation (UNEVALUABLE on missing evidence) | Engine produces UNEVALUABLE_MISSING_EVIDENCE when required evidence is absent; no silent skip | Test: completeness rule fails with UNEVALUABLE on empty store |
| ADR-0032 | C1.9 — Rule Determinism | Same evidence + same RuleSnapshot → identical outcomes every time | Test: two runs produce identical ExecutionOutcome vectors |
| ADR-0032 | C1.10 — Rule Self-Containment | Each rule declares domain, minimum evidence level, parameter schema, version, contract compatibility | Test: rules evaluated independently; no inter-rule side effects |
| ADR-0032 | C1.11 — Bound RuleSnapshot Sovereignty | RuleSnapshot hash is immutable; rules are not added/removed post-capture | Test: snapshot modification after creation |
| ADR-0032 | C1.12 — Contract Compatibility Boundary | Rules declare contract boundary; mismatched evidence → UNEVALUABLE_MISSING_EVIDENCE | Test: rule with unsatisfied contract yields UNEVALUABLE |

---

## 4. Domain Taxonomy & Vertical Slice Rules

| Rule (Asset) | Domain Category | Expected Outcome | Invariants Exercised |
|--------------|----------------|--------------------|------------------|
| **Quantity Validation** | MEASUREMENT | PASS | C1.5, C1.9, C1.10, C1.11, C1.12 |
| **Standards Adherence** | COMPLIANCE | FAIL → Finding | C1.2, C1.6, C1.7, C1.13, C1.14, C1.15 |
| **Conformance Check** | SPECIFICATION | FAIL → Finding | C1.2, C1.6, C1.7, C1.9, C1.13 |
| **Cross-Reference Check** | COORDINATION | FAIL → Finding | C1.2, C1.6, C1.7, C1.10, C1.14 |
| **Data Completeness** | DOCUMENTATION_INTEGRITY | UNEVALUABLE_MISSING_EVIDENCE | C1.5, C1.7, C1.12, C1.15 |

---

## 5. Out of Scope

| Excluded Concern | Reason |
|-----------------|--------|
| Direct LLM prompt integrations or AI Assistant context synthesis | M10 Product Workbench concern (ADR-0030 non-goals) |
| UI report rendering or PDF layout generation | Formatter capability concern (ADR-0030 non-goals) |
| Modifying frozen ADR-0030, ADR-0031, or ADR-0032 | EP-1003 has zero architectural authority per Engineering Execution Playbook §2 |
| New domain categories beyond the 6 canonical categories | Requires ADR-0030 amendment per ADR-0030 C1.8 |
| Post-run evidence re-ingestion or re-binding | Evidence is frozen per run per C1.4 |
| End-to-end integration with BOQ Intelligence artifacts | BOQ Intelligence owns its own stages; EP-1003 tests operate on synthetic EvidenceReference records |

---

## 6. Acceptance Criteria

| # | Criterion | Pass Condition |
|---|-----------|---------------|
| AC-1 | Rule protocol defines self-contained evaluation units | All 5 vertical-slice rules implement the Rule protocol and register with RuleRegistry |
| AC-2 | RuleRegistry compiles immutable RuleSnapshot with deterministic hash | RuleSnapshot has fixed hash for same registry state; hash changes on registry mutation |
| AC-3 | ExecutionOutcome properly reflects PASS, FAIL, and UNEVALUABLE outcomes | Engine produces correct outcomes for each vertical-slice rule |
| AC-4 | Rule determinism: identical inputs produce identical outputs | Two engine runs with frozen snapshot and same evidence produce identical outcome vectors |
| AC-5 | Telemetry outcome separation: only FAIL outcomes generate Findings | PASS and UNEVALUABLE outcomes produce zero Findings in assembled report |
| AC-6 | Missing evidence produces UNEVALUABLE outcome, not crash or silent skip | Completeness rule with empty repository yields UNEVALUABLE, not exception/omission |
| AC-7 | FindingReportAssembler produces complete 4-tier report | Assembled report contains provenance, telemetry summary, actionable findings, domain coverage |
| AC-8 | Documentation verifier exits code 0 | exit code 0 from verify_documentation.py |

---

## 7. Quality Gates

**Tier 1 — Mandatory (MUST pass before promotion):**
- Documentation verifier (`tools/quality/verify_documentation.py`)
- Unit test suite (`pytest`)

**Tier 2 — Extended (DEFERRED during early milestone setup):**
- Static type checker (DEFERRED — Tier 2 not configured)
- Import boundary analysis (DEFERRED — Tier 2 not configured)

---

## 8. Engineering Debt

| ID | Description | Classification | Resolution Path |
|----|-------------|----------------|----------------|
| ED-006 | Granularity indexing for EvidenceRepository searches by granularity is not yet implemented | **Inherited** from M10.2 | Awaiting: build granularity tag index in `FileEvidenceRepository` during evidence ingestion |

---

## 9. Evidence Packages

This EP pairs with:
- **EV-1003:** `docs/engineering/evidence/EV-1003_M10_3_CheckMate_Engine_Core.md`

Per the Engineering Execution Playbook §3 Step 5: all promotions are governed by the EV-1003 record, not raw code changes or this plan alone.

---

## 10. Completion Record

| Field | Value |
|-------|-------|
| **Completed Date** | |
| **ADR Baseline Verified** | ADR-0030, ADR-0031, ADR-0032 |
| **Quality Gate Result** | |