# EQ-0020 Architecture Recommendation

## BOQ Intelligence Consumer Architecture

### Spike 7 — Architecture Recommendation

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020 Spike 7

---

## 1. Executive Summary

This Engineering Question investigated how production systems consume BOQ Intelligence evidence. The investigation determined the correct architecture for consuming evidence while ensuring future consumers remain independent from parser implementation, BOQ extraction, and BOQ Intelligence internals.

**Recommendation:** Adopt a star-topology consumer architecture with the Evidence Contract at the center. Consumers depend only on the frozen public evidence contract. No implementation is performed — this is an architecture investigation only.

---

## 2. Investigation Summary

### 2.1 Spikes Completed

| Spike | Title | Deliverable | Status |
|-------|-------|-------------|--------|
| 1 | Consumer Inventory | `BOQ_Consumer_Matrix.md` | ✅ Complete |
| 2 | Evidence Ownership | `BOQ_Evidence_Ownership.md` | ✅ Complete |
| 3 | Consumer Boundaries | `BOQ_Consumer_Boundaries.md` | ✅ Complete |
| 4 | Consumer Access Patterns | `BOQ_Consumer_Access_Patterns.md` | ✅ Complete |
| 5 | Dependency Analysis | `BOQ_Consumer_Dependency_Analysis.md` | ✅ Complete |
| 6 | Versioning Strategy | `BOQ_Consumer_Versioning.md` | ✅ Complete |
| 7 | Architecture Recommendation | `EQ_0020_Architecture_Recommendation.md` | ✅ Complete |

### 2.2 Key Findings

1. **All consumers identified:** 5 production consumers (Validation Engine, CheckMate, Formatter, Builder, O&A, Reporting) + 3 internal infrastructure consumers (Test Suite, Contract Verification Tools, Engineering Evidence Reports) + 3 external consumers (External CI/CD, External Reporting, Domain Knowledge Layer).

2. **Every evidence field has an owner:** BOQ Intelligence is the sole producer of all 19 evidence fields + BOQHeaderNode (9 fields). Consumers own interpretation exclusively. No shared ownership of production logic.

3. **Consumer boundaries documented:** Interpretation, presentation, recommendations, and assessment all belong to consumers (or humans via consumers). Validation belongs to the Validation Engine. Evidence production belongs to BOQ Intelligence.

4. **Dependency direction established:** Dependencies flow downward. Consumers depend on Evidence Contract and Validation Findings Contract. No consumer depends on parser, extraction, or BOQ Intelligence internals.

5. **Versioning strategy documented:** SemVer with MAJOR/MINOR/PATCH policy. Optional field pattern for backward compatibility. Three-phase deprecation lifecycle.

6. **Consumer architecture independent of implementation:** Direct immutable dataclass access pattern. No facades, protocols, or abstractions. Consumers import only from stable contract paths.

7. **Future Implementation Packages clearly defined:** IP-0002 (Consumer Contract), IP-0003 (CheckMate), IP-0004 (Formatter), IP-0005 (Builder), IP-0006 (O&A), IP-0007 (Reporting).

---

## 3. Final Architecture Recommendation

### 3.1 Consumer Topology

**Star topology** with the Evidence Contract at the center:

```
                    ┌─────────────────────────────────────┐
                    │         Evidence Contract           │
                    │     BOQIntelligenceResult v1.1.0    │
                    └─────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │ Validation      │ │ CheckMate       │ │ Formatter       │
          │ Engine          │ │ (Primary        │ │ (Output         │
          │ (Findings       │ │  Consumer)      │ │  Adapter)       │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │ Validation      │ │ Builder         │ │ O&A             │
          │ Findings        │ │ (CI/CD)         │ │ (Specialized)   │
          │ Contract        │ │                 │ │                 │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────────────────────────────────────────────┐
          │                    Reporting                            │
          │                  (Summary)                              │
          └─────────────────────────────────────────────────────────┘
```

**Rationale:** Star topology ensures each consumer is independent. No consumer depends on another consumer. All consumers depend only on the Evidence Contract (and Validation Findings Contract for consumers that use the Validation Engine).

### 3.2 Ownership

| Component | Owns | Does NOT Own |
|-----------|------|--------------|
| BOQ Intelligence | Evidence production | Interpretation, presentation, validation, recommendations, assessment |
| Validation Engine | Finding production, rule evaluation | Evidence production, interpretation, presentation, recommendations, assessment |
| CheckMate | Interpretation, presentation, user workflow | Evidence production, finding production, recommendations, assessment |
| Formatter | Output rendering | Evidence production, finding production, interpretation, recommendations, assessment |
| Builder | CI/CD integration | Evidence production, finding production, interpretation, recommendations, assessment |
| O&A | O&A analysis | Evidence production, finding production, interpretation (beyond O&A), recommendations, assessment |
| Reporting | Summary reports | Evidence production, finding production, interpretation (beyond reporting), recommendations, assessment |

**Rationale:** Exclusive ownership prevents responsibility overlap. Each component has a single, well-defined role.

### 3.3 Boundaries

**EQ-0011 Engineering Boundary:**
- Engines produce evidence/findings (deterministic)
- Consumers interpret (professional judgment)
- No engine produces recommendations or assessments

**Responsibility Boundaries:**
- Evidence production → BOQ Intelligence
- Finding production → Validation Engine
- Interpretation → Consumers
- Presentation → Consumers
- Recommendations → Human (via consumers)
- Assessment → Human (via consumers)

**Rationale:** The EQ-0011 boundary is the foundational constraint. It prevents overconfident automation drift and ensures human authority over professional judgment.

### 3.4 Contracts

| Contract | Version | Status | Consumers |
|----------|---------|--------|-----------|
| BOQ Intelligence Public Evidence Contract | v1.1.0 | Frozen | All consumers |
| Validation Findings Contract | v1.0.0 | Candidate | CheckMate, Formatter, Builder, O&A, Reporting |

**Rationale:** Contracts are the sole integration surface. They provide stable, versioned APIs that decouple producers from consumers.

### 3.5 Extension Strategy

1. **New optional fields** — Added with `None` default, controlled by `include_*` parameter (MINOR version change)
2. **New contract version** — MINOR for additive changes, MAJOR for breaking changes
3. **New capabilities** — Require frozen Engineering Question disposition
4. **New consumer types** — No impact on existing consumers (star topology)

**Rationale:** The extension strategy follows the established pattern from EQ-0012 and EQ-0013. It ensures backward compatibility and consumer independence.

### 3.6 Implementation Sequence

| Priority | IP | Consumer | Rationale |
|----------|----|----------|-----------|
| P0 | IP-0002 | Consumer Contract | Foundation for all consumers |
| P1 | IP-0003 | CheckMate | Primary consumer; M8 milestone |
| P2 | IP-0004 | Formatter | Output formatting |
| P3 | IP-0005 | Builder | CI/CD integration |
| P4 | IP-0006 | O&A | Specialized analysis |
| P5 | IP-0007 | Reporting | Summary reporting |

**Rationale:** The implementation sequence follows the consumer priority from EQ-0019 Spike 5. CheckMate is the primary consumer and drives Validation Engine adoption.

---

## 4. Architecture Compliance

### 4.1 AGENTS.md Compliance

| AGENTS.md Rule | Compliance | Evidence |
|----------------|------------|----------|
| Documentation First | ✓ | All architecture documented before implementation |
| Evidence Before Promotion | ✓ | Architecture based on frozen contracts and evidence |
| ADR Driven | ✓ | ADR-0021, ADR-0013 |
| Deterministic Engineering | ✓ | Evidence is deterministic; consumers preserve determinism |
| Human Authority | ✓ | Project Owner is final authority; humans make recommendations/assessments |
| YAGNI | ✓ | No speculative abstractions |
| Small Iterations | ✓ | Consumer architecture defined incrementally per spike |
| Clarity over Cleverness | ✓ | Direct dataclass access; no runtime abstraction |
| Explicitness over Magic | ✓ | Explicit import paths; no reflection |
| Maintainability over Novelty | ✓ | Follows established patterns |

### 4.2 Architecture Rule Compliance

| Architecture Rule | Compliance | Evidence |
|-------------------|------------|----------|
| Kernel never creates Context | ✓ | Consumers are Data Plane |
| Kernel never creates Plans | ✓ | Consumers are Data Plane |
| Kernel never executes Workflows | ✓ | Consumers are Data Plane |
| Kernel never performs business logic | ✓ | Consumers are Data Plane |
| Kernel never executes Skills | ✓ | Consumers are Data Plane |
| Context Engine owns Context | ✓ | Not applicable |
| Planner Engine owns Plans | ✓ | Not applicable |
| Workflow Engine owns Workflows | ✓ | Not applicable |
| Skills perform work | ✓ | Not applicable |
| Validation evaluates outputs | ✓ | Validation Engine evaluates evidence |
| Learning promotes approved knowledge | ✓ | Not applicable |

### 4.3 Prohibited Without Approval

| Prohibition | Compliance | Evidence |
|-------------|------------|----------|
| Dependency Injection frameworks | ✓ | No DI frameworks |
| Plugin frameworks | ✓ | No plugin frameworks |
| Service Locators | ✓ | No service locators |
| Event Buses | ✓ | No event buses |
| Reflection-based discovery | ✓ | No reflection |
| Dynamic loading | ✓ | No dynamic loading |
| Generic abstractions without production use | ✓ | No Protocol/facade |
| Architecture rewrites | ✓ | No rewrites |
| Breaking behavioral changes | ✓ | Backward compatible |

---

## 5. Success Criteria Verification

| Success Criterion | Status | Evidence |
|-------------------|--------|----------|
| Every BOQ Intelligence consumer identified | ✅ | `BOQ_Consumer_Matrix.md` — 11 consumers identified |
| Every evidence field has an owner | ✅ | `BOQ_Evidence_Ownership.md` — 19 fields + 9 BOQHeaderNode fields |
| Consumer boundaries documented | ✅ | `BOQ_Consumer_Boundaries.md` — 5 boundary questions answered |
| Dependency direction established | ✅ | `BOQ_Consumer_Dependency_Analysis.md` — star topology, downward flow |
| Versioning strategy documented | ✅ | `BOQ_Consumer_Versioning.md` — SemVer, deprecation, optional fields |
| Consumer architecture independent of implementation | ✅ | `BOQ_Consumer_Access_Patterns.md` — direct dataclass access |
| Future Implementation Packages clearly defined | ✅ | `BOQ_Consumer_Architecture.md` §8 — 6 IPs defined |
| No implementation performed | ✅ | All deliverables are design documents |
| Engineering Question ready for Project Owner disposition | ✅ | This document |

---

## 6. Engineering Debt Register

| ID | Finding | Severity | Blocks Freeze | Planned Resolution | Status |
|----|---------|----------|---------------|-------------------|--------|
| ED-001 | Validation Findings Contract v1.0.0 is Candidate, not Frozen | Low | No | Awaiting EQ-0013 Gate 3 approval | Open |
| ED-002 | No production consumer (CheckMate, Formatter, etc.) implemented | Low | No | Future IPs (IP-0003–0007) | Open |
| ED-003 | Repository version consistency not verified across all locations | Low | No | Future verification | Open |

**No freeze-blocking engineering debt identified.**

---

## 7. Next Step

If approved, EQ-0020 authorizes:

**IP-0002 — BOQ Consumer Contract Implementation**

No implementation may begin until EQ-0020 is accepted and frozen.

---

## 8. Deliverables

| Document | Spike | Path |
|----------|-------|------|
| Consumer Inventory | 1 | `docs/design/BOQ_Consumer_Matrix.md` |
| Evidence Ownership | 2 | `docs/design/BOQ_Evidence_Ownership.md` |
| Consumer Boundaries | 3 | `docs/design/BOQ_Consumer_Boundaries.md` |
| Consumer Access Patterns | 4 | `docs/design/BOQ_Consumer_Access_Patterns.md` |
| Dependency Analysis | 5 | `docs/design/BOQ_Consumer_Dependency_Analysis.md` |
| Versioning Strategy | 6 | `docs/design/BOQ_Consumer_Versioning.md` |
| Architecture Overview | — | `docs/design/BOQ_Consumer_Architecture.md` |
| Architecture Recommendation | 7 | `docs/design/EQ_0020_Architecture_Recommendation.md` |

---

## 9. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-S7-ARCHITECTURE-RECOMMENDATION |
| **EQ** | EQ-0020 |
| **Spike** | 7 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | All EQ-0020 spike deliverables, BOQ_Intelligence_Public_Evidence_Contract_v1.1.md, Validation_Findings_Contract_v1.0.md, EQ-0011 (Boundary), EQ-0012 (Evidence Contract), EQ-0013 (Validation Engine), EQ-0019 (Semantic Intelligence), ADR-0021 (Control Plane/Data Plane), ADR-0013 (Workflow Ownership), Implementation_Governance.md v1.0 |

---

## 10. Disposition

**Status:** Ready for Project Owner disposition.

**Options:**

- **Approve:** EQ-0020 accepted and frozen. IP-0002 authorized.
- **Request Revisions:** Specific revisions requested. EQ-0020 remains in Draft.
- **Defer:** EQ-0020 deferred pending additional prerequisites.

---

**End of EQ-0020 Architecture Recommendation**
