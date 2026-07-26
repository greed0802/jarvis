# BOQ Consumer Architecture

## EQ-0020 — BOQ Intelligence Consumer Architecture

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020

---

## 1. Purpose

This document defines the production architecture for consuming BOQ Intelligence evidence. It ensures future consumers remain independent from parser implementation, BOQ extraction, and BOQ Intelligence internals. Consumers depend only upon the public evidence contract.

This is an architecture investigation document. No production implementation is performed.

---

## 2. Architecture Overview

### 2.1 Consumer Topology

The consumer architecture follows a **star topology** with the Evidence Contract at the center:

```
                    ┌─────────────────────────────────────┐
                    │         Evidence Contract           │
                    │     BOQIntelligenceResult v1.1.0    │
                    │     (frozen dataclass)              │
                    └─────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │ Validation      │ │ CheckMate       │ │ Formatter       │
          │ Engine          │ │ (Primary        │ │ (Output         │
          │ (Findings       │ │  Consumer)      │ │  Adapter)       │
          │  Producer)      │ │                 │ │                 │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │ Validation      │ │ Builder         │ │ O&A             │
          │ Findings        │ │ (CI/CD)         │ │ (Specialized)   │
          │ Contract        │ │                 │ │                 │
          │ v1.0.0          │ │                 │ │                 │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────────────────────────────────────────────┐
          │                    Reporting                            │
          │                  (Summary)                              │
          └─────────────────────────────────────────────────────────┘
```

### 2.2 Architecture Layers

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

### 2.3 Data Flow

```
CostX Workbook
    ↓
[WorkbookParser validation → extract_boq()]
    ↓
BOQRow[]
    ↓
analyze_boq()  ← Evidence Producer
    ↓
BOQIntelligenceResult  ← Public Evidence Contract v1.1.0
    ↓
[Validation Engine: validate()]
    ↓
ValidationFindings  ← Validation Findings Contract v1.0.0
    ↓
[All Consumers: CheckMate, Formatter, Builder, O&A, Reporting]
```

---

## 3. Ownership Model

### 3.1 Exclusive Ownership

| Component | Owns | Does NOT Own |
|-----------|------|--------------|
| BOQ Intelligence | Evidence production | Interpretation, presentation, validation, recommendations, assessment |
| Validation Engine | Finding production, rule evaluation | Evidence production, interpretation, presentation, recommendations, assessment |
| CheckMate | Interpretation, presentation, user workflow | Evidence production, finding production, recommendations, assessment |
| Formatter | Output rendering | Evidence production, finding production, interpretation, recommendations, assessment |
| Builder | CI/CD integration | Evidence production, finding production, interpretation, recommendations, assessment |
| O&A | O&A analysis | Evidence production, finding production, interpretation (beyond O&A), recommendations, assessment |
| Reporting | Summary reports | Evidence production, finding production, interpretation (beyond reporting), recommendations, assessment |

### 3.2 Evidence Ownership

Every evidence field has a single producer (BOQ Intelligence) and multiple consumers. No shared ownership of production logic. Consumers own interpretation exclusively.

See `BOQ_Evidence_Ownership.md` for the complete evidence field ownership matrix.

---

## 4. Architectural Boundaries

### 4.1 EQ-0011 Engineering Boundary

The EQ-0011 boundary is the foundational constraint:

```
Detection              vs           Decision
   ↓                                   ↓
Evidence                          Professional
   ↓                              Interpretation
(Deterministic)                        ↓
                                   (Judgment?)
```

- **Engines produce evidence/findings** (deterministic)
- **Consumers interpret** (professional judgment)
- **No engine produces recommendations or assessments**

### 4.2 Responsibility Boundaries

| Responsibility | Owner | Contract Authority |
|----------------|-------|-------------------|
| Evidence production | BOQ Intelligence | Evidence Contract v1.1.0 |
| Finding production | Validation Engine | Validation Findings Contract v1.0.0 |
| Evidence interpretation | Consumers | Evidence Contract v1.1.0 |
| Finding interpretation | Consumers | Validation Findings Contract v1.0.0 |
| Evidence presentation | Consumers | Consumer-specific |
| Finding presentation | Consumers | Consumer-specific |
| Recommendations | Human (via consumers) | Prohibited in contracts |
| Assessment | Human (via consumers) | Prohibited in contracts |

### 4.3 No Boundary Overlap

| Component | Produces Evidence | Consumes Evidence | Produces Findings | Consumes Findings | Interprets | Presents |
|-----------|-------------------|-------------------|-------------------|-------------------|------------|----------|
| BOQ Intelligence | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Validation Engine | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| CheckMate | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |
| Formatter | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |
| Builder | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |
| O&A | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |
| Reporting | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |

See `BOQ_Consumer_Boundaries.md` for the complete boundary analysis.

---

## 5. Dependency Direction

### 5.1 Dependency Flow

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

### 5.2 Prohibited Dependencies

All consumers must NOT depend on:

| Prohibited Dependency | Risk |
|-----------------------|------|
| `jarvis.parsers.costx.boq_intelligence._*` | Internal implementation; violates versioning policy |
| `jarvis.parsers.costx.boq_extraction._*` | Internal extraction logic; not part of evidence contract |
| `jarvis.parsers.costx.workbook_parser` | Pre-extraction infrastructure; not part of evidence contract |
| `jarvis.parsers.costx.loader` | Internal loading logic; not part of evidence contract |
| Direct modification of `BOQIntelligenceResult` | Evidence is immutable; mutation violates determinism |
| Direct modification of `ValidationFindings` | Findings are immutable; mutation violates determinism |

See `BOQ_Consumer_Dependency_Analysis.md` for the complete dependency matrix.

---

## 6. Access Patterns

### 6.1 Recommended Access Pattern

**Direct immutable dataclass + public function** (current production pattern). No facade, no protocol, no contracts package, no wrapper, no adapter, no runtime abstraction.

```python
from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
from jarvis.parsers.costx.boq_intelligence import analyze_boq, BOQIntelligenceResult, BOQHeaderNode

# 1. Extract rows from a validated CostX workbook
rows: list[BOQRow] = extract_boq(workbook)

# 2. Run intelligence analysis
result: BOQIntelligenceResult = analyze_boq(
    rows,
    include_hierarchy=True,
    include_detection=True,
    include_semantic=True,
)

# 3. Access evidence directly from the frozen dataclass
for row_type, count in result.row_classification.items():
    ...

# 4. Access optional fields with defensive None-checking
if result.hierarchy is not None:
    for root in result.hierarchy:
        print(f"Root header: {root.description} (depth {root.depth})")

if result.vocabulary is not None:
    for term, count in result.vocabulary.items():
        ...
```

### 6.2 Stable Import Paths

```python
from jarvis.parsers.costx.boq_intelligence import analyze_boq
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.parsers.costx.boq_intelligence import BOQHeaderNode
from jarvis.parsers.costx.boq_extraction import BOQRow
from jarvis.parsers.costx.boq_extraction import extract_boq
```

### 6.3 Prohibited Imports

All `_`-prefixed symbols are internal implementation. Consumers must NOT import them.

See `BOQ_Consumer_Access_Patterns.md` for the complete access pattern analysis.

---

## 7. Versioning Strategy

### 7.1 Contract Versioning

- **Evidence Contract:** SemVer (MAJOR.MINOR.PATCH)
- **Validation Findings Contract:** SemVer (MAJOR.MINOR.PATCH)
- **Current Evidence Contract:** v1.1.0 (Frozen)
- **Current Validation Findings Contract:** v1.0.0 (Candidate)

### 7.2 Consumer Compatibility

- **Backward compatible within MAJOR version**
- **Optional fields return `None` when disabled**
- **Consumers check `is not None` before accessing optional fields**
- **No migration required for MINOR version changes**

### 7.3 Deprecation Policy

Three-phase model:
1. **Phase 1:** Deprecation announcement (MINOR version bump)
2. **Phase 2:** Removal notice (same MAJOR version)
3. **Phase 3:** Removal (next MAJOR version bump)

See `BOQ_Consumer_Versioning.md` for the complete versioning strategy.

---

## 8. Implementation Packages

### 8.1 Future Implementation Packages

If approved, EQ-0020 authorizes the following Implementation Packages:

| IP | Title | Authorized By | Scope |
|----|-------|---------------|-------|
| IP-0002 | BOQ Consumer Contract Implementation | EQ-0020 | Consumer contract interfaces, consumer base classes, access pattern enforcement |
| IP-0003 | CheckMate Consumer Implementation | EQ-0014 | CheckMate application (interpretation layer, presentation layer) |
| IP-0004 | Formatter Consumer Implementation | Future EQ | Formatter output adapter |
| IP-0005 | Builder Consumer Implementation | Future EQ | Builder CI/CD integration |
| IP-0006 | O&A Consumer Implementation | Future EQ | O&A specialized analysis |
| IP-0007 | Reporting Consumer Implementation | Future EQ | Reporting summary generation |

### 8.2 Implementation Sequence

| Priority | IP | Consumer | Rationale |
|----------|----|----------|-----------|
| P0 | IP-0002 | Consumer Contract | Foundation for all consumers |
| P1 | IP-0003 | CheckMate | Primary consumer; M8 milestone |
| P2 | IP-0004 | Formatter | Output formatting |
| P3 | IP-0005 | Builder | CI/CD integration |
| P4 | IP-0006 | O&A | Specialized analysis |
| P5 | IP-0007 | Reporting | Summary reporting |

---

## 9. Architecture Compliance

### 9.1 AGENTS.md Compliance

| AGENTS.md Rule | Compliance | Evidence |
|----------------|------------|----------|
| Documentation First | ✓ | All architecture documented before implementation |
| Evidence Before Promotion | ✓ | Architecture based on frozen contracts and evidence |
| ADR Driven | ✓ | ADR-0021 (Control Plane/Data Plane), ADR-0013 (Workflow Ownership) |
| Deterministic Engineering | ✓ | Evidence is deterministic; consumers preserve determinism |
| Human Authority | ✓ | Project Owner is final authority; humans make recommendations/assessments |
| YAGNI | ✓ | No speculative abstractions; no Protocol/facade without production use |
| Small Iterations | ✓ | Consumer architecture defined incrementally per spike |
| Clarity over Cleverness | ✓ | Direct dataclass access; no runtime abstraction |
| Explicitness over Magic | ✓ | Explicit import paths; no reflection or dynamic loading |
| Maintainability over Novelty | ✓ | Follows established patterns from EQ-0012/EQ-0013 |

### 9.2 Architecture Rule Compliance

| Architecture Rule | Compliance | Evidence |
|-------------------|------------|----------|
| Kernel never creates Context | ✓ | Consumers are Data Plane; Kernel not involved |
| Kernel never creates Plans | ✓ | Consumers are Data Plane; Kernel not involved |
| Kernel never executes Workflows | ✓ | Consumers are Data Plane; Kernel not involved |
| Kernel never performs business logic | ✓ | Consumers are Data Plane; Kernel not involved |
| Kernel never executes Skills | ✓ | Consumers are Data Plane; Kernel not involved |
| Context Engine owns Context | ✓ | Not applicable; consumers don't own Context |
| Planner Engine owns Plans | ✓ | Not applicable; consumers don't own Plans |
| Workflow Engine owns Workflows | ✓ | Not applicable; consumers don't own Workflows |
| Skills perform work | ✓ | Not applicable; consumers don't perform work |
| Validation evaluates outputs | ✓ | Validation Engine evaluates evidence |
| Learning promotes approved knowledge | ✓ | Not applicable; consumers don't promote knowledge |

### 9.3 Prohibited Without Approval

| Prohibition | Compliance | Evidence |
|-------------|------------|----------|
| Dependency Injection frameworks | ✓ | No DI frameworks; direct imports |
| Plugin frameworks | ✓ | No plugin frameworks |
| Service Locators | ✓ | No service locators |
| Event Buses | ✓ | No event buses |
| Reflection-based discovery | ✓ | No reflection |
| Dynamic loading | ✓ | No dynamic loading |
| Generic abstractions without production use | ✓ | No Protocol/facade; direct dataclass access |
| Architecture rewrites | ✓ | No rewrites; follows existing patterns |
| Breaking behavioral changes | ✓ | Backward compatible; MINOR version change |

---

## 10. Deliverable

This document is the **BOQ Consumer Architecture** overview, synthesizing the findings from all EQ-0020 spikes:

- Spike 1: Consumer Inventory → `BOQ_Consumer_Matrix.md`
- Spike 2: Evidence Ownership → `BOQ_Evidence_Ownership.md`
- Spike 3: Consumer Boundaries → `BOQ_Consumer_Boundaries.md`
- Spike 4: Consumer Access Patterns → `BOQ_Consumer_Access_Patterns.md`
- Spike 5: Dependency Analysis → `BOQ_Consumer_Dependency_Analysis.md`
- Spike 6: Versioning Strategy → `BOQ_Consumer_Versioning.md`
- Spike 7: Architecture Recommendation → `EQ_0020_Architecture_Recommendation.md`

---

## 11. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-ARCHITECTURE |
| **EQ** | EQ-0020 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | BOQ_Intelligence_Public_Evidence_Contract_v1.1.md, Validation_Findings_Contract_v1.0.md, EQ-0011 (Boundary), EQ-0012 (Evidence Contract), EQ-0013 (Validation Engine), EQ-0019 (Semantic Intelligence), ADR-0021 (Control Plane/Data Plane), ADR-0013 (Workflow Ownership) |

---

**End of BOQ Consumer Architecture**
