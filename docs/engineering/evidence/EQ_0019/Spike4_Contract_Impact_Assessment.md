# Spike 4 — Contract Impact Assessment

## EQ-0019 BOQ Semantic Intelligence Increment 1

### Purpose
Determine whether each Production Ready capability uses existing evidence, extends existing evidence, or requires a new contract version. Backward compatibility must be preserved.

### Authority
BOQ Intelligence Public Evidence Contract v1.0 (frozen)
- 10 evidence fields (4 required + 6 optional)
- 19 invariants (structural x8, type x4, semantic x3, determinism x4)
- Semantic versioning: MAJOR.MINOR.PATCH

### Versioning Rules
- MAJOR: Breaking changes to existing contracts (requires new EQ + PO approval)
- MINOR: New capabilities added (backward compatible)
- PATCH: Bug fixes, documentation, non-functional changes

---

## 1. Individual Capability Impact

### SEM-PROD-01: Vocabulary Extraction

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | New optional field |
| **New Field** | `vocabulary: dict[str, int] \| None` on `BOQIntelligenceResult` |
| **Backward Compatible?** | Yes — absent = None, existing consumers unaffected |
| **Existing Contract Area** | Extends `BOQIntelligenceResult` dataclass with new field |
| **Invariant Impact** | None — new invariants (INV-VOC-01 through -04) are additive |
| **Consumer Impact** | Existing consumers that don't read `vocabulary` are unaffected |

---

### SEM-PROD-02: Head1 Text Categorization

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | New optional field |
| **New Field** | `head1_categorization: dict[str, list[dict]] \| None` on `BOQIntelligenceResult` |
| **Backward Compatible?** | Yes — absent by default, must be requested via `include_semantic=True` flag |
| **Existing Contract Area** | Extends `BOQIntelligenceResult` dataclass with new field |
| **Invariant Impact** | None — new invariants (INV-H1C-01 through -04) are additive |
| **Consumer Impact** | Existing consumers that don't request categorization are unaffected |

---

### SEM-PROD-04: Administrative Pattern Detection

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | New optional field |
| **New Field** | `administrative_patterns: dict[str, list[dict]] \| None` on `BOQIntelligenceResult` |
| **Backward Compatible?** | Yes — requires `include_semantic=True` flag |
| **Existing Contract Area** | Extends `BOQIntelligenceResult` dataclass with new field |
| **Invariant Impact** | None — new invariants (INV-ADM-01 through -04) are additive |
| **Consumer Impact** | Existing consumers unaffected |

---

### SEM-PROD-05: Section Code Enumeration

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | Enhancement to existing field |
| **Existing Field** | `section_statistics: dict[str, dict[str, int]]` |
| **Change** | Add `section_code` and `section_name` to existing section statistics dictionaries |
| **Backward Compatible?** | Yes — existing fields (`negative_qty`, `positive_qty`) preserved. New keys are additive. |
| **Existing Contract Area** | Enhances `section_statistics` |
| **Invariant Impact** | None — structural invariants still hold |
| **Consumer Impact** | Consumers reading `section_statistics` still get existing data. New keys are optional reads. |

---

### SEM-PROD-06: UOM Distribution Reporting

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | New optional field |
| **New Field** | `uom_distribution: dict[str, int] \| None` plus `uom_percentages: dict[str, float] \| None` on `BOQIntelligenceResult` |
| **Backward Compatible?** | Yes — requires `include_semantic=True` flag |
| **Existing Contract Area** | Extends `BOQIntelligenceResult` dataclass with new fields |
| **Invariant Impact** | None — new invariants (INV-UOM-01 through -04) are additive |
| **Consumer Impact** | Existing consumers unaffected |

---

### SEM-PROD-07: Header Level Count Distribution

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | Enhancement to existing field |
| **Existing Field** | `row_classification: dict[str, int]` (currently counts Head as aggregate) |
| **Change** | Add `Head1`, `Head2`, `Head3`, `Head4` keys to `row_classification` dict |
| **Backward Compatible?** | Yes — existing `Head` key preserved. New keys are additive. |
| **Existing Contract Area** | Enhances `row_classification` |
| **Invariant Impact** | None — structural invariant still holds. Add consistency invariant: `Head == Head1 + Head2 + Head3 + Head4` |
| **Consumer Impact** | Consumers reading `row_classification['Head']` still work. New keys available for consumers that want per-level breakdown. |

---

### SEM-PROD-09: "Items Always Quantify" Enforcement

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | New optional detection field |
| **New Field** | `header_quantity_violations: tuple[dict[str, int \| str \| float \| None], ...] \| None` on `BOQIntelligenceResult` |
| **Backward Compatible?** | Yes — requires `include_detection=True` flag (follows existing Increment 3 pattern) |
| **Existing Contract Area** | Extends optional detection fields (alongside `detected_level_skips`, `zero_quantity_items`, etc.) |
| **Invariant Impact** | None — new invariants (INV-IAQ-01 through -04) are additive |
| **Consumer Impact** | Existing consumers unaffected. New detection field available to consumers that opt in. |

---

### SEM-PROD-12: Head1 Administrative Sub-Template Recognition

| Aspect | Assessment |
|---|---|
| **Contract Impact** | MINOR |
| **Change Type** | New optional field |
| **New Field** | `admin_template_matches: dict[str, list[dict]] \| None` on `BOQIntelligenceResult` |
| **Backward Compatible?** | Yes — requires `include_semantic=True` flag |
| **Existing Contract Area** | Extends `BOQIntelligenceResult` dataclass with new field |
| **Invariant Impact** | None — new invariants (INV-TMP-01 through -04) are additive |
| **Consumer Impact** | Existing consumers unaffected |

---

## 2. Aggregate Contract Impact

| Aspect | Assessment |
|---|---|
| **Contract Version Change** | MINOR (from 1.0.0 → 1.1.0) |
| **New Required Fields** | 0 — ALL new data is optional |
| **New Optional Fields** | 6 new fields (vocabulary, head1_categorization, administrative_patterns, uom_distribution + percentages, header_quantity_violations, admin_template_matches) |
| **Enhanced Existing Fields** | 2 (section_statistics, row_classification) |
| **Existing Required Fields** | Unchanged (row_type, quantity, uom, section_context) |
| **Existing Optional Fields** | Unchanged (code, description, rate, amount, row_number, sign) |
| **Existing Invariants** | All 19 unchanged |
| **New Invariants** | 28 (4 per new capability × 7 new capability areas) |
| **Backward Compatibility** | Fully preserved — no breaking changes |
| **Consumer Migration** | None required — existing consumers continue without modification |

---

## 3. Consumer Guarantee Impact

The 16 permanent consumer guarantees from Contract v1.0 remain unchanged. Specifically:

| Guarantee Category | Status |
|---|---|
| Structural (4) | Unchanged |
| Type (4) | Unchanged |
| Semantic (3) | Unchanged |
| Determinism (4) | Unchanged |
| Access (1) | Unchanged |

**New consumer guarantees for Increment 4 (implied):**

| ID | Category | Guarantee |
|---|---|---|
| G-SEM-01 | Semantic | Vocabulary extraction reports term frequencies only — no semantic meaning |
| G-SEM-02 | Semantic | Head1 categorization uses exact string matching against frozen patterns only |
| G-SEM-03 | Access | All new semantic capabilities are opt-in via `include_semantic` flag |

---

## 4. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Consumer depends on new optional field being present | Low | Minor | Always opt-in pattern — consumer must explicitly request |
| New invariants create developer burden | Low | Low | Automated test suite covers all invariants |
| Future consumer requests incompatible changes | Medium | Medium | Contract versioning policy (MAJOR = new EQ + PO approval) |
| Template patterns need updating | Low | Medium | Frozen templates require EQ modification — prevents ad-hoc changes |

---

## 5. Decision

**Contract v1.0.0 → v1.1.0 (MINOR)**

Implementation shall:
1. Add 6 new optional fields to `BOQIntelligenceResult`
2. Enhance 2 existing fields (`section_statistics`, `row_classification`)
3. Preserve all 19 existing invariants
4. Add 28 new invariants
5. Add `include_semantic` parameter to `analyze_boq()`
6. Maintain full backward compatibility

**No MAJOR version change is required.**

---

## Document Control

**Version:** 1.0
**Spike:** 4 of 7
**EQ:** EQ-0019
**Status:** Complete
**Last Updated:** 2026-07-25
**Owner:** Project Owner