# 06 — Contracts

> **Purpose**: Summaries of both frozen public contracts — BOQ Intelligence Evidence v1.0 and Validation Findings v1.0. Includes contract engineering pattern.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Contract engineering pattern (from EQ-0012, ADR-0023)
- BOQ Intelligence Public Evidence Contract v1.0 summary
- Validation Findings Contract v1.0 summary
- Versioning policy and consumer guarantees

For full contract text, refer to original contract documents in `docs/contracts/`.

---

## Contract Engineering Pattern

**Governed by**: ADR-0023 (Evidence Contract Engineering), EQ-0012 Spike 2 (Versioning Policy), Spike 5 (Documentation Standards)

### Every Contract Must Document
1. **Purpose** — what the contract provides
2. **Version** — MAJOR.MINOR.PATCH
3. **Authority** — which EQ/ADR authorized this contract
4. **Public API** — exact fields, types, return values
5. **Invariants** — structural, type, semantic, determinism
6. **Consumer Guarantees** — what consumers can permanently rely on
7. **Versioning Rules** — what changes require MAJOR/MINOR/PATCH
8. **Dependencies** — what evidence sources this contract depends on
9. **Verification Method** — how invariants are verified
10. **Deprecation Policy** — 3-phase: Deprecated → Sunset → Removed

### Versioning Policy (Semantic)
```
MAJOR.MINOR.PATCH
  │     │     └── Documentation fixes, clarifications (no behavioral change)
  │     └──────── New optional fields, new keys, new enum values (backward compatible)
  └────────────── Breaking changes: remove required fields, change invariants, remove types
```

### Consumer Independence Rule
Consumers import ONLY the contract module. Never import internal implementation modules.

---

## BOQ Intelligence Public Evidence Contract v1.0

**Status**: **FROZEN**
**Source**: `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md`
**Authority**: EQ-0012 (Gate 3), ADR-0026
**Version**: 1.0.0

### Purpose
Provides deterministic evidence fields extracted from BOQRow data. Consumers use this contract to access BOQ structural and semantic evidence without depending on internal BOQ Intelligence implementation.

### Public API

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `row_type` | Enum | ✅ | ITEM, SECTION_HEADER, BLANK, SUBTOTAL |
| `quantity` | float | ✅ | Numeric quantity (may be 0 for non-item rows) |
| `uom` | str | ✅ | Unit of Measure string |
| `section_context` | str | ✅ | Section/subsection the row belongs to |
| `code` | str | ❌ | Item code (may be empty) |
| `description` | str | ❌ | Item description (may be empty) |
| `rate` | float | ❌ | Unit rate (may be 0) |
| `amount` | float | ❌ | Extended amount (may be 0) |
| `row_number` | int | ❌ | Sequential row index |
| `sign` | Enum | ❌ | POSITIVE (addition), NEGATIVE (omission), ZERO |

### Invariants (19 total, all verified)

| Category | Count | Examples |
|----------|-------|----------|
| Structural | 8 | Every row has a row_type; section_context is non-empty for ITEM rows |
| Type | 4 | quantity is float; uom is non-empty string |
| Semantic | 3 | sign matches quantity direction (positive→addition, negative→omission) |
| Determinism | 4 | Identical BOQRow input produces identical evidence output |

### Consumer Guarantees (16 permanent)

| Category | Count | Examples |
|----------|-------|----------|
| Structural | 4 | Fields always present in specified order; row_type always populated |
| Type | 4 | Types never change without MAJOR version bump |
| Semantic | 3 | sign semantics preserved; uom values from production UOM set |
| Determinism | 4 | Same input → same output; no side effects; no external dependencies |
| Access | 1 | Immutable return values (tuples, frozen dataclasses) |

### Verification
Spike 6 verification audit executed. All 19 invariants pass against production data. Contract frozen.

---

## Validation Findings Contract v1.0

**Status**: **FROZEN**
**Source**: `docs/contracts/Validation_Findings_Contract_v1.0.md`
**Authority**: EQ-0013 (Gate 3), ADR-0022
**Version**: 1.0.0

### Purpose
Provides the public contract for ValidationFindings produced by the Validation Engine. Any consumer (capability, plugin, export) can depend on this contract without depending on the Validation Engine implementation.

### Public API

| Field | Type | Description |
|-------|------|-------------|
| `rule_id` | str | Rule identifier from rule registry |
| `severity` | Enum | FATAL, ERROR, WARNING, INFO, DEBUG, SUGGESTION, CUSTOM |
| `category` | Enum | STRUCTURAL, TYPE, SEMANTIC, COMPLETENESS, CONSISTENCY, DOMAIN, CUSTOM |
| `row_reference` | int | Row number the finding relates to |
| `field_reference` | str | Field name the finding relates to |
| `message` | str | Human-readable finding description |
| `context` | dict | Additional context (e.g., expected vs actual values) |

### Severity Levels (7)

| Level | Meaning |
|-------|---------|
| FATAL | Data corruption — cannot proceed |
| ERROR | Definite violation of rule |
| WARNING | Potential issue — needs review |
| INFO | Informational observation |
| DEBUG | Diagnostic detail |
| SUGGESTION | Improvement recommendation |
| CUSTOM | Consumer-defined severity |

### Rule Tiers (4)

| Tier | Scope | Enforcement |
|------|-------|-------------|
| Architectural | All capabilities always | Always enforced |
| Domain | When domain docs verified | Conditional on domain freeze |
| Consumer | Capability-specific | Defined by consumer |
| Custom | User-defined | User-configured |

---

## Contract Comparison

| Aspect | BOQ Intelligence Evidence | Validation Findings |
|--------|--------------------------|---------------------|
| **Version** | 1.0.0 | 1.0.0 |
| **Authority EQ** | EQ-0012 | EQ-0013 |
| **Fields** | 10 (4 required, 6 optional) | 7 (all required) |
| **Invariants** | 19 | (per contract doc) |
| **Consumer Guarantees** | 16 | (per contract doc) |
| **Validation Method** | Spike 6 audit | Spike 4 smoke test + audit |
| **Frozen** | ✅ | ✅ |

---

## Future Contracts

Expected as platform matures:
- Capability Registry Contract — discovery interface for available capabilities
- Skill Contract — interface for skill implementations
- Workflow Contract — task orchestration interface
- Context Contract — context assembly interface

Each must follow the contract engineering pattern (ADR-0023).

---

## References

- `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` — Full contract
- `docs/contracts/Validation_Findings_Contract_v1.0.md` — Full contract
- `docs/engineering/questions/EQ_0012_*.md` — Contract engineering EQ
- `docs/engineering/questions/EQ_0013_*.md` — Validation engine EQ
- `docs/engineering/evidence/EQ_0012_Spike1-6_*.md` — Contract evidence reports
- `docs/engineering/evidence/EQ_0013_Spike1-4_*.md` — Validation evidence reports
- ADRs: 0022, 0023, 0026

---

## Verification Status

| Item | Status |
|------|--------|
| BOQ Intelligence Contract | **Evidence-Backed**, Frozen |
| Validation Findings Contract | **Evidence-Backed**, Frozen |
| Contract Engineering Pattern | **Evidence-Backed** (EQ-0012 spikes) |
| Versioning Policy | **Evidence-Backed** (EQ-0012 Spike 2, Frozen) |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation