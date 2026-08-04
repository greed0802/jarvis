# Capability Dependency Graph

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Owner** | Project Owner |
| **Effective** | 2026-07-22 |
| **Supersedes** | None |
| **Sprint Reference** | CB-0001 |

---

## Purpose

This document visualizes the dependency relationships between all Jarvis capabilities — both delivered and deferred.

It exists to:

- Prevent circular dependencies during planning
- Clarify what must exist before a deferred capability can begin
- Help prioritize next capabilities after the current Active capability matures

This graph is derived from the Capability Register but is conceptually separate. It is a dependency map, not a lifecycle state tracker.

---

## Legend

```
[A] ────▶ [B]           A depends on B (B must exist first)
[A] ──base──▶ [B]       A uses B as its baseline
[A] ──consumer──▶ [B]   A consumes B's evidence contract
```

---

## Complete Dependency Graph

```
                    ┌──────────────────────┐
                    │  BOQ Intelligence     │
                    │  (Active / Strategic) │
                    └──────┬───────────────┘
                           │
               ┌───────────┼───────────┐
               │           │           │
       consumer│    base   │  prereq   │    foundation
               ▼           ▼           ▼
    ┌──────────────┐ ┌───────────┐ ┌──────────────┐
    │  Validation  │ │ CheckMate │ │  Formatter   │
    │   Engine     │ │ (Deferred)│ │  (Deferred)  │
    │   (Frozen)   │ └───────────┘ └──────────────┘
    └──────────────┘                     │
                                         │ prereq (trusted output)
                                         ▼
                                  ┌ ─ ─ ─ ─ ─ ─ ─
                                  │ Validation    │
                                  │  Reports/API   │
                                  │ (not scoped)  │
                                  └ ─ ─ ─ ─ ─ ─ ─


┌───────────────┐         ┌──────────────────────┐
│ Cubit Parser   │─────────▶   BOQ Intelligence   │
│  (Deferred)   │  needs   │   (cross-source)    │
└───────────────┘         └──────────────────────┘


┌───────────────┐         ┌──────────────────────┐
│  PDF Parser   │─────────▶   BOQ Intelligence   │
│  (Deferred)   │  needs   (cross-source)        │
└───────────────┘         └──────────────────────┘


┌─────────────────────────┐
│ AI-Assisted Estimation  │
│       (Deferred)        │
└─────┬─────────────┬─────┘
      │             │
      │             └──────────────▶ BOQ Intelligence (foundation)
      │
      └──────────────▶ Context Engine    (not built)
                      ├───▶ Knowledge Framework (not built)
                      └───▶ Training Data        (not collected)


┌──────────────────────┐
│ Observation Runtime  │
│   M6 (Historical)    │─── ADR-0025 rejected this as production architecture
└──────────────────────┘
```

---

## Dependency Table

| Upstream Capability | Relationship | Downstream Capability | Status |
|---------------------|:------------:|------------------------|:------:|
| BOQ Intelligence | ← consumer _←_ | Validation Engine | Active consumer |
| BOQ Intelligence | ← baseline ← | CheckMate | Blocked (BOQ requires more maturity) |
| BOQ Intelligence | ← prereq ← | Formatter | Blocked (pending trusted validation) |
| BOQ Intelligence | ← foundation ← | AI-Assisted Estimation | Long-term blocked |
| Cubit Parser | ← needs evidence → | BOQ Intelligence (cross-source) | Blocked (no fixtures) |
| PDF Parser | ← needs evidence → | BOQ Intelligence (cross-source) | Blocked (no fixtures) |
| BOQ Intelligence | ← foundation ← | AI-Assisted Estimation | Long-term blocked |
| Context Engine | ← dependency ← | AI-Assisted Estimation | Not built |
| Knowledge Framework | ← dependency ← | AI-Assisted Estimation | Built, no production evidence |

---

## Blocked-By Summary

| Deferred Capability | Blocked By |
|----------------------|------------|
| **CheckMate** | BOQ Intelligence (needs mature validation baseline); Domain rule catalog (not yet formally cataloged) |
| **Formatter** | BOQ Intelligence (needs trusted validation output before export) |
| **Cubit Parser** | Cubit export fixtures from Project Owner; Engineering Question |
| **PDF Parser** | PDF fixtures; fundamentally different extraction problem |
| **AI-Assisted Estimation** | BOQ Intelligence, Context Engine production evidence, training data |
| **Observation Runtime** | Blocked permanently — rejected by ADR-0025; Historical artifact |

---

## Graph Invariants

These are true regardless of how capabilities evolve:

1. No capability may depend on anything that does not have a Frozen Public Contract.
2. The Capability Register is the authoritative lifecycle source; this graph is a dependency projection.
3. A new capability may not introduce circular dependencies.
4. The dependency graph expands with each capability's integration surface.

---

## Future Extension Plan

- When a capability reaches **Frozen Sub-capability**, its box in the graph turns solid.
- When a new capability is approved, its box is added in outline.
- When a new Engineering Question introduces cross-cutting evidence, a new arrow appears.

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Created. Records dependency graph for all 8 capabilities (7 active/deferred + 1 Historical). Sprint CB-0001. |