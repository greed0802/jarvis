# BOQ Consumer Versioning Strategy

## EQ-0020 — BOQ Intelligence Consumer Architecture

### Spike 6 — Versioning Strategy

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020 Spike 6

---

## 1. Purpose

Investigate:

- Contract evolution
- Consumer compatibility
- Optional field handling
- Future extensions
- Deprecation policy

---

## 2. Versioning Foundation

### 2.1 Evidence Contract Versioning

The BOQ Intelligence Public Evidence Contract uses Semantic Versioning (SemVer):

| Property | Value |
|----------|-------|
| Scheme | Semantic Versioning |
| Format | MAJOR.MINOR.PATCH |
| Current Version | 1.1.0 (Frozen) |
| Previous Version | 1.0.0 (Frozen) |
| Location | `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.1.md` |

### 2.2 Validation Findings Contract Versioning

The Validation Findings Contract also uses SemVer:

| Property | Value |
|----------|-------|
| Scheme | Semantic Versioning |
| Format | MAJOR.MINOR.PATCH |
| Current Version | 1.0.0 (Candidate) |
| Location | `docs/contracts/Validation_Findings_Contract_v1.0.md` |

### 2.3 Versioning Authority

- **Evidence Contract:** EQ-0012 Spike 2 (Versioning Policy)
- **Validation Findings Contract:** EQ-0013 Spike 4 (Engine Implementation)
- **Consumer Architecture:** EQ-0020 Spike 6 (this document)

---

## 3. Contract Evolution

### 3.1 Evidence Contract Evolution Rules

#### MAJOR (X.0.0) — Breaking changes requiring consumer attention:

| Change | Rationale |
|--------|-----------|
| Removing a required field | Breaks consuming code that expects the field |
| Changing type of a required field | Breaks consuming code that depends on the type |
| Renaming a required field | Breaks consuming code that references by name |
| Adding, removing, or changing a required field | Contract shape altered; strict consumers consider required fields mandatory |
| Changing invariants consumers depend on | Changes behavior consumers may rely on |
| Removing optional field without deprecation | Violates deprecation contract |
| Removing documented dictionary keys | Breaks consumers expecting keys |
| Changing tuple element order or semantics | Breaks consumers using positional access |
| Extending tuple contents | Tuples are ordered, frozen structures; consumers may destructure or index |

#### MINOR (0.Y.0) — Non-breaking additions:

| Change | Rationale |
|--------|-----------|
| Adding new optional field | Consumer must opt-in to use |
| Adding new dict keys | Consumers iterating dynamically unaffected |
| Adding BOQHeaderNode fields (with defaults) | Backward compatible dataclass extension |
| Marking field as deprecated | Field still present and functional |

#### PATCH (0.0.Z) — Internal corrections:

| Change | Rationale |
|--------|-----------|
| Fixing documentation errors | No behavior change |
| Clarifying field semantics | No consumer impact |
| Adding invariant documentation | No consumer impact |
| Correcting type annotations | Matching actual behavior |
| Non-functional changes | No consumer impact |

### 3.2 Validation Findings Contract Evolution Rules

| Change Type | SemVer | Impact |
|-------------|--------|--------|
| Add optional finding field | MINOR | Consumers opt-in |
| Add new finding type | MINOR | Consumers opt-in |
| Remove finding field | MAJOR | Consumers must update |
| Rename finding field | MAJOR | Consumers must update |
| Change finding_value semantics | MAJOR | Consumers must update |
| Bug fix (no API change) | PATCH | Transparent |
| Documentation only | PATCH | Transparent |

### 3.3 Key Insight

**Required vs. Optional distinction is critical.** Changes to required fields are always MAJOR. Additions to optional fields can be MINOR. Removing optional fields without deprecation lifecycle is MAJOR.

---

## 4. Consumer Compatibility

### 4.1 Backward Compatibility Guarantees

The Evidence Contract v1.1.0 provides 16 consumer guarantees (G-01 through G-16):

**Structural Guarantees (G-01 to G-03):**
- G-01: All documented fields will exist for the promised contract version
- G-02: Required fields will never be None
- G-03: Optional fields will never be removed without formal deprecation

**Type Guarantees (G-04 to G-07):**
- G-04: Field types as documented will not change within a MAJOR version
- G-05: Union types will not remove valid variants
- G-06: Documented dictionary keys will remain present
- G-07: Undocumented keys may appear (non-breaking addition)

**Semantic Guarantees (G-08 to G-10):**
- G-08: Documented field semantics will not change within a MAJOR version
- G-09: Evidence classification (Observation/Hierarchy/Detection) will not change
- G-10: EQ-0011 engineering boundary preserved in all evidence

