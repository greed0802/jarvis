# BOQ Consumer Matrix

## EQ-0020 — BOQ Intelligence Consumer Architecture

### Spike 1 — Consumer Inventory

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020 Spike 1

---

## 1. Purpose

Identify every current and future consumer of BOQ Intelligence evidence. Determine production consumers, planned consumers, and external consumers.

This inventory is the authoritative source for all downstream EQ-0020 spikes (ownership, boundaries, dependencies, versioning).

---

## 2. Consumer Inventory

### 2.1 Production Consumers

| Consumer | Status | Role | Evidence Contract Dependency | Validation Engine Dependency | Notes |
|----------|--------|------|------------------------------|------------------------------|-------|
| **Validation Engine** | **Production (Frozen)** | Evaluates evidence against rules; produces ValidationFindings | v1.0.0 (frozen) | N/A (consumer of evidence, not validation) | `src/jarvis/engines/validation/engine.py` — 18 rules implemented |
| **BOQ Intelligence** | **Production (Frozen)** | Evidence Producer | N/A (produces evidence) | N/A | `src/jarvis/parsers/costx/boq_intelligence.py` — source of truth |

### 2.2 Planned Consumers

| Consumer | Status | Role | Evidence Contract Dependency | Validation Engine Dependency | Notes |
|----------|--------|------|------------------------------|------------------------------|-------|
| **CheckMate** | **Planned** | BOQ validation application; primary consumer of evidence + findings | v1.1.0 (planned) | v1.0.0 (planned) | M8 milestone; consumes ValidationFindings, adds interpretation layer |
| **Formatter** | **Planned** | Output format adapter (Excel, PDF, HTML) | v1.1.0 (planned) | v1.0.0 (planned) | Renders evidence + findings into output formats |
| **Builder** | **Planned** | Build/CI integration | v1.1.0 (planned) | v1.0.0 (planned) | Machine-readable evidence for automated checks in CI pipeline |
| **O&A (Omission & Addition)** | **Planned** | Omission/addition analysis | v1.1.0 (planned) | v1.0.0 (planned) | Specialized analysis of omission/addition sections |
| **Reporting** | **Planned** | Summary reporting | v1.1.0 (planned) | v1.0.0 (planned) | Aggregated statistics for executive summaries |

### 2.3 External Consumers

| Consumer | Status | Role | Evidence Contract Dependency | Validation Engine Dependency | Notes |
|----------|--------|------|------------------------------|------------------------------|-------|
| **External CI/CD Systems** | **Future** | Automated pipeline integration | Via Builder (indirect) | Via Builder (indirect) | Consumes Builder output, not evidence directly |
| **External Reporting Tools** | **Future** | Third-party report generation | Via Reporting (indirect) | Via Reporting (indirect) | Consumes Reporting output, not evidence directly |
| **Domain Knowledge Layer** | **Future** | QS domain knowledge integration | Via evidence (indirect) | Via evidence (indirect) | Consumes evidence for domain rule application |

### 2.4 Internal Infrastructure Consumers

| Consumer | Status | Role | Evidence Contract Dependency | Notes |
|----------|--------|------|------------------------------|-------|
| **Test Suite** | **Production** | Regression and contract verification | v1.1.0 | `tests/` — verifies determinism, invariants, backward compatibility |
| **Contract Verification Tools** | **Production** | Evidence contract compliance | v1.1.0 | `tools/` — verifies implementation matches contract |
| **Engineering Evidence Reports** | **Production** | Evidence documentation | v1.1.0 | `docs/engineering/evidence/` — documents evidence for future EQs |

---

## 3. Consumer Classification

### 3.1 By Evidence Consumption Pattern

| Pattern | Consumers | Description |
|---------|-----------|-------------|
| **Direct Evidence Consumer** | Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting | Consumes `BOQIntelligenceResult` directly |
| **Findings Consumer** | CheckMate, Formatter, Builder, O&A, Reporting | Consumes `ValidationFindings` from Validation Engine |
| **Indirect Consumer** | External CI/CD, External Reporting, Domain Knowledge Layer | Consumes output of direct consumers |
| **Verification Consumer** | Test Suite, Contract Verification Tools | Verifies evidence contract compliance |

### 3.2 By Consumer Tier

| Tier | Consumers | Description |
|------|-----------|-------------|
| **Tier 1 — Evidence Producer** | BOQ Intelligence | Produces evidence; does not consume |
| **Tier 2 — Evidence Processor** | Validation Engine | Consumes evidence, produces findings |
| **Tier 3 — Evidence Interpreter** | CheckMate, Formatter, Builder, O&A, Reporting | Consumes evidence + findings, applies interpretation |
| **Tier 4 — Output Consumer** | External systems | Consumes output of Tier 3 consumers |

### 3.3 By Architecture Plane

| Plane | Consumers | Description |
|-------|-----------|-------------|
| **Data Plane** | All listed consumers | Process user work; transform evidence into value |
| **Control Plane** | Platform Kernel | Does not consume evidence directly |

---

## 4. Consumer Evidence Field Usage

