# Domain Rule Authority Matrix

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Approved |
| **Owner** | Project Owner (QS Authority) |
| **Effective** | 2026-07-22 |
| **Supersedes** | None |
| **Sprint Reference** | CB-0003 |

---

## Purpose

This document records the authority, ownership, evidence, and approval status for every domain rule in the Jarvis Platform.

It is the single source of truth for rule governance.

---

## Authority Matrix

| Rule ID | Name | Owner | Authority | Evidence | Version | Approval Status | Consumer |
|---------|------|-------|-----------|----------|:-------:|:---------------:|:--------:|
| D-001 | Duplicate Item Code Detection | Project Owner (QS Authority) | `docs/domain/Duplicate_Code_Policy.md` | Policy document v1.0 | 1.0.0 | IMPLEMENTED | CheckMate |
| D-002 | Missing Description Detection | Project Owner (QS Authority) | `docs/domain/Missing_Description_Policy.md` | Policy document v1.0 | 1.0.0 | IMPLEMENTED | CheckMate |
| D-003 | Missing UOM Detection | Project Owner (QS Authority) | `docs/domain/Missing_UOM_Policy.md` | Policy document v1.0 | 1.0.0 | IMPLEMENTED | CheckMate |
| D-004 | Trade Classification | Project Owner (QS Authority) | `docs/domain/Trade_Taxonomy.md` | Taxonomy document v1.0 | 1.0.0 | APPROVED | CheckMate, Formatter |

---

## Engineering Rules (for reference)

| Rule ID | Name | Owner | Authority | Evidence | Version | Approval Status | Consumer |
|---------|------|-------|-----------|----------|:-------:|:---------------:|:--------:|
| E-001 | Required Evidence Fields Present | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-002 | Row Classification Keys Complete | Project Owner | EQ-0001 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-003 | Row Classification Non-Negative | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-004 | Row Classification Sum Consistency | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-005 | OMISSION Section Sign Convention | Project Owner | EQ-0002 | EQ-0002 — Sign Convention | 1.0.0 | VERIFIED | Validation Engine, CheckMate |
| E-006 | Section Quantity Counts Non-Negative | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-007 | Hierarchy Availability | Project Owner | EQ-0010 | Spike 4 — Hierarchy Reconstruction | 1.0.0 | VERIFIED | Validation Engine, CheckMate |
| E-008 | Level Skip Detection | Project Owner | EQ-0010, EQ-0011 | Spikes 2-4 | 1.0.0 | VERIFIED | Validation Engine |
| E-009 | Structural Containment Verification | Project Owner | EQ-0010, EQ-0011, EQ-0015 | Spikes 1-4 | 1.0.0 | VERIFIED | Validation Engine |
| E-010 | Code Completeness Ratio | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-011 | Description Completeness Ratio | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-012 | Quantity Completeness Ratio | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-013 | Zero Quantity Detection | Project Owner | EQ-0010, EQ-0011 | Spikes 1-3 | 1.0.0 | VERIFIED | Validation Engine |
| E-014 | Empty Section Detection | Project Owner | EQ-0010, EQ-0011 | Spikes 3 | 1.0.0 | VERIFIED | Validation Engine |
| E-015 | Anomaly Row Range | Project Owner | EQ-0012 | Spike 3 — Contract Invariants | 1.0.0 | VERIFIED | Validation Engine |
| E-016 | Root Header Count | Project Owner | EQ-0010 | Spike 4 — Hierarchy Reconstruction | 1.0.0 | VERIFIED | Validation Engine |
| E-017 | Hierarchy Depth Distribution | Project Owner | EQ-0010 | Spike 4 — Hierarchy Reconstruction | 1.0.0 | VERIFIED | Validation Engine |
| E-018 | Level Skip Magnitude | Project Owner | EQ-0010, EQ-0011 | Spikes 2-4 | 1.0.0 | VERIFIED | Validation Engine |

---

## Approval Lifecycle

| Status | Meaning |
|--------|---------|
| **CANDIDATE** | Rule identified but not yet evaluated |
| **APPROVED** | Rule has documented authority and is approved for implementation |
| **IMPLEMENTED** | Rule is implemented in production code |
| **VERIFIED** | Rule has been verified against production evidence |
| **FROZEN** | Rule is stable and immutable for consumers |
| **INSUFFICIENT_EVIDENCE** | Rule cannot be implemented due to insufficient evidence |
| **BOUNDARY_VIOLATION** | Rule violates the EQ-0011 Observe/Detect boundary |

---

## Change Authority

| Change Type | Required Authority |
|-------------|-------------------|
| Add new domain rule | Project Owner (QS Authority) |
| Modify domain rule logic | Project Owner (QS Authority) |
| Change rule severity | Project Owner |
| Deprecate rule | Project Owner |
| Add new engineering rule | Engineering Question process |
| Modify engineering rule | Engineering Question process |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial authority matrix. 4 domain rules APPROVED, 18 engineering rules VERIFIED. Sprint CB-0003. |
| 1.1 | 2026-07-22 | D-001, D-002, D-003 status changed: APPROVED → IMPLEMENTED. Production code in executor.py. Sprint CB-0004. |
