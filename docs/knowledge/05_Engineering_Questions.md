# 05 — Engineering Questions

> **Purpose**: Executive summaries of all 4 completed Engineering Questions with compressed spike evidence. Replaces reading 24 individual EQ and spike documents.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- One-page executive summary per Engineering Question
- Compressed spike summaries (minimal format)
- Capability matrix summaries
- Key decisions, frozen outputs, and consumer impact

For raw evidence, refer to original EQ files and spike reports. This is the compressed engineering summary.

---

## EQ-0010: Deterministic BOQ Structural Intelligence

| Field | Value |
|-------|-------|
| **Status** | **FROZEN — Gate 3 Approved** |
| **EQ File** | `docs/engineering/questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md` (541 lines) |
| **Spikes** | 5 |
| **Duration** | ~2 weeks |
| **Dependencies** | EQ-0007 (production extraction), BOQ Intelligence Increment 1 |
| **Architecture Impact** | None (pure functions over `list[BOQRow]`) |

### Engineering Question
What deterministic structural intelligence can be extracted from the production BOQRow data structure alone — hierarchy depth, parent-child relationships, orphan detection, section integrity?

### First Principle
Investigate what is **deterministically computable** from BOQRow fields without AI, NLP, heuristics, or domain inference.

### Spikes

| # | Spike | Key Discovery | Status |
|---|-------|---------------|--------|
| 1 | Direct Field Observation | 9 fields directly observable per BOQRow. All fields present in production data. | Complete |
| 2 | UOM Pattern Analysis | 38 unique UOMs identified. Patterns: linear (m), area (m2), volume (m3), count (nr), weight (kg, t). Common UOMs confirmed. | Complete |
| 3 | Row Sequence Analysis | Row types transition predictably: HEADER→ITEM→ITEM→SUBTOTAL→BLANK. Section context derivable from preceding headers. | Complete |
| 4 | Hierarchy Reconstruction | Parent-child relationships derivable from section headers + row sequence. 4-level depth max. Orphan rows detectable (ITEM rows with no preceding section header). | Complete |
| 5 | Domain Reconciliation | Reconciled spike findings with domain docs. Confirmed 02_BOQ_Structure.md accuracy. Identified gaps in domain knowledge for trade classification. | Complete |

### Capability Matrix
- **18 structural capabilities** classified
- **8 Observable** (row type, row number, code presence, description presence, quantity value, UOM value, rate presence, amount presence)
- **10 Derivable** (row type transitions, section depth, parent-child relationships, orphan detection, section integrity, blank row patterns, subtotal detection, hierarchy depth, section context, row classification)
- **4 Domain Dependent** (trade from code, item categorization, measurement validation, rate reasonability)
- **4 Not Determinable** (semantic meaning, design compliance, cost accuracy, scope completeness)

### Key Decisions
- Single-fixture investigation (`full_boq.xlsx`) sufficient
- Deterministic analysis only — no AI/NLP/heuristics
- All capabilities start in "Unknown" state, classified by evidence
- Architecture impact: None — all capabilities are pure functions
- 18 structural capabilities provide foundational evidence for BOQ Intelligence

### Frozen Outputs
- `docs/engineering/capability_matrices/EQ_0010_Structural_Capability_Matrix.md` (Frozen)
- 5 spike evidence reports (preserved as evidence)
- EQ-0010 Gate 3 approval

---

## EQ-0011: BOQ Semantic Intelligence Boundary

| Field | Value |
|-------|-------|
| **Status** | **FROZEN — Gate 3 Approved** |
| **EQ File** | `docs/engineering/questions/EQ_0011_BOQ_Semantic_Intelligence_Boundary.md` (~400 lines) |
| **Spikes** | 5 |
| **Dependencies** | EQ-0010 (structural intelligence), Domain Knowledge Layer |
| **Architecture Impact** | Established Evidence/Assessment boundary (ADR-0025) |

### Engineering Question
Where is the boundary between what Jarvis can deterministically extract (evidence) and what requires human domain judgment (assessment)?

### First Principle
Jarvis provides evidence; humans make assessments. The engineering boundary must be explicit and never crossed.

### Spikes

| # | Spike | Key Discovery |
|---|-------|---------------|
| 1 | Domain Vocabulary Discovery | Extracted vocabulary from domain docs + production data. Confirmed glossary terms. Identified terms spanning evidence/assessment boundary. |
| 2 | Evidence vs Assessment Decomposition | Decomposed BOQ intelligence into evidence (machine-extractable) and assessment (human judgment). Trade classification = assessment. Quantity/UOM/sign = evidence. |
| 3 | Boundary Validation | Validated boundary against production data. Confirmed that evidence fields are consistently extractable; assessment fields vary by domain context. |
| 4 | Engineering Boundary Synthesis | Synthesized final boundary definition. Established rule: Jarvis never classifies trades, categorizes items, or evaluates "reasonableness". |
| 5 | Semantic Capability Disposition | Classified 17 semantic capabilities as Evidence (7), Assessment (7), or Boundary-Dependent (3). Froze disposition. |

### Capability Matrix
- **17 semantic capabilities** classified
- **7 Evidence** (sign detection, quantity validation, UOM standardization, code format validation, description completeness, row sequence validation, section labeling)
- **7 Assessment** (trade classification, item categorization, measurement compliance, rate benchmarking, scope gap analysis, design compliance, cost reasonability)
- **3 Boundary-Dependent** (description parsing, naming convention enforcement, client convention compliance)

### Key Decisions
- Evidence/Assessment boundary is ENGINEERING LAW (frozen by ADR-0025)
- Jarvis NEVER crosses into assessment territory
- M6 Observation Model REJECTED — replaced by Evidence/Assessment decomposition
- Semantic capabilities that require domain judgment are deferred until domain docs are verified

### Frozen Outputs
- `docs/engineering/capability_matrices/EQ_0011_Semantic_Capability_Matrix.md` (Frozen)
- ADR-0025 (Observation vs Assessment) — Accepted
- Evidence/Assessment boundary definition (frozen)

---

## EQ-0012: BOQ Intelligence Public Evidence Contract

| Field | Value |
|-------|-------|
| **Status** | **FROZEN — Gate 3 Approved** |
| **EQ File** | `docs/engineering/questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md` (~400 lines) |
| **Spikes** | 6 |
| **Dependencies** | EQ-0010, EQ-0011, EQ-0007 |
| **Architecture Impact** | Established contract engineering pattern (ADR-0023). First public contract. |

### Engineering Question
What public evidence contract should BOQ Intelligence expose to consumers, ensuring consumer independence while preserving evidence traceability?

### First Principle
Consumers depend on public contracts, not internal implementation. Contracts are evidence-backed, versioned, with explicit consumer guarantees.

### Spikes

| # | Spike | Key Discovery |
|---|-------|---------------|
| 1 | Current Evidence Inventory | 10 evidence fields identified (4 required + 6 optional). All traceable to frozen EQ evidence. All classified as Stable. |
| 2 | Contract Versioning Policy | Semantic Versioning (MAJOR.MINOR.PATCH). 16 permanent consumer guarantees. Three-phase deprecation lifecycle. |
| 3 | Contract Invariants | 8 structural invariants, 4 type invariants, 3 semantic invariants, 4 determinism invariants. All verified against production data. |
| 4 | Consumer Access Patterns | 3 consumer types identified (Direct API, Plugin, Export). Access patterns documented. Immutable return values (tuples, frozen dataclasses). |
| 5 | Contract Documentation Standards | Documentation template established. Every contract must document: purpose, version, authority, public API, invariants, consumer guarantees, verification method. |
| 6 | Contract Verification | Full verification audit executed. All invariants pass against production data. Contract v1.0 Frozen. |

### Contract v1.0 Summary

| Aspect | Detail |
|--------|--------|
| **Version** | 1.0.0 |
| **Required Fields** | 4 (row_type, quantity, uom, section_context) |
| **Optional Fields** | 6 (code, description, rate, amount, row_number, sign) |
| **Consumer Guarantees** | 16 permanent (Structural x4, Type x4, Semantic x3, Determinism x4, Access x1) |
| **Invariants** | 19 total (verified against production data) |
| **Versioning** | Semantic (MAJOR.MINOR.PATCH) |
| **Verification** | Spike 6 audit — all invariants pass |

### Key Decisions
- Contract-first engineering pattern established
- Semantic Versioning for all public contracts
- Consumer Independence: consumers never import internal modules
- Contract is FROZEN — breaking changes require MAJOR version + new EQ
- Deprecation: 3-phase lifecycle (Deprecated → Sunset → Removed)

### Frozen Outputs
- `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` (Frozen)
- Contract versioning policy (Semantic Versioning)
- Consumer guarantee set (16 permanent)
- EQ-0012 retrospective

---

## EQ-0013: Validation Engine

| Field | Value |
|-------|-------|
| **Status** | **FROZEN — Gate 3 Approved** |
| **EQ File** | `docs/engineering/questions/EQ_0013_Validation_Engine.md` (442 lines) |
| **Spikes** | 4 |
| **Dependencies** | EQ-0012 (contract pattern), ADR-0022 |
| **Architecture Impact** | Validation Engine implemented (`src/jarvis/engines/validation/engine.py`). Second public contract. |

### Engineering Question
How should the Validation Engine be architected as reusable deterministic infrastructure that evaluates outputs against rules without modifying inputs?

### First Principle
Validation Engine is reusable deterministic infrastructure. Findings never modify inputs. Engine is capability-agnostic. Consumer compliance is contract-guaranteed.

### Spikes

