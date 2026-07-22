# 08 — Consumers

> **Purpose**: Summary of consumer architecture — who consumes Jarvis capabilities, how they connect, and the consumer independence pattern.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Consumer types and access patterns (from EQ-0012 Spike 4)
- Consumer Independence governance (ADR-0019)
- CheckMate architecture (first planned consumer)
- Consumer compliance requirements

---

## Consumer Independence (ADR-0019)

**Rule**: Consumers depend on public contracts, never on internal implementation.

This means:
- Consumers import contract modules (e.g., `BOQ_Intelligence_Public_Evidence_Contract_v1.0`)
- Consumers NEVER import internal implementation modules
- Capability internals can change without breaking consumers
- Contract versioning (MAJOR.MINOR.PATCH) governs consumer compatibility

---

## Consumer Types (from EQ-0012 Spike 4)

| Type | Description | Contract Dependency | Example |
|------|-------------|---------------------|---------|
| **Direct API** | Python modules that import contract and call capability functions | Imports contract module only | CheckMate, custom scripts |
| **Plugin** | Registered plugins that consume contract through plugin interface | Depends on contract + plugin SDK (future) | Third-party BOQ tools |
| **Export** | External systems consuming exported contract data | Depends on contract data format | Excel exports, database integrations |

### Access Pattern (Spike 4 Findings)
- **Immutable returns**: All contract outputs are immutable (tuples, frozen dataclasses)
- **Version locking**: Consumers lock to specific contract version
- **Graceful degradation**: Consumers handle missing optional fields
- **No side effects**: Consuming evidence does not modify platform state

---

## CheckMate — First Planned Consumer

**Source**: `docs/planning/M8_Repository_Assessment_and_Consumer_Architecture_Planning.md`

### Architecture
- Consumer application that uses BOQ Intelligence Evidence Contract v1.0
- Operates independently from Jarvis internals
- Consumes evidence, provides QS-specific assessment layer

### Consumer-Compliant Design
- Imports only `BOQ_Intelligence_Public_Evidence_Contract_v1.0`
- Never imports `src/jarvis/` internals
- Locked to contract version MAJOR.MINOR
- Handles optional fields gracefully

### Dependencies
```
BOQ Intelligence Evidence Contract v1.0
    ↓
CheckMate (consumer)
    ├── Receives: Evidence data (10 fields)
    ├── Adds: QS assessment layer (human domain judgment)
    └── Output: Assessed BOQ
```

### Status
- Planning phase (M8 assessment: GO recommendation)
- Not yet implemented
- Depends on: BOQ Intelligence Contract (frozen), Validation Findings Contract (frozen)

---

## Consumer Compliance Requirements

Every consumer must:

1. **Contract-only imports** — never import Jarvis internal modules
2. **Version locking** — specify compatible contract version range
3. **Optional field handling** — gracefully handle missing optional fields
4. **Immutable data respect** — never attempt to modify contract outputs
5. **Deprecation readiness** — handle deprecated contracts via 3-phase lifecycle

### Deprecation Lifecycle
```
Contract v1.0.0 (Active)
    ↓
Contract v1.0.0 (Deprecated) — warning issued, still functional
    ↓
Contract v1.0.0 (Sunset) — still available, migration required
    ↓
Contract v1.0.0 (Removed) — consumers must be on newer version
```

Each phase gives consumers time to migrate.

---

## Future Consumer Patterns

As platform matures:

| Future Consumer | Depends On | Status |
|-----------------|------------|--------|
| QS Assessment Dashboard | BOQ Intelligence + Validation | Not started |
| BOQ Export Tool | BOQ Intelligence + Export capability | Not started |
| Third-party QS plugins | Plugin SDK + contracts | Plugin SDK not built |
| Cost Analysis Tool | BOQ Intelligence + Cost Analysis capability | Not started |

---

## References

- `docs/planning/M8_Repository_Assessment_and_Consumer_Architecture_Planning.md` — M8 assessment (1618 lines)
- `docs/engineering/evidence/EQ_0012_Spike4_Evidence_Report_Consumer_Access_Patterns.md` — Consumer patterns
- `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` — Primary contract
- `docs/contracts/Validation_Findings_Contract_v1.0.md` — Validation contract
- ADRs: 0019 (Consumer Independence), 0023 (Evidence Contract Engineering)
- `docs/knowledge/06_Contracts.md` — Contract summaries

---

## Verification Status

| Item | Status |
|------|--------|
| Consumer Access Patterns | **Evidence-Backed** (EQ-0012 Spike 4) |
| Consumer Independence (ADR-0019) | **Project Owner Verified** (Accepted ADR) |
| M8 Assessment | **Evidence-Backed** |
| CheckMate Implementation | Not yet started (planning phase) |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation