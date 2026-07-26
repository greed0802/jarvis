# BOQ Consumer Dependency Analysis

## EQ-0020 — BOQ Intelligence Consumer Architecture

### Spike 5 — Dependency Analysis

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020 Spike 5

---

## 1. Purpose

Determine whether consumers depend on:

- Parser
- Extraction
- BOQ Intelligence
- Evidence Contract

Identify all undesirable coupling.

---

## 2. Dependency Model

### 2.1 Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    External Systems                     │
├─────────────────────────────────────────────────────────┤
│  Tier 3: Evidence Interpreter                          │
│  CheckMate, Formatter, Builder, O&A, Reporting         │
├─────────────────────────────────────────────────────────┤
│  Tier 2: Evidence Processor                            │
│  Validation Engine                                     │
├─────────────────────────────────────────────────────────┤
│  Tier 1: Evidence Producer                             │
│  BOQ Intelligence                                      │
├─────────────────────────────────────────────────────────┤
│  Pre-Extraction Infrastructure                         │
│  WorkbookParser, BOQ Extraction                        │
├─────────────────────────────────────────────────────────┤
│  Input                                                 │
│  CostX Workbook                                        │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Dependency Direction

Dependencies flow downward (consumers depend on producers, never vice versa):

```
External Systems
  → Reporting → Evidence Contract
  → O&A → Evidence Contract
  → Builder → Evidence Contract + Validation Findings Contract
  → Formatter → Evidence Contract + Validation Findings Contract
  → CheckMate → Evidence Contract + Validation Findings Contract
  → Validation Engine → Evidence Contract
  → BOQ Intelligence → BOQRow (from Extraction)
  → BOQ Extraction → WorkbookParser
  → WorkbookParser → CostX Workbook
```

---

## 3. Consumer Dependency Matrix

### 3.1 Direct Dependencies

| Consumer | Depends on Parser? | Depends on Extraction? | Depends on BOQ Intelligence? | Depends on Evidence Contract? | Depends on Validation Findings? |
|----------|--------------------|------------------------|------------------------------|-------------------------------|---------------------------------|
| **Validation Engine** | ✗ | ✗ | ✗ | ✓ | N/A (produces) |
| **CheckMate** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Formatter** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Builder** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **O&A** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Reporting** | ✗ | ✗ | ✗ | ✓ | ✓ |
| **Test Suite** | ✗ | ✓ (fixture loading) | ✓ (determinism) | ✓ | ✓ |
| **Contract Verification Tools** | ✗ | ✓ (production comparison) | ✓ (production comparison) | ✓ | N/A |

### 3.2 Dependency Detail

#### Validation Engine

| Dependency | Import Path | Stability | Justification |
|------------|-------------|-----------|---------------|
| `BOQIntelligenceResult` | `jarvis.parsers.costx.boq_intelligence` | HIGH (frozen) | Consumes evidence; does not import internals |
| `ValidationFinding` | `jarvis.engines.validation.engine` | HIGH (frozen) | Produces findings; own type |
| `ValidationFindings` | `jarvis.engines.validation.engine` | HIGH (frozen) | Produces findings; own type |
| **Does NOT depend on** | | | |
| `WorkbookParser` | `jarvis.parsers.costx.workbook_parser` | — | Pre-extraction infrastructure; not needed |
| `BOQRow` | `jarvis.parsers.costx.boq_extraction` | — | Evidence is post-extraction; does not need raw rows |
| `analyze_boq` | `jarvis.parsers.costx.boq_intelligence` | — | Does not call analysis; consumes result |
| `_count_row_types` | `jarvis.parsers.costx.boq_intelligence._*` | — | Internal; prohibited |

#### CheckMate (Planned)

| Dependency | Import Path | Stability | Justification |
|------------|-------------|-----------|---------------|
| `BOQIntelligenceResult` | `jarvis.parsers.costx.boq_intelligence` | HIGH (frozen) | Consumes evidence |
| `ValidationFindings` | `jarvis.engines.validation.engine` | HIGH (frozen) | Consumes findings |
| `BOQHeaderNode` | `jarvis.parsers.costx.boq_intelligence` | HIGH (frozen) | Traverses hierarchy |
| **Does NOT depend on** | | | |
| `WorkbookParser` | — | — | Pre-extraction; CheckMate consumes evidence |
| `BOQRow` | — | — | Evidence is post-extraction |
| `analyze_boq` | — | — | Does not produce evidence |
| `_*` functions | — | — | Internal; prohibited |

#### Formatter (Planned)

| Dependency | Import Path | Stability | Justification |
|------------|-------------|-----------|---------------|
| `BOQIntelligenceResult` | `jarvis.parsers.costx.boq_intelligence` | HIGH (frozen) | Renders evidence |
| `ValidationFindings` | `jarvis.engines.validation.engine` | HIGH (frozen) | Renders findings |
| **Does NOT depend on** | | | |
| `WorkbookParser` | — | — | Pre-extraction |
| `BOQRow` | — | — | Evidence is post-extraction |
| `analyze_boq` | — | — | Does not produce evidence |
| `_*` functions | — | — | Internal; prohibited |

#### Builder (Planned)

| Dependency | Import Path | Stability | Justification |
|------------|-------------|-----------|---------------|
| `ValidationFindings` | `jarvis.engines.validation.engine` | HIGH (frozen) | CI/CD gates on findings |
| `BOQIntelligenceResult` | `jarvis.parsers.costx.boq_intelligence` | HIGH (frozen) | Optional: machine-readable evidence |
| **Does NOT depend on** | | | |
| `WorkbookParser` | — | — | Pre-extraction |
| `BOQRow` | — | — | Evidence is post-extraction |
| `analyze_boq` | — | — | Does not produce evidence |
| `_*` functions | — | — | Internal; prohibited |

#### O&A (Planned)

| Dependency | Import Path | Stability | Justification |
|------------|-------------|-----------|---------------|
| `BOQIntelligenceResult` | `jarvis.parsers.costx.boq_intelligence` | HIGH (frozen) | O&A analysis |
| `ValidationFindings` | `jarvis.engines.validation.engine` | HIGH (frozen) | O&A-specific checks |
| **Does NOT depend on** | | | |
| `WorkbookParser` | — | — | Pre-extraction |
| `BOQRow` | — | — | Evidence is post-extraction |
| `analyze_boq` | — | — | Does not produce evidence |
| `_*` functions | — | — | Internal; prohibited |

#### Reporting (Planned)

| Dependency | Import Path | Stability | Justification |
|------------|-------------|-----------|---------------|
| `BOQIntelligenceResult` | `jarvis.parsers.costx.boq_intelligence` | HIGH (frozen) | Aggregated statistics |
| `ValidationFindings` | `jarvis.engines.validation.engine` | HIGH (frozen) | Finding summaries |
| **Does NOT depend on** | | | |
| `WorkbookParser` | — | — | Pre-extraction |
| `BOQRow` | — | — | Evidence is post-extraction |
| `analyze_boq` | — | — | Does not produce evidence |
| `_*` functions | — | — | Internal; prohibited |

---

## 4. Undesirable Coupling Identification

### 4.1 Prohibited Dependencies

The following dependencies are **undesirable coupling** and must be prevented:

| Prohibited Dependency | Consumer | Risk | Mitigation |
|-----------------------|----------|------|------------|
| `jarvis.parsers.costx.boq_intelligence._*` | Any consumer | Internal implementation may change without notice; violates versioning policy | Consumers must import only public symbols (no `_` prefix) |
| `jarvis.parsers.costx.boq_extraction._*` | Any consumer | Internal extraction logic; not part of evidence contract | Consumers must import only `BOQRow` and `extract_boq` |
| `jarvis.parsers.costx.workbook_parser` | Any consumer | Pre-extraction infrastructure; not part of evidence contract | Consumers must not import `WorkbookParser` |
| `jarvis.parsers.costx.loader` | Any consumer | Internal loading logic; not part of evidence contract | Consumers must not import loader internals |
| Direct modification of `BOQIntelligenceResult` | Any consumer | Evidence is immutable; mutation violates determinism | `BOQIntelligenceResult` is `frozen=True`; mutation raises `FrozenInstanceError` |
| Direct modification of `ValidationFindings` | Any consumer | Findings are immutable; mutation violates determinism | `ValidationFinding` and `ValidationFindings` are `frozen=True` |

### 4.2 Coupling Risk Assessment

| Coupling Type | Risk Level | Description | Current Status |
|---------------|------------|-------------|----------------|
| Internal function import | HIGH | Consumer imports `_`-prefixed function | Prevented by contract (G-14–G-16) |
| Parser dependency | HIGH | Consumer imports `WorkbookParser` | Prevented by architecture (pre-extraction) |
| Extraction dependency | MEDIUM | Consumer imports `BOQRow` directly | Acceptable for test/verification; not for production consumers |
| Evidence mutation | HIGH | Consumer modifies `BOQIntelligenceResult` | Prevented by `frozen=True` |
| Finding mutation | HIGH | Consumer modifies `ValidationFindings` | Prevented by `frozen=True` |
| Consumer-specific logic in engine | HIGH | Engine contains CheckMate/Formatter/etc. logic | Prevented by EQ-0013 Spike 3 scope |
| Assessment in engine | HIGH | Engine produces assessments | Prevented by Validation Findings Contract (SI-FR-09) |
| Recommendation in engine | HIGH | Engine produces recommendations | Prevented by Validation Findings Contract (SI-FR-08) |

### 4.3 Coupling Prevention Mechanisms

| Mechanism | Enforced By | Scope |
|-----------|-------------|-------|
| Public symbol convention (`_` prefix) | Python convention + contract | All internal functions |
| Frozen dataclass (`frozen=True`) | Python runtime | Evidence immutability |
| Contract import paths (G-14–G-16) | Evidence Contract | Stable consumer imports |
| Architecture Consistency Gate | EQ-0013 Spike 3 | Engine/consumer boundary |
| EQ-0011 boundary verification | Validation Findings Contract | No assessment/recommendation |
| Consumer compliance verification | Validation Findings Contract §10 | Consumer behavior |

---

## 5. Dependency Evolution

### 5.1 Future Dependency Scenarios

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| New evidence field added (MINOR) | Consumers opt-in; no breaking change | Optional field pattern; None-checking |
| New consumer added | No impact on existing consumers | Star topology; independent consumers |
| New contract version (MAJOR) | Breaking change; consumers must migrate | Deprecation lifecycle; 3-phase model |
| New Validation Engine version | Consumers must update if breaking | Validation Findings Contract versioning |
| New consumer type (e.g., AI Assistant) | No impact on existing consumers | Star topology; independent consumers |

### 5.2 Dependency Stability

| Dependency | Stability | Evolution Policy |
|------------|-----------|-----------------|
| `BOQIntelligenceResult` | HIGH (frozen) | MAJOR version changes only |
| `BOQHeaderNode` | HIGH (frozen) | MAJOR version changes only |
| `ValidationFinding` | HIGH (frozen) | MAJOR version changes only |
| `ValidationFindings` | HIGH (frozen) | MAJOR version changes only |
| `analyze_boq` | HIGH (frozen) | Backward compatible parameter additions only |
| `BOQRow` | HIGH (frozen) | MAJOR version changes only |
| `extract_boq` | HIGH (frozen) | Backward compatible changes only |

---

## 6. Deliverable

This document is the **Dependency Matrix** deliverable for EQ-0020 Spike 5.

---

## 7. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-S5-DEPENDENCY-ANALYSIS |
| **EQ** | EQ-0020 |
| **Spike** | 5 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | BOQ_Intelligence_Public_Evidence_Contract_v1.1.md §Consumer Access Patterns, Validation_Findings_Contract_v1.0.md, EQ-0013 Spike 3 (Engine Scope) |

---

**End of Consumer Dependency Analysis**
