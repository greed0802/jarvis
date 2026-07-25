# Domain Rule Catalog

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Owner** | Project Owner (Engineering rules), QS Authority (Domain rules) |
| **Effective** | 2026-07-22 |
| **Supersedes** | None |
| **Sprint Reference** | CB-0002 |

---

## Purpose

This document catalogs all BOQ domain rules — both Engineering-derived and Domain-derived — in a single authoritative inventory.

Every rule listed here traces to existing evidence. No rules are invented. No speculative rules.

---

## Rule Inventory

### Engineering-Derived Rules (E-001 through E-018)

These rules are traced to answered Engineering Questions or spike evidence. They are stable until new evidence contradicts them.

| ID | Name | Category | Severity | Status | EQ Reference | Consumer |
|----|------|----------|:--------:|:------:|:------------:|:--------:|
| E-001 | Required Evidence Fields Present | Evidence Integrity | ERROR | VERIFIED | EQ-0012 | Validation Engine |
| E-002 | Row Classification Keys Complete | Classification | ERROR | VERIFIED | EQ-0001 | Validation Engine |
| E-003 | Row Classification Non-Negative | Classification | ERROR | VERIFIED | EQ-0012 | Validation Engine |
| E-004 | Row Classification Sum Consistency | Classification | ERROR | VERIFIED | EQ-0012 | Validation Engine |
| E-005 | OMISSION Section Sign Convention | Sign Convention | WARNING | VERIFIED | EQ-0002 | Validation Engine, CheckMate |
| E-006 | Section Quantity Counts Non-Negative | Sign Convention | ERROR | VERIFIED | EQ-0012 | Validation Engine |
| E-007 | Hierarchy Availability | Structural | INFO | VERIFIED | EQ-0010 | Validation Engine, CheckMate |
| E-008 | Level Skip Detection | Structural | INFO | VERIFIED | EQ-0010, EQ-0011 | Validation Engine |
| E-009 | Structural Containment Verification | Structural | ERROR | VERIFIED | EQ-0010, EQ-0011, EQ-0015 | Validation Engine |
| E-010 | Code Completeness Ratio | Completeness | INFO | VERIFIED | EQ-0012 | Validation Engine |
| E-011 | Description Completeness Ratio | Completeness | INFO | VERIFIED | EQ-0012 | Validation Engine |
| E-012 | Quantity Completeness Ratio | Completeness | INFO | VERIFIED | EQ-0012 | Validation Engine |
| E-013 | Zero Quantity Detection | Completeness | INFO | VERIFIED | EQ-0010, EQ-0011 | Validation Engine |
| E-014 | Empty Section Detection | Completeness | INFO | VERIFIED | EQ-0010, EQ-0011 | Validation Engine |
| E-015 | Anomaly Row Range | Anomaly Detection | ERROR | VERIFIED | EQ-0012 | Validation Engine |
| E-016 | Root Header Count | Structural | INFO | VERIFIED | EQ-0010 | Validation Engine |
| E-017 | Hierarchy Depth Distribution | Structural | INFO | VERIFIED | EQ-0010 | Validation Engine |
| E-018 | Level Skip Magnitude | Structural | INFO | VERIFIED | EQ-0010, EQ-0011 | Validation Engine |

**Total Engineering Rules:** 18

**Evidence provenance:** Every engineering rule traces to at least one answered EQ. See `src/jarvis/domain/registry.py` for full traceability.

---

### Domain-Derived Rules (D-001 through D-004)

These rules are sourced from office standards, professional conventions, or QS authority. They require Project Owner or QS authority to change.

| ID | Name | Category | Severity | Status | Authority Reference | Consumer |
|----|------|----------|:--------:|:------:|:------------------:|:--------:|
| D-001 | Duplicate Item Code Detection | Domain Quality | WARNING | APPROVED | `docs/domain/Duplicate_Code_Policy.md` | CheckMate |
| D-002 | Missing Description Detection | Domain Quality | WARNING | APPROVED | `docs/domain/Missing_Description_Policy.md` | CheckMate |
| D-003 | Missing UOM Detection | Domain Quality | WARNING | APPROVED | `docs/domain/Missing_UOM_Policy.md` | CheckMate |
| D-004 | Trade Classification | Trade | INFO | APPROVED | `docs/domain/Trade_Taxonomy.md` | CheckMate, Formatter |

**Total Domain Rules:** 4 (all insufficient evidence)

---

## Authority

| Classification | Authority | Change Mechanism |
|----------------|-----------|-----------------|
| **Engineering Rule** | Engineering Question evidence, spike reports | Changed through Engineering Question process |
| **Domain Rule** | Office standards, QS convention, Project Owner | Changed when office standard changes or QS authority modifies rule |

---

## Evidence Provenance

### Engineering Rules

| EQ | Rules Traced | Key Finding |
|----|:------------:|-------------|
| **EQ-0001** | E-002 | UOM-based row classification is deterministic |
| **EQ-0002** | E-005 | Sign convention validation mechanism proven |
| **EQ-0010** | E-007, E-008, E-009, E-013, E-014, E-016, E-017, E-018 | Hierarchy reconstruction using stack algorithm, structural detection |
| **EQ-0011** | E-008, E-009, E-013, E-014, E-018 | Observe/Detect/Assess/Recommend boundary |
| **EQ-0012** | E-001, E-003, E-004, E-006, E-010, E-011, E-012, E-015 | Public Evidence Contract v1.0 invariants |
| **EQ-0015** | E-009 | Structural Containment Investigation (docstring inconsistency identified) |

### Domain Rules

All domain rules are classified as APPROVED per the documented policy documents:
- D-001: `docs/domain/Duplicate_Code_Policy.md` v1.0 — **IMPLEMENTED in CB-0004**
- D-002: `docs/domain/Missing_Description_Policy.md` v1.0 — **IMPLEMENTED in CB-0004**
- D-003: `docs/domain/Missing_UOM_Policy.md` v1.0 — **IMPLEMENTED in CB-0004**
- D-004: `docs/domain/Trade_Taxonomy.md` v1.0 — **APPROVED, pending implementation**

Authority source for all domain rules: `docs/domain/Domain_Rule_Authority.md` v1.0.

---

## Consumer Readiness

### CheckMate Dependency Status

| CheckMate Dependency | Status |
|----------------------|:------:|
| Domain Rule Foundation (this catalog) | ✅ Complete |
| Rule data model (`DomainRule`, `RuleRegistry`) | ✅ Complete |
| Rule registry (`load_registry()`) | ✅ Complete |
| 18 engineering rules (VERIFIED) | ✅ Complete |
| 4 domain rules (APPROVED) | ✅ All have documented policy and QS authority sign-off |
| Domain rule execution engine | ✅ Complete (CB-0004) |

**CheckMate readiness: PARTIAL.** The rule foundation is in place (data model + registry + engineering rules + domain rule execution engine). CheckMate now has:
- ✅ D-001, D-002, D-003 implemented and tested
- ✅ Domain rule execution engine (`execute_domain_rules()`)
- ✅ Immutable result models (`DomainRuleFinding`, `DomainRuleExecutionResult`)
- ⚠️ D-004 pending (Trade Classification)
- ⚠️ CheckMate integration adapter not yet built

---

## Implementation Status

| ID | Status | Production Code | Regression Tests |
|----|:------:|:---------------:|:----------------:|
| E-001 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-002 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-003 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-004 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-005 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-006 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-007 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-008 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-009 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-010 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-011 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-012 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-013 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-014 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-015 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-016 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-017 | VERIFIED | registry.py | tests/domain/test_registry.py |
| E-018 | VERIFIED | registry.py | tests/domain/test_registry.py |
| D-001 | IMPLEMENTED | `src/jarvis/domain/executor.py` (detect_duplicate_item_codes) | tests/domain/test_executor.py |
| D-002 | IMPLEMENTED | `src/jarvis/domain/executor.py` (detect_missing_descriptions) | tests/domain/test_executor.py |
| D-003 | IMPLEMENTED | `src/jarvis/domain/executor.py` (detect_missing_uoms) | tests/domain/test_executor.py |
| D-004 | APPROVED | Not yet implemented | Planned for CB-0005+ |

---

## Evidence Gaps

| Rule ID | Gap | Required Action |
|---------|-----|-----------------|
| D-001 | None | Implemented in CB-0004. 10 regression tests passing. |
| D-002 | None | Implemented in CB-0004. 9 regression tests passing. |
| D-003 | None | Implemented in CB-0004. 9 regression tests passing. |
| D-004 | Classification patterns not yet analyzed | Analyze item code patterns from fixture data; implement classification logic (CB-0005+) |

---

## Future Candidates

These rules are identified in Capability Discovery 001 but have no evidence. They are listed for tracking only.

- **CSV / JSON export** (engineering) — formatting, not a rule
- **Human-readable summary report** (engineering) — formatting, not a rule
- **Section analysis** (partial) — deeper section analysis beyond current classification

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `src/jarvis/domain/models.py` | DomainRule and RuleRegistry dataclasses |
| `src/jarvis/domain/registry.py` | Deterministic rule catalog implementation |
| `src/jarvis/domain/__init__.py` | Package public API |
| `tests/domain/test_registry.py` | Registry regression tests |
| `docs/planning/BOQ_Intelligence_Readiness_Report.md` | BOQ Intelligence readiness assessment |
| `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` | Public Evidence Contract |
| `docs/domain/02_BOQ_Structure.md` | BOQ hierarchy rules and structural semantics |

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Initial rule catalog. 18 engineering rules (VERIFIED), 4 domain rules (INSUFFICIENT EVIDENCE). Sprint CB-0002. |
| 1.1 | 2026-07-22 | Domain rules reclassified: INSUFFICIENT EVIDENCE → APPROVED. Policy documents created for D-001 through D-004. Authority matrix established. Sprint CB-0003. |
| 1.2 | 2026-07-22 | D-001, D-002, D-003 implemented. Domain rule execution engine built. Result models created. 103 total regression tests passing. Sprint CB-0004. |