| # | Spike | Key Discovery |
|---|-------|---------------|
| 1 | Validation Capability Discovery | 58 candidate validation rules identified across 7 categories (structural, type, semantic, completeness, consistency, domain, custom). Rule registry format designed. |
| 2 | Validation Rule Taxonomy | Rules classified into 4 tiers: Architectural (always enforced), Domain (when domain docs verified), Consumer (capability-specific), Custom (user-defined). 7 severity levels. |
| 3 | Engine Scope & Responsibilities | Engine scope: evaluate findings, never modify. Architecture consistency audit passed (Kernel separation, Consumer Independence, Evidence Contract alignment). |
| 4 | Engine Implementation | Smoke test passed. Verification audit passed. ValidationFindings contract v1.0 frozen. Engine code: ~200 lines, deterministic, stateless. |

### Validation Engine Architecture

| Aspect | Detail |
|--------|--------|
| **Input** | `list[BOQRow]` + `RuleRegistry` |
| **Output** | `list[ValidationFinding]` (immutable) |
| **Finding Fields** | rule_id, severity, category, row_reference, field_reference, message, context |
| **Severity Levels** | FATAL, ERROR, WARNING, INFO, DEBUG, SUGGESTION, CUSTOM |
| **Side Effects** | NONE — pure evaluation |
| **State** | Stateless — identical inputs = identical outputs |
| **Location** | `src/jarvis/engines/validation/engine.py` |

### Key Decisions
- Option A (reusable deterministic engine) selected over Option B (per-capability) and Option C (deferred)
- Validation Engine is platform infrastructure, not a BOQ-specific capability
- Consumer Independence: consumers depend on ValidationFindings contract, not engine internals
- Boundary Preservation: Validation Engine evaluates evidence, never makes assessments
- Architecture consistency audit passed (all 5 principles)

### Frozen Outputs
- `docs/contracts/Validation_Findings_Contract_v1.0.md` (Frozen)
- `src/jarvis/engines/validation/engine.py` (Implemented)
- `data/reports/eq0013_spike1_validation_rule_registry.json` (58 rules)
- EQ-0013 Final Freeze Report

---

## Capability Matrix Summary

### EQ-0010 Structural Matrix (18 capabilities)

| Classification | Count | Examples |
|---------------|-------|----------|
| Observable | 8 | Row type, row number, code presence, quantity, UOM |
| Derivable | 10 | Hierarchy depth, parent-child, orphan detection, section integrity |
| Domain Dependent | 4 | Trade from code, item categorization |
| Not Determinable | 4 | Semantic meaning, design compliance |

### EQ-0011 Semantic Matrix (17 capabilities)

| Classification | Count | Examples |
|---------------|-------|----------|
| Evidence | 7 | Sign detection, quantity validation, UOM standardization |
| Assessment | 7 | Trade classification, rate benchmarking, scope gap analysis |
| Boundary-Dependent | 3 | Description parsing, naming convention enforcement |

---

## Cross-EQ Dependencies

```
EQ-0007 (Production Extraction)
    ↓
EQ-0010 (Structural Intelligence) → EQ-0011 (Semantic Boundary)
    ↓                                    ↓
    └────────── EQ-0012 (Evidence Contract) ←──────┘
                    ↓
              EQ-0013 (Validation Engine)
```

---

## Consumer Impact Summary

| Contract | Consumers | Status |
|----------|-----------|--------|
| BOQ Intelligence Evidence v1.0 | CheckMate (planned), future plugins | Frozen |
| Validation Findings v1.0 | All capabilities, consumer plugins | Frozen |
| Structural Capability Matrix | BOQ Intelligence consumers | Frozen |
| Semantic Capability Matrix | BOQ Intelligence consumers | Frozen |

---

## Future Engineering Questions (Deferred)

From `docs/reference/Engineering_Questions.md`:
- EQ-0001 through EQ-0009: Earlier EQs (some completed, some deferred)
- EQ-0008, EQ-0009: Deferred — see `11_Open_Questions.md`

---

## References

- `docs/engineering/questions/EQ_0010_*.md` — Full EQ documents
- `docs/engineering/questions/EQ_0011_*.md`
- `docs/engineering/questions/EQ_0012_*.md`
- `docs/engineering/questions/EQ_0013_*.md`
- `docs/engineering/evidence/` — All 20 spike reports + final freeze reports
- `docs/engineering/capability_matrices/` — Both capability matrices
- `docs/contracts/` — Both public contracts
- `docs/retrospectives/EQ_0012_*.md` — EQ-0012 retrospective
- `docs/knowledge/Appendices/B_ADR_Registry.md` — Related ADRs

---

## Verification Status

| Item | Status |
|------|--------|
| All 4 EQs | **Evidence-Backed** (Frozen, Gate 3) |
| All 20 spike reports | **Evidence-Backed** (tool output + verification audit) |
| Both capability matrices | **Evidence-Backed** (traceable to spike evidence) |
| Both contracts | **Evidence-Backed** (Frozen) |
| EQ-0013 Implementation | **Implementation-Backed** (code exists) |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation