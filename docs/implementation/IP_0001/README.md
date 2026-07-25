# IP-0001 — BOQ Intelligence Increment 4

## Status

**PERMANENTLY FROZEN**

**Freeze Date:** 2026-07-25

**Project Owner Approval:** APPROVED

## Source Engineering Question

[EQ-0019 — BOQ Semantic Intelligence Increment 1](../../engineering/questions/EQ_0019_BOQ_Semantic_Intelligence_Increment_1.md)

**Status:** PERMANENTLY FROZEN

**Disposition:** 8 Production Ready capabilities authorized. Deferred capabilities (SEM-PROD-03, SEM-PROD-08, SEM-PROD-10, SEM-PROD-11) remain deferred.

## Implementation Governance

**Governed by:** [Implementation_Governance.md](../../engineering/Implementation_Governance.md) v1.0

## Authorized Capabilities

| ID | Capability | Status | Evidence Source |
|----|-----------|--------|-----------------|
| SEM-PROD-01 | Vocabulary Extraction | Implemented | EQ-0019 Spike 3 |
| SEM-PROD-02 | Head1 Text Categorization | Implemented | EQ-0019 Spike 3 |
| SEM-PROD-04 | Administrative Pattern Detection | Implemented | EQ-0019 Spike 3 |
| SEM-PROD-05 | Section Code Enumeration | Implemented | EQ-0019 Spike 3 |
| SEM-PROD-06 | UOM Distribution Reporting | Implemented | EQ-0019 Spike 3 |
| SEM-PROD-07 | Header Level Count Distribution | Implemented | EQ-0019 Spike 3 |
| SEM-PROD-09 | "Items Always Quantify" Enforcement | Implemented | EQ-0019 Spike 3 |
| SEM-PROD-12 | Administrative Sub-Template Recognition | Implemented | EQ-0019 Spike 3 |

## Deferred Capabilities (Not Implemented)

| ID | Capability | Reason |
|----|-----------|--------|
| SEM-PROD-03 | (deferred by EQ-0019) | Not authorized |
| SEM-PROD-08 | (deferred by EQ-0019) | Not authorized |
| SEM-PROD-10 | (deferred by EQ-0019) | Not authorized |
| SEM-PROD-11 | (deferred by EQ-0019) | Not authorized |

## Architecture Constraints

- **ADR-0017:** Platform Kernel never creates Context, Plans, or executes Skills
- **ADR-0021:** Control Plane and Data Plane Separation — semantic intelligence is Data Plane evidence
- **ADR-0025:** Observation Runtime Architecture (rejected) — production stays with deterministic extraction
- **EQ-0011:** Evidence/Assessment boundary — all Increment 4 capabilities produce evidence only

## Applicable Contracts

- [BOQ Intelligence Public Evidence Contract v1.1.0](../../contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.1.md) — Frozen

## Verification Documents

This README serves as the canonical entry point for IP-0001 verification.

| Document | Purpose |
|----------|---------|
| `Verification_Report.md` | Phase 1: Acceptance criteria verification |
| `Architecture_Audit.md` | Phase 2: Architecture compliance audit |
| `Contract_Verification.md` | Phase 3: Public Evidence Contract verification |
| `Regression_Report.md` | Phase 4: Regression test results |
| `Freeze_Recommendation.md` | Phase 7: Freeze recommendation (incorporates Phases 5-6) |

## Production Code

- `src/jarvis/parsers/costx/boq_intelligence.py` (extended)
- 9 new fields on `BOQIntelligenceResult`
- `include_semantic` parameter on `analyze_boq()`
- 8 new internal pure functions

## Tests

- `tests/parser/test_boq_intelligence.py` (extended)
- 53 new test cases across 11 test classes
- Full test suite: 372 passed, 8 skipped (pre-existing historical), 0 failures

## Document Control

| Field | Value |
|-------|-------|
| IP Number | IP-0001 |
| Title | BOQ Intelligence Increment 4 — Semantic Intelligence Implementation |
| Source EQ | EQ-0019 (PERMANENTLY FROZEN) |
| Status | PERMANENTLY FROZEN |
| Created | 2026-07-25 |
| Frozen | 2026-07-25 |
| Owner | Project Owner |
| Repository Version | v0.0.1-alpha.13 |
