# Appendix B: ADR Registry

> **Purpose**: Compact summary of all 26 Architecture Decision Records governing the Jarvis platform.
> **Generated**: 2026-07-15
> **Part of**: Jarvis Knowledge Consolidation

---

## ADR Summary

All 26 ADRs are **Accepted**. None are Proposed, Deprecated, or Superseded.

| # | Title | Date | Decision Summary | Implementation Status |
|---|-------|------|------------------|----------------------|
| 0001 | Core Ontology | 2026-07-08 | Core ontology objects are the foundation of all platform concepts | **Upheld**: Domain types in `src/jarvis/domain/` match ontology |
| 0002 | Workspace vs Project | 2026-07-08 | Workspace = container; Project = domain-specific work unit | **Upheld**: Types exist in `src/jarvis/domain/` |
| 0003 | Resource Identity | 2026-07-08 | Resources identified by immutable composite key | **Upheld** (domain type exists) |
| 0004 | Resource Versioning | 2026-07-08 | Resources support content-addressable versioning | **Not yet implemented** (storage not built) |
| 0005 | Deterministic Planner | 2026-07-08 | Planner must be deterministic — same inputs = same plan | **Governance only** (Planner not built; ADR governs future design) |
| 0006 | Skill Collaboration | 2026-07-08 | Skills collaborate through Workflow, never directly | **Governance only** (no Skill/Workflow implementation yet) |
| 0007 | Knowledge Promotion | 2026-07-08 | Learning Engine promotes validated Results to Knowledge | **Not yet implemented** |
| 0008 | Context | 2026-07-08 | Context is dynamic, references-not-copies, objective-scoped lifetime | **Governance only** (Context Engine not built; reinforced by ADR-0022) |
| 0009 | Skill Architecture | 2026-07-08 | Planner decides WHAT; Workflow decides WHEN/HOW; Skills do work | **Governance only** (reinforced by ADR-0013, ADR-0024) |
| 0010 | Human Control | 2026-07-08 | Jarvis assists but never makes important autonomous decisions | **Upheld**: Foundational principle — all EQs require Gate approval |
| 0011 | Documentation Repository | 2026-07-08 | Documentation is part of repository, versioned alongside code | **Upheld**: `docs/` structure |
| 0012 | Repository Structure | 2026-07-08 | Defines repository directory layout | **Upheld**: Current structure matches |
| 0013 | Workflow Ownership | 2026-07-08 | Workflow Engine exclusively owns Workflows and Tasks | **Governance only** (architecture rule) |
| 0014 | Workflow Determinism | 2026-07-08 | Workflows must produce deterministic results | **Governance only** |
| 0015 | Result Persistence | 2026-07-08 | Results must be persisted with traceability | **Not yet implemented** |
| 0016 | Result Traceability | 2026-07-08 | Every result traces back to inputs, plan, and execution path | **Not yet implemented** |
| 0017 | Platform Kernel Philosophy | 2026-07-08 | Kernel is control plane only — never creates context, plans, or executes business logic | **Upheld**: Kernel code in `src/jarvis/core/jarvis/kernel.py` matches |
| 0018 | Platform Runtime Lifecycle | 2026-07-08 | Defines init→start→shutdown lifecycle with LifecycleAware contract | **Upheld**: LifecycleAware Protocol + Kernel implementation |
| 0019 | Consumer Independence | 2026-07-08 | Consumers depend on public contracts, not internal implementation | **Upheld**: BOQ Intelligence contract follows this pattern |
| 0020 | Engineering Question Format | 2026-07-08 | Standardized EQ format for all investigations | **Upheld**: EQ-0010 through EQ-0013 follow this format |
| 0021 | Capability Engineering Pattern | 2026-07-08 | Capabilities defined by contract first, implementation second | **Upheld**: Both implemented capabilities follow contract-first |
| 0022 | Validation Engine Architecture | 2026-07-08 | Validation Engine is reusable deterministic infrastructure; never modifies inputs | **Upheld**: `ValidationEngine` in code matches ADR |
| 0023 | Evidence Contract Engineering | 2026-07-08 | Contracts are evidence-backed, semantically versioned, with consumer guarantees | **Upheld**: Both frozen contracts follow this |
| 0024 | Workflow Execution Model | 2026-07-08 | Workflow execution orchestration model specification | **Governance only** (not yet implemented) |
| 0025 | Observation vs Assessment | 2026-07-08 | Rejected M6 Observation Model; established Evidence/Assessment decomposition | **Upheld**: EQ-0011 boundary follows this; M6 doc is obsolete |
| 0026 | BOQ Intelligence Evidence Contract | 2026-07-14 | Formalized BOQ Intelligence public evidence contract v1.0 | **Upheld**: Contract v1.0 Frozen |

---

## Implementation Status Breakdown

| Status | Count | ADRs |
|--------|-------|------|
| **Upheld in code** | 8 | 0001, 0002, 0003, 0010, 0011, 0012, 0017, 0018 |
| **Upheld by contract/process** | 5 | 0019, 0020, 0021, 0022, 0023, 0025, 0026 |
| **Governance only** (not yet implemented) | 8 | 0005, 0006, 0008, 0009, 0013, 0014, 0024 |
| **Not yet implemented** | 4 | 0004, 0007, 0015, 0016 |

---

## Key Governance Rules from ADRs

1. **ADR wins over architecture docs** per Evidence Hierarchy (ADR > Architecture Docs > Production Code)
2. **Kernel is control plane only** — never creates context, plans, or executes business logic (ADR-0017)
3. **Consumer Independence** — all capabilities expose public contracts; consumers never depend on internals (ADR-0019)
4. **Contract-first engineering** — capability contracts defined before implementation (ADR-0021, ADR-0023)
5. **Evidence/Assessment boundary** — Jarvis provides evidence; humans make assessments (ADR-0025)
6. **Deterministic engineering** — same inputs must produce same outputs (ADR-0005, ADR-0014)
7. **Human authority** — Project Owner is final authority; Jarvis never autonomously decides (ADR-0010)
8. **Exclusive ownership** — each engine owns one concern; responsibilities never overlap (ADR-0013, ADR-0022)

---

## Chronological Clusters

| Period | ADRs | Focus |
|--------|------|-------|
| 2026-07-08 | 0001–0024 | Foundation architecture — ontology, engines, lifecycle, governance |
| 2026-07-14 | 0025–0026 | Capability-era decisions — BOQ Intelligence contract, Evidence/Assessment boundary |

---

**Source Documents**: All 26 ADR files under `docs/decisions/`