### 4.1 Evidence Field → Consumer Mapping

| Evidence Field | Validation Engine | CheckMate | Formatter | Builder | O&A | Reporting |
|----------------|-------------------|-----------|-----------|---------|-----|-----------|
| `row_classification` | ✓ (V-001, V-002, V-003, V-004) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `section_statistics` | ✓ (V-001, V-005) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `boq_statistics` | ✓ (V-001, V-004, V-006, V-007, V-008, V-009) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `known_anomalies` | ✓ (V-001, V-006) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `hierarchy` | ✓ (V-010) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `hierarchy_statistics` | ✓ (V-011, V-012) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `detected_level_skips` | ✓ (V-013, V-014, V-015) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `zero_quantity_items` | ✓ (V-016) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `structural_containment_findings` | ✓ (V-017) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `completeness_findings` | ✓ (V-018) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `vocabulary` | — | ✓ | ✓ | — | — | ✓ |
| `head1_categorization` | — | ✓ | ✓ | — | — | ✓ |
| `administrative_patterns` | — | ✓ | ✓ | ✓ | — | ✓ |
| `section_enumeration` | — | ✓ | ✓ | ✓ | ✓ | ✓ |
| `uom_distribution` | — | ✓ | ✓ | ✓ | — | ✓ |
| `uom_percentages` | — | ✓ | ✓ | ✓ | — | ✓ |
| `header_distribution` | — | ✓ | ✓ | ✓ | — | ✓ |
| `header_quantity_violations` | — | ✓ | ✓ | ✓ | — | ✓ |
| `admin_template_matches` | — | ✓ | ✓ | ✓ | — | ✓ |
| `BOQHeaderNode` (fields) | — | ✓ | ✓ | ✓ | ✓ | ✓ |

### 4.2 Findings Field → Consumer Mapping

| Finding Type | Validation Engine | CheckMate | Formatter | Builder | O&A | Reporting |
|--------------|-------------------|-----------|-----------|---------|-----|-----------|
| `ValidationFindings` | Produces | Consumes | Consumes | Consumes | Consumes | Consumes |
| `ValidationFinding` | Produces | Consumes | Consumes | Consumes | Consumes | Consumes |

---

## 5. Consumer Independence Assessment

### 5.1 Current State

| Consumer | Independent of Parser? | Independent of Extraction? | Independent of BOQ Intelligence Internals? | Depends Only on Contract? |
|----------|------------------------|----------------------------|--------------------------------------------|---------------------------|
| Validation Engine | ✓ | ✓ | ✓ | ✓ |
| CheckMate (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) |
| Formatter (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) |
| Builder (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) |
| O&A (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) |
| Reporting (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) | ✓ (planned) |

### 5.2 Independence Verification

All consumers satisfy the independence requirement:

- **No consumer imports from `jarvis.parsers.costx.boq_intelligence._*`** (internal helpers)
- **No consumer imports from `jarvis.parsers.costx.boq_extraction._*`** (internal helpers)
- **No consumer imports from `jarvis.parsers.costx.workbook_parser`** (pre-extraction infrastructure)
- **All consumers import only from stable contract paths** (see BOQ_Consumer_Access_Patterns.md)

---

## 6. Consumer Readiness

### 6.1 Consumer Readiness Matrix

| Consumer | Status | Evidence Contract v1.1.0 Compatible | Validation Findings Contract v1.0.0 Compatible | Ready for Implementation |
|----------|--------|--------------------------------------|-----------------------------------------------|--------------------------|
| Validation Engine | Production (Frozen) | ✓ (uses v1.0.0, backward compatible) | ✓ (produces v1.0.0) | N/A (already implemented) |
| CheckMate | Planned | ✓ (planned) | ✓ (planned) | Pending EQ-0014 |
| Formatter | Planned | ✓ (planned) | ✓ (planned) | Pending future EQ |
| Builder | Planned | ✓ (planned) | ✓ (planned) | Pending future EQ |
| O&A | Planned | ✓ (planned) | ✓ (planned) | Pending future EQ |
| Reporting | Planned | ✓ (planned) | ✓ (planned) | Pending future EQ |

### 6.2 Consumer Implementation Sequence

| Priority | Consumer | Rationale |
|----------|----------|-----------|
| P0 | CheckMate | Primary consumer; M8 milestone; drives Validation Engine adoption |
| P1 | Formatter | Output formatting; depends on evidence structure |
| P2 | Builder | CI/CD integration; depends on CheckMate/Formatter patterns |
| P3 | O&A | Specialized analysis; depends on evidence completeness |
| P4 | Reporting | Summary reporting; depends on all upstream consumers |

---

## 7. Deliverable

This document is the **Consumer Inventory** deliverable for EQ-0020 Spike 1.

---

## 8. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-S1-CONSUMER-MATRIX |
| **EQ** | EQ-0020 |
| **Spike** | 1 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | BOQ_Intelligence_Public_Evidence_Contract_v1.1.md, EQ-0013 (Validation Engine), EQ-0019 Spike 5 (Consumer Analysis) |

---

**End of Consumer Matrix**
