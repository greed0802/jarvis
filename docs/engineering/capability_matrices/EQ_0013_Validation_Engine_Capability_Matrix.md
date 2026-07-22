# EQ-0013: Validation Engine Capability Matrix

**Status:** FROZEN — Gate 3 Approved
**Authority:** EQ-0013 Spike 4
**Contract Version:** Validation Findings Contract v1.0.0
**Engine Version:** v1.0.0
**Registry Version:** v1.0.0

---

## 1. Purpose

This matrix documents all validation capabilities implemented by the Validation Engine v1.0.0.

The Validation Engine consumes the frozen BOQ Intelligence Public Evidence Contract v1.0.0 and produces deterministic findings per the Validation Findings Contract v1.0.0.

---

## 2. Validation Rule Registry

**Total Rules:** 22
**Implemented Rules:** 18 (V-001 through V-018)
**Rejected Rules:** 4 (V-801, V-802, V-901, V-902)

---

## 3. Rule Classification Matrix

### 3.1. By Category

| Category | Count | Rule IDs |
|----------|-------|----------|
| Structural | 3 | V-001, V-002, V-003 |
| Consistency | 3 | V-004, V-005, V-006 |
| Completeness | 3 | V-007, V-008, V-009 |
| Hierarchy | 3 | V-010, V-011, V-012 |
| Detection | 6 | V-013, V-014, V-015, V-016, V-017, V-018 |
| Financial | 1 | V-801 (Rejected) |
| Reference | 1 | V-802 (Rejected) |
| Assessment | 1 | V-901 (Rejected) |
| Recommendation | 1 | V-902 (Rejected) |

### 3.2. By Boundary Class

| Boundary Class | Count | Rule IDs |
|----------------|-------|----------|
| Observation | 14 | V-001, V-002, V-003, V-004, V-005, V-007, V-008, V-009, V-010, V-011, V-012, V-013, V-016, V-017 |
| Detection | 4 | V-014, V-015, V-018, V-801 |
| Violation | 4 | V-802, V-901, V-902 (Rejected) |

### 3.3. By Classification

| Classification | Count | Rule IDs |
|----------------|-------|----------|
| Supported | 12 | V-001, V-002, V-003, V-007, V-008, V-009, V-010, V-011, V-012, V-013, V-016, V-017 |
| Multiple Fields | 6 | V-004, V-005, V-006, V-014, V-015, V-018 |
| Insufficient Evidence | 2 | V-801, V-802 (Rejected) |
| Boundary Violation | 2 | V-901, V-902 (Rejected) |

### 3.4. By Status

| Status | Count | Rule IDs |
|--------|-------|----------|
| Approved | 18 | V-001 through V-018 |
| Deprecated | 4 | V-801, V-802, V-901, V-902 |

---

## 4. Finding Type Matrix

| Finding Type | Count | Rule IDs |
|--------------|-------|----------|
| list | 6 | V-001, V-002, V-003, V-005, V-006, V-010 |
| difference | 1 | V-004 |
| ratio | 3 | V-007, V-008, V-009 |
| presence | 2 | V-010, V-013 |
| count | 4 | V-011, V-014, V-016, V-017 |
| value | 6 | V-012, V-015, V-018, V-801, V-802, V-901, V-902 |

---

## 5. Evidence Field Matrix

| Evidence Field | Count | Rule IDs |
|----------------|-------|----------|
| row_classification | 3 | V-001, V-002, V-003 |
| section_statistics | 2 | V-001, V-005 |
| boq_statistics | 6 | V-001, V-004, V-006, V-007, V-008, V-009 |
| known_anomalies | 1 | V-006 |
| hierarchy | 1 | V-010 |
| hierarchy_statistics | 2 | V-011, V-012 |
| detected_level_skips | 3 | V-013, V-014, V-015 |
| zero_quantity_items | 1 | V-016 |
| structural_containment_findings | 1 | V-017 |
| completeness_findings | 1 | V-018 |

---

## 6. Rule Detail Table

| Rule ID | Category | Description | Evidence Fields | Boundary Class | Classification | Status | Finding Type | Deterministic Finding |
|---------|----------|-------------|-----------------|----------------|----------------|--------|--------------|------------------------|
| V-001 | Structural | Verify all required evidence fields are present | row_classification, section_statistics, boq_statistics, known_anomalies | Observation | Supported | Approved | list | Lists missing required fields (empty if all present) |
| V-002 | Structural | Verify row_classification contains exactly 5 expected keys | row_classification | Observation | Supported | Approved | list | Reports missing or unexpected keys |
| V-003 | Structural | Verify row_classification values are non-negative integers | row_classification | Observation | Supported | Approved | list | Reports negative values |
| V-004 | Consistency | Verify sum of row_classification equals total_rows | row_classification, boq_statistics | Observation | Multiple Fields | Approved | difference | Reports difference between sum and total_rows |
| V-005 | Consistency | Verify all sections have non-negative quantity counts | section_statistics | Observation | Multiple Fields | Approved | list | Reports sections with negative quantity counts |
| V-006 | Consistency | Verify known_anomalies row_numbers are within [1, total_rows] | known_anomalies, boq_statistics | Observation | Multiple Fields | Approved | list | Reports anomalies with out-of-range row numbers |
| V-007 | Completeness | Calculate ratio of code_rows to total_rows | boq_statistics | Observation | Supported | Approved | ratio | Reports completeness ratio (0.0 to 1.0) |
| V-008 | Completeness | Calculate ratio of description_rows to total_rows | boq_statistics | Observation | Supported | Approved | ratio | Reports completeness ratio (0.0 to 1.0) |
| V-009 | Completeness | Calculate ratio of quantity_rows to total_rows | boq_statistics | Observation | Supported | Approved | ratio | Reports completeness ratio (0.0 to 1.0) |
| V-010 | Hierarchy | Check if hierarchy evidence is available (not None) | hierarchy | Observation | Supported | Approved | presence | Returns True if hierarchy is available, False otherwise |
| V-011 | Hierarchy | Report number of root headers, or None if hierarchy unavailable | hierarchy_statistics | Observation | Supported | Approved | count | Returns number of root headers, or None if hierarchy unavailable |
| V-012 | Hierarchy | Report min/max depth, or None if hierarchy unavailable | hierarchy_statistics | Observation | Supported | Approved | value | Returns dict with min_depth and max_depth, or None if hierarchy unavailable |
| V-013 | Detection | Check if level skip detection evidence is available | detected_level_skips | Observation | Supported | Approved | presence | Returns True if level skips are available, False otherwise |
| V-014 | Detection | Count detected level skips, or None if unavailable | detected_level_skips | Detection | Multiple Fields | Approved | count | Returns number of level skips, or None if unavailable |
| V-015 | Detection | Report min/max skip magnitude, or None if unavailable | detected_level_skips | Detection | Multiple Fields | Approved | value | Returns dict with min_magnitude and max_magnitude, or None if unavailable |
| V-016 | Detection | Count zero quantity items, or None if unavailable | zero_quantity_items | Observation | Supported | Approved | count | Returns number of zero quantity items, or None if unavailable |
| V-017 | Detection | Count structural containment findings, or None if unavailable | structural_containment_findings | Observation | Supported | Approved | count | Returns number of structural containment findings, or None if unavailable |
| V-018 | Detection | Count sections with zero items, or None if unavailable | completeness_findings | Detection | Multiple Fields | Approved | count | Returns number of sections with zero items, or None if unavailable |
| V-801 | Financial | Verify item costs are reasonable | — | Detection | Insufficient Evidence | Deprecated | value | N/A - no cost evidence |
| V-802 | Reference | Verify items reference valid drawings | — | Observation | Insufficient Evidence | Deprecated | value | N/A - no drawing evidence |
| V-901 | Assessment | Assess whether hierarchy is structurally valid | hierarchy | Detection | Boundary Violation | Deprecated | value | N/A - crosses boundary |
| V-902 | Recommendation | Recommend whether level skips should be corrected | detected_level_skips | Detection | Boundary Violation | Deprecated | value | N/A - crosses boundary |

---

## 7. Consumer Compliance Requirements

All consumers of the Validation Engine must:

- Consume `ValidationFindings`, not raw engine output
- Not mutate findings (frozen dataclasses)
- Respect `finding_type` semantics
- Not rely on finding ordering beyond alphanumeric sort
- Handle empty findings (findings tuple length = 0)
- Handle `None` finding_value for optional evidence
- Not expect recommendations or assessments
- Maintain their own interpretation layer

---

## 8. Contract Compliance

| Contract | Compliance Status |
|----------|-------------------|
| Validation Findings Contract v1.0.0 | ✓ FULL COMPLIANCE |
| Evidence Contract v1.0.0 | ✓ FULL COMPLIANCE |
| EQ-0011 Boundary | ✓ FULL COMPLIANCE |

---

## 9. Verification

| Verification Item | Status | Tool |
|-------------------|--------|------|
| Registry validation | ✓ PASS | `tools/eq0013_registry_validator.py` |
| Engine smoke test | ✓ PASS | `tools/eq0013_spike4_smoke_test.py` |
| Regression suite | ✓ PASS | `tests/validation/test_engine.py` (34 tests) |
| Determinism | ✓ VERIFIED | TestDeterminism class |
| Contract compliance | ✓ VERIFIED | TestContractCompliance class |
| finding_type correctness | ✓ VERIFIED | TestFindingType class |

---

## 10. Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-07-15 | 1.0.0 | Initial freeze — EQ-0013 Spike 4 |
| 2026-07-16 | 1.0.0 | HD-004: finding_type added to registry, heuristic removed |
| 2026-07-16 | 1.0.0 | HD-006: Registry validator fixes applied |

---

**End of Capability Matrix — EQ-0013 Frozen**