**Determinism Guarantees (G-11 to G-13):**
- G-11: All evidence is deterministic — same input produces same output
- G-12: All evidence is immutable — consumers cannot modify evidence
- G-13: All evidence is traceable to frozen engineering evidence

**Access Guarantees (G-14 to G-16):**
- G-14: Consumers may depend on the Evidence Contract directly
- G-15: Consumers may import evidence types without importing internal implementation
- G-16: Consumers will not need access to internal BOQ Intelligence functions

### 4.2 Backward Compatibility Verification

**All existing consumers are fully backward compatible with v1.1.0.**

| Consumer Action | v1.0 Behavior | v1.1.0 Behavior | Compatible? |
|-----------------|---------------|-----------------|-------------|
| `analyze_boq(rows)` | Returns result with v1.0 fields, new fields = None | Same — new fields default to None | ✓ |
| `analyze_boq(rows, include_hierarchy=True)` | Returns v1.0 + hierarchy fields | Same — new fields still None | ✓ |
| `analyze_boq(rows, include_detection=True)` | Returns v1.0 + detection fields | Same — new fields still None | ✓ |
| Access `result.row_classification` | Works | Works | ✓ |
| Access `result.hierarchy` | Works | Works | ✓ |
| Access `result.detected_level_skips` | Works | Works | ✓ |
| Access `result.vocabulary` | AttributeError (field doesn't exist) | Returns None (field exists, default None) | ✓ (improvement) |

### 4.3 Consumer Migration Path

**No migration required for existing consumers.**

Consumers that wish to use the new semantic evidence fields should:
1. Call `analyze_boq(rows, include_semantic=True)`
2. Check `result.vocabulary is not None` before accessing (defensive pattern)
3. All new fields follow the same `None`-when-disabled pattern as existing optional fields

---

## 5. Optional Field Handling

### 5.1 Optional Field Pattern

The Evidence Contract uses a consistent optional field pattern:

| Field Type | Behavior | Consumer Handling |
|------------|----------|-------------------|
| Required fields | Always present, never None | Direct access |
| Optional fields | None when disabled, populated when enabled | Check `is not None` before access |
| Optional fields (with dependencies) | None when dependency not met | Check dependency + `is not None` |

### 5.2 Optional Field Parameters

| Parameter | Default | Optional Fields Enabled |
|-----------|---------|------------------------|
| `include_hierarchy=False` | False | `hierarchy`, `hierarchy_statistics` |
| `include_detection=False` | False | `detected_level_skips`, `zero_quantity_items`, `structural_containment_findings`, `completeness_findings` |
| `include_semantic=False` | False | `vocabulary`, `head1_categorization`, `administrative_patterns`, `section_enumeration`, `uom_distribution`, `uom_percentages`, `header_distribution`, `header_quantity_violations`, `admin_template_matches` |

### 5.3 Dependency-Aware Optional Fields

Some optional fields have dependencies:

| Field | Dependency | Behavior When Dependency Missing |
|-------|------------|----------------------------------|
| `administrative_patterns` | `hierarchy` (requires `include_hierarchy=True`) | None when hierarchy not available |
| `detected_level_skips` | `hierarchy` (requires `include_detection=True` + `include_hierarchy=True`) | None when hierarchy not available |
| `zero_quantity_items` | None (standalone) | None when `include_detection=False` |
| `structural_containment_findings` | `hierarchy` (requires `include_detection=True` + `include_hierarchy=True`) | None when hierarchy not available |
| `completeness_findings` | `hierarchy` (requires `include_detection=True` + `include_hierarchy=True`) | None when hierarchy not available |

### 5.4 Consumer Defensive Pattern

```python
# Recommended consumer pattern for optional fields
result = analyze_boq(rows, include_hierarchy=True, include_detection=True, include_semantic=True)

# Required fields — direct access
row_counts = result.row_classification
boq_stats = result.boq_statistics

# Optional fields — defensive None-checking
if result.hierarchy is not None:
    process_hierarchy(result.hierarchy)

if result.detected_level_skips is not None:
    process_level_skips(result.detected_level_skips)

if result.vocabulary is not None:
    process_vocabulary(result.vocabulary)

# Dependency-aware optional fields
if result.administrative_patterns is not None:
    process_admin_patterns(result.administrative_patterns)
```

---

## 6. Future Extensions

### 6.1 Extension Strategy

Future evidence extensions follow the established pattern:

1. **New optional fields** — Added with `None` default, controlled by `include_*` parameter
2. **New contract version** — MINOR version bump for additive changes, MAJOR for breaking
3. **New capabilities** — Require frozen Engineering Question disposition
4. **New consumer types** — No impact on existing consumers (star topology)

### 6.2 Extension Constraints

| Constraint | Rationale |
|------------|-----------|
| New fields must be optional with default `None` | Backward compatibility (MINOR change) |
| New fields must be controlled by a parameter | Following the `include_*` pattern |
| New fields must preserve the EQ-0011 evidence/assessment boundary | No assessment language in evidence |
| New fields must be deterministic and immutable | Core engineering requirements |
| New fields must be traceable to frozen engineering evidence | Evidence admission rule |
| Adding required fields is a MAJOR version change | Requires new EQ disposition |
| Adding optional fields is a MINOR version change | Requires contract update |

### 6.3 Future Extension Scenarios

| Scenario | Version Change | Consumer Impact |
|----------|----------------|-----------------|
| New semantic evidence field | MINOR | Consumers opt-in; backward compatible |
| New detection evidence field | MINOR | Consumers opt-in; backward compatible |
| New required evidence field | MAJOR | Consumers must update; breaking change |
| New `include_*` parameter | MINOR | Consumers opt-in; backward compatible |
| New contract section | MINOR | Documentation only; no consumer impact |
| Contract deprecation | MINOR (announce) → MAJOR (remove) | Consumers must migrate within deprecation window |

---

## 7. Deprecation Policy

### 7.1 Three-Phase Model

```
Phase 1: Deprecation Announcement (MINOR version bump)
    ↓
Phase 2: Removal Notice (same MAJOR version)
    ↓
Phase 3: Removal (next MAJOR version bump)
```

### 7.2 Phase 1 — Deprecation Announcement

- **Trigger:** Engineering Question determines field is obsolete
- **Action:** Field marked `@deprecated` in contract documentation
- **Version:** MINOR version bump (field still present and functional)
- **Duration:** One full MAJOR version cycle minimum

### 7.3 Phase 2 — Removal Notice

- **Trigger:** Next MAJOR version planning
- **Action:** Explicit notification with target removal version
- **Version:** Still present in current MAJOR version
- **Consumer impact:** Field still present, consumers should migrate

### 7.4 Phase 3 — Removal

- **Trigger:** MAJOR version bump
- **Action:** Field removed from Evidence Contract
- **Version:** MAJOR version bump
- **Consumer impact:** Breaking change — consumers must migrate

### 7.5 Governance Gate

Before any deprecation can begin:

1. Engineering Question must classify the field as obsolete
2. Project Owner must approve deprecation
3. All consumers must be notified
4. Migration path must be documented
5. Minimum deprecation period: one full MAJOR version

### 7.6 Deprecation Example

If `known_anomalies` were deprecated in v1.2.0:

1. **v1.2.0 (Phase 1):** Field marked `@deprecated` in contract; still functional
2. **v1.x.0 (Phase 2):** Removal notice in v2.0.0 planning; consumers notified
3. **v2.0.0 (Phase 3):** Field removed; consumers must migrate to replacement

---

## 8. Version Consistency

### 8.1 Version Locations

Repository version SHALL be consistent across:

| Location | Current Value |
|----------|---------------|
| README | v0.0.1-alpha.13 |
| Version module | (to be verified) |
| Implementation Status | (to be verified) |
| Release documentation | (to be verified) |
| Contracts | Evidence Contract v1.1.0, Validation Findings Contract v1.0.0 |
| Capability Register | (to be verified) |

### 8.2 Version Synchronization

| Component | Version | Sync Status |
|-----------|---------|-------------|
| BOQ Intelligence Evidence Contract | v1.1.0 | Frozen |
| Validation Findings Contract | v1.0.0 | Candidate |
| Validation Engine | v1.0.0 | Frozen |
| Repository | v0.0.1-alpha.13 | Active |
| EQ-0020 | Draft | Active |

---

## 9. Deliverable

This document is the **Consumer Versioning Strategy** deliverable for EQ-0020 Spike 6.

---

## 10. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-S6-CONSUMER-VERSIONING |
| **EQ** | EQ-0020 |
| **Spike** | 6 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | BOQ_Intelligence_Public_Evidence_Contract_v1.1.md §Versioning Policy, Validation_Findings_Contract_v1.0.md §Contract Version, EQ-0012 Spike 2 (Versioning Policy), EQ-0013 Spike 4 (Engine Implementation) |

---

**End of Consumer Versioning Strategy**
