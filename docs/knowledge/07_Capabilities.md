# 07 — Capabilities

> **Purpose**: Summary of all registered Jarvis capabilities — implemented, deferred, and their contracts, matrices, and dependencies.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Current capability register (7 capabilities, 2 implemented, 5 deferred)
- Capability lifecycle and governance
- Capability matrices (structural + semantic classifications)
- Dependencies between capabilities

For detailed capability matrices, see `05_Engineering_Questions.md`. For the living register, see `docs/planning/Capability_Register.md`.

---

## Capability Register (Current State)

| Capability | Status | Contract | EQ | Implemented |
|------------|--------|----------|-----|-------------|
| **BOQ Intelligence** | **Implemented** | BOQ Intelligence Evidence v1.0 | EQ-0010, EQ-0011, EQ-0012 | 2026-07-14 |
| **Validation Engine** | **Implemented** | Validation Findings v1.0 | EQ-0013 | 2026-07-15 |
| BOQ Summaries | Deferred | — | — | — |
| BOQ Export | Deferred | — | — | — |
| Anomaly Detection | Deferred | — | — | — |
| QA Workflow | Deferred | — | — | — |
| Cost Analysis | Deferred | — | — | — |

---

## Capability Lifecycle

Per `docs/planning/Capability_Roadmap.md` and `09_Methodology.md`:

```
Discovery → Evaluation → PO Decision → EQ → Spike → Implementation → Validation → Promotion → Release
```

Terminal states: Rejected, Deferred, Archived

Two readiness checkpoints:
1. **Evidence Ready**: Sufficient spike evidence exists to define a contract
2. **Implementation Ready**: Contract frozen, architecture consistent, PO authorized

Evidence readiness is a precondition, NOT authorization.

---

## Capability Relationships

```
BOQ Extraction (EQ-0007, foundation)
    ↓
BOQ Intelligence (Implemented)
    ├── Structural Intelligence (EQ-0010)
    ├── Semantic Boundary (EQ-0011)
    └── Evidence Contract (EQ-0012)
        ↓
    Validation Engine (Implemented, EQ-0013)
        ↓
    BOQ Summaries (Deferred — depends on Evidence Contract)
    BOQ Export (Deferred — depends on Evidence Contract)
    Anomaly Detection (Deferred — depends on Validation Engine)
    QA Workflow (Deferred — depends on Validation Engine)
    Cost Analysis (Deferred — depends on Evidence Contract + Domain Knowledge)
```

---

## Capability Evaluation Criteria

From `Capability_Discovery_001.md`:

| Criterion | Description |
|-----------|-------------|
| Domain Value | How valuable to the QS domain? |
| Engineering Complexity | How complex to engineer? |
| Architecture Risk | Risk of architecture violation? |
| Domain Knowledge Dependency | How much unverified domain knowledge needed? |

BOQ Intelligence scored: High Value / High Complexity / Low Risk / Low Domain Dependency → strongest first candidate.

---

## Implemented Capabilities Detail

### BOQ Intelligence
- **Owner**: Platform
- **Input**: `list[BOQRow]` (production data)
- **Output**: `list[EvidenceRow]` (per BOQ Intelligence Contract v1.0)
- **Public Contract**: 10 evidence fields (4 required, 6 optional), 19 invariants
- **Consumers**: CheckMate (planned), future plugins
- **Engineering Questions**: EQ-0010 (structural), EQ-0011 (semantic), EQ-0012 (contract)
- **Capability Matrices**: 18 structural + 17 semantic capabilities classified
- **Status**: Implemented, Contract Frozen

### Validation Engine
- **Owner**: Platform (reusable infrastructure)
- **Input**: `BOQIntelligenceResult` (Evidence Contract v1.0.0) + Rule Registry
- **Output**: `ValidationFindings` (frozen, immutable, deterministic per Validation Findings Contract v1.0.0)
- **Public Contract**: 6 finding fields per finding, no severity levels, no rule tiers
- **Consumers**: CheckMate, Formatter, Builder, O&A, Reporting
- **Engineering Questions**: EQ-0013
- **Status**: Implemented, Contract Frozen

---

## Capability Matrix Summary

### EQ-0010: 18 Structural Capabilities

| Classification | Count | Consumer Impact |
|---------------|-------|-----------------|
| Observable | 8 | Available to all consumers via evidence contract |
| Derivable | 10 | Available to consumers as derived evidence |
| Domain Dependent | 4 | Deferred until domain docs verified |
| Not Determinable | 4 | Out of scope — requires human judgment |

### EQ-0011: 17 Semantic Capabilities

| Classification | Count | Consumer Impact |
|---------------|-------|-----------------|
| Evidence | 7 | Available to consumers (structural + sign + validation) |
| Assessment | 7 | Out of scope — human domain judgment |
| Boundary-Dependent | 3 | Deferred until domain docs verified |

---

## Deferred Capabilities — Activation Requirements

| Capability | Blockers |
|------------|----------|
| BOQ Summaries | Needs: summary aggregation logic, export formatting |
| BOQ Export | Needs: export engine, format templates |
| Anomaly Detection | Needs: statistical baseline, anomaly rules |
| QA Workflow | Needs: `08_Checking_Workflow.md` verified, QA engine |
| Cost Analysis | Needs: rate database, cost benchmarking domain knowledge |

**None have started the EQ lifecycle.**

---

## References

- `docs/planning/Capability_Register.md` — Living capability register
- `docs/planning/Capability_Roadmap.md` — Capability lifecycle governance
- `docs/planning/Capability_Discovery_001.md` — First discovery
- `docs/planning/Capability_Evaluation_001.md` — BOQ Intelligence evaluation
- `docs/engineering/capability_matrices/EQ_0010_Structural_Capability_Matrix.md` — Frozen
- `docs/engineering/capability_matrices/EQ_0011_Semantic_Capability_Matrix.md` — Frozen
- `docs/knowledge/05_Engineering_Questions.md` — EQ summaries
- `docs/knowledge/06_Contracts.md` — Contract summaries

---

## Verification Status

| Item | Status |
|------|--------|
| Capability_Register.md | **Evidence-Backed** (living document) |
| Both capability matrices | **Evidence-Backed** (Frozen) |
| Capability_Roadmap.md | AI-Generated, Pending Verification |
| Capability_Discovery_001.md | **Evidence-Backed** (Complete) |
| Capability_Evaluation_001.md | **Evidence-Backed** (Complete) |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation