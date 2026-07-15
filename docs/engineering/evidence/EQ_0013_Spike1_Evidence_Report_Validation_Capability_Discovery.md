# EQ-0013 Spike 1: Validation Capability Discovery

**Evidence Report ID:** EQ-0013-S1-EVD
**Date:** 2026-07-15
**Status:** Complete
**Authority:** EQ-0013 (Validation Engine Investigation)
**Contract Version:** BOQ Intelligence Public Evidence Contract v1.0.0
**Engineering Boundary:** EQ-0011 (Observe/Reconstruct/Detect)

---

## Executive Summary

Spike 1 discovered **22 validation rules** derivable from the frozen Public Evidence Contract v1.0, established the Validation Rule Registry as a governance artifact, and classified each rule by implementation feasibility and boundary compliance.

**Key Findings:**
- **18 rules** can proceed toward implementation (16 Supported + 2 Multiple Fields)
- **2 rules** cross EQ-0011 boundary (documented but rejected)
- **2 rules** require additional evidence not in Contract v1.0 (documented but rejected)
- **0 speculative rules** (all rules evidence-backed)

---

## Investigation Objective

**Question:** What deterministic validation capabilities are possible using only the frozen Public Evidence Contract v1.0?

**Not Asked:**
- How to implement validations (belongs to future spikes)
- What consumers need (consumer-independent investigation)
- What recommendations to make (crosses EQ-0011 boundary)

---

## Methodology

### Evidence-First Discovery

1. **Read frozen Evidence Contract v1.0** — 10 evidence fields from Increments 1-3
2. **Enumerate validation capabilities** — Single-field and cross-field checks
3. **Classify every rule** — Supported, Multiple Fields, Insufficient Evidence, Boundary Violation, Speculative
4. **Document provenance** — Every rule traces to frozen evidence (EQ-0010, EQ-0011, EQ-0012)
5. **Preserve boundary** — Evidence → Rule → Finding → Human Interpretation

### Classification System

| Classification | Definition | Can Proceed? |
|----------------|------------|--------------|
| **Supported** | Implementable with single evidence field | Yes |
| **Multiple Fields** | Requires multiple evidence fields | Yes |
| **Insufficient Evidence** | Missing evidence in Contract v1.0 | No |
| **Boundary Violation** | Crosses EQ-0011 boundary | No |
| **Speculative** | Not backed by frozen evidence | No |

---

## Discovered Validation Rules

### Summary Statistics

| Metric | Count |
|--------|-------|
| Total Rules Discovered | 22 |
| Supported (Single Field) | 16 |
| Multiple Fields | 2 |
| Insufficient Evidence | 2 |
| Boundary Violations | 2 |
| Speculative | 0 |
| **Implementable Rules** | **18** |

### Rule Categories

| Category | Count | Rules |
|----------|-------|-------|
| Structural | 6 | V-001, V-002, V-003, V-010, V-011, V-012 |
| Consistency | 3 | V-004, V-005, V-006 |
| Completeness | 3 | V-007, V-008, V-009 |
| Detection | 6 | V-013, V-014, V-015, V-016, V-017, V-018 |
| Assessment (Rejected) | 1 | V-901 |
| Recommendation (Rejected) | 1 | V-902 |
| Financial (Rejected) | 1 | V-801 |
| Reference (Rejected) | 1 | V-802 |

---

## Validation Rule Registry v1.0

### Structural Validations (6 rules)

#### V-001: Required Field Presence
- **Evidence Fields:** row_classification, section_statistics, boq_statistics, known_anomalies
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Lists missing required fields (empty if all present)
- **Rationale:** Contract guarantees G-01, G-02 (required fields always present)
- **EQ Source:** EQ-0012

#### V-002: Row Classification Shape
- **Evidence Fields:** row_classification
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports missing or unexpected keys
- **Rationale:** Contract invariant SI-RC-04 (5 keys: Head, Note, Section, Item, Other)
- **EQ Source:** EQ-0012

#### V-003: Row Classification Non-Negative
- **Evidence Fields:** row_classification
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports negative count values
- **Rationale:** Counts represent observed row frequencies, cannot be negative
- **EQ Source:** EQ-0010

#### V-010: Hierarchy Availability
- **Evidence Fields:** hierarchy
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports whether hierarchy was reconstructed
- **Rationale:** Hierarchy is optional evidence (include_hierarchy parameter)
- **EQ Source:** EQ-0010

#### V-011: Root Header Count
- **Evidence Fields:** hierarchy_statistics
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports root_headers count or None if unavailable
- **Rationale:** Observes hierarchy structure
- **EQ Source:** EQ-0010

#### V-012: Hierarchy Depth Range
- **Evidence Fields:** hierarchy_statistics
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports (min_depth, max_depth) or None if unavailable
- **Rationale:** Observes hierarchy depth distribution
- **EQ Source:** EQ-0010

---

### Consistency Validations (3 rules)

#### V-004: Total Rows Consistency
- **Evidence Fields:** row_classification, boq_statistics
- **Boundary Class:** Relationship
- **Classification:** Multiple Fields
- **Finding:** Reports discrepancy magnitude if sums don't match
- **Rationale:** Classification counts must sum to total (cross-field dependency)
- **EQ Source:** EQ-0010

#### V-005: Section Statistics Coverage
- **Evidence Fields:** section_statistics
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports sections with invalid (negative) counts
- **Rationale:** Quantity counts represent observed frequencies
- **EQ Source:** EQ-0010

#### V-006: Anomaly Row Numbers Within Range
- **Evidence Fields:** known_anomalies, boq_statistics
- **Boundary Class:** Relationship
- **Classification:** Multiple Fields
- **Finding:** Reports anomalies with out-of-range row numbers
- **Rationale:** Row numbers reference BOQ rows, must be within observed range
- **EQ Source:** EQ-0010

---

### Completeness Validations (3 rules)

#### V-007: Code Column Completeness
- **Evidence Fields:** boq_statistics
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports completeness ratio (0.0 to 1.0)
- **Rationale:** Observes code column population density
- **EQ Source:** EQ-0010

#### V-008: Description Column Completeness
- **Evidence Fields:** boq_statistics
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports completeness ratio (0.0 to 1.0)
- **Rationale:** Observes description column population density
- **EQ Source:** EQ-0010

#### V-009: Quantity Column Completeness
- **Evidence Fields:** boq_statistics
- **Boundary Class:** Observation
- **Classification:** Supported
- **Finding:** Reports completeness ratio (0.0 to 1.0)
- **Rationale:** Observes quantity column population density
- **EQ Source:** EQ-0010

---

### Detection Validations (6 rules)

#### V-013: Level Skip Detection Availability
- **Evidence Fields:** detected_level_skips
- **Boundary Class:** Detection
- **Classification:** Supported
- **Finding:** Reports whether level skips were detected
- **Rationale:** Detection is optional evidence (include_detection parameter)
- **EQ Source:** EQ-0011

#### V-014: Level Skip Count
- **Evidence Fields:** detected_level_skips
- **Boundary Class:** Detection
- **Classification:** Supported
- **Finding:** Reports skip count or None if unavailable
- **Rationale:** Observes level skip pattern frequency
- **EQ Source:** EQ-0011

#### V-015: Level Skip Magnitude Range
- **Evidence Fields:** detected_level_skips
- **Boundary Class:** Detection
- **Classification:** Supported
- **Finding:** Reports (min_magnitude, max_magnitude) or None
- **Rationale:** Observes skip magnitude distribution
- **EQ Source:** EQ-0011

#### V-016: Zero Quantity Item Count
- **Evidence Fields:** zero_quantity_items
- **Boundary Class:** Detection
- **Classification:** Supported
- **Finding:** Reports count or None if unavailable
- **Rationale:** Observes zero quantity pattern frequency
- **EQ Source:** EQ-0011

#### V-017: Structural Containment Finding Count
- **Evidence Fields:** structural_containment_findings
- **Boundary Class:** Detection
- **Classification:** Supported
- **Finding:** Reports finding count or None if unavailable
- **Rationale:** Observes structural inversion frequency
- **EQ Source:** EQ-0011

#### V-018: Empty Section Count
- **Evidence Fields:** completeness_findings
- **Boundary Class:** Detection
- **Classification:** Supported
- **Finding:** Reports empty section count or None if unavailable
- **Rationale:** Observes section-level item completeness
- **EQ Source:** EQ-0011

---

## Rejected Rules (Documented for Completeness)

### Boundary Violations (2 rules)

#### V-901: BOQ Quality Assessment (REJECTED)
- **Evidence Fields:** boq_statistics
- **Boundary Class:** Violation
- **Classification:** Boundary Violation
- **Rationale:** Crosses EQ-0011 boundary (Assess/Judge)
- **Status:** Documented but rejected

#### V-902: Level Skip Recommendation (REJECTED)
- **Evidence Fields:** detected_level_skips
- **Boundary Class:** Violation
- **Classification:** Boundary Violation
- **Rationale:** Crosses EQ-0011 boundary (Recommend)
- **Status:** Documented but rejected

### Insufficient Evidence (2 rules)

#### V-801: Item Cost Validation (REJECTED)
- **Evidence Fields:** (none)
- **Boundary Class:** Observation
- **Classification:** Insufficient Evidence
- **Rationale:** No cost/price evidence in Contract v1.0
- **Status:** Documented but rejected

#### V-802: Drawing Reference Validation (REJECTED)
- **Evidence Fields:** (none)
- **Boundary Class:** Relationship
- **Classification:** Insufficient Evidence
- **Rationale:** No drawing reference evidence in Contract v1.0
- **Status:** Documented but rejected

---

## Evidence-to-Rule Mapping

### Evidence Field Coverage

| Evidence Field | Supported Rules | Multiple Field Rules | Total |
|----------------|-----------------|---------------------|-------|
| row_classification | 3 | 1 | 4 |
| section_statistics | 1 | 0 | 1 |
| boq_statistics | 4 | 2 | 6 |
| known_anomalies | 0 | 1 | 1 |
| hierarchy | 1 | 0 | 1 |
| hierarchy_statistics | 2 | 0 | 2 |
| detected_level_skips | 3 | 0 | 3 |
| zero_quantity_items | 1 | 0 | 1 |
| structural_containment_findings | 1 | 0 | 1 |
| completeness_findings | 1 | 0 | 1 |

### Highest Coverage Fields

1. **boq_statistics** — 6 rules (completeness ratios, consistency checks)
2. **row_classification** — 4 rules (structural checks, consistency)
3. **detected_level_skips** — 3 rules (detection availability, count, magnitude)

---

## Boundary Compliance Analysis

### Boundary Class Distribution

| Boundary Class | Count | Percentage |
|----------------|-------|------------|
| Observation | 11 | 50% |
| Detection | 6 | 27% |
| Relationship | 3 | 14% |
| Violation | 2 | 9% |

**Result:** 20/22 rules (91%) preserve EQ-0011 boundary. 2 violations documented but rejected.

### EQ-0011 Boundary Preservation

All 18 implementable rules follow:
```
Evidence → Deterministic Rule → Deterministic Finding → Human Interpretation
```

Never:
```
Evidence → Automatic Recommendation
```

**Examples:**
- ✓ V-014: "Reports skip count" (Finding)
- ✓ V-007: "Reports completeness ratio" (Finding)
- ✗ V-902: "Recommend whether to correct" (Recommendation — REJECTED)
- ✗ V-901: "Assess overall quality" (Assessment — REJECTED)

---

## Rule Provenance Matrix

### All Rules Trace to Frozen Evidence

| EQ Source | Rule Count | Rules |
|-----------|------------|-------|
| EQ-0010 | 9 | V-003, V-004, V-005, V-006, V-007, V-008, V-009, V-010, V-011, V-012 |
| EQ-0011 | 6 | V-013, V-014, V-015, V-016, V-017, V-018 |
| EQ-0012 | 3 | V-001, V-002, (plus 4 rejected) |

**No speculative rules:** Every rule originated from frozen engineering evidence (EQ-0010, EQ-0011) or Contract invariants (EQ-0012).

---

## Consumer Independence

### No Application-Specific Logic

All 18 implementable rules are application-independent:
- No "CheckMate needs X" reasoning
- No "Formatter requires Y" assumptions
- Only "What does evidence support?" questions

**Result:** All rules reusable across CheckMate, Formatter, Builder, O&A, Reporting.

---

## Unsupported Validation Inventory

### What Contract v1.0 Cannot Support

**Financial Validations:**
- Item cost reasonableness (no cost evidence)
- Budget compliance (no budget evidence)
- Price variations (no historical price evidence)

**Reference Validations:**
- Drawing linkage (no drawing reference evidence)
- Specification references (no specification evidence)
- External document validation (no document ID evidence)

**Temporal Validations:**
- Schedule alignment (no schedule evidence)
- Version history (no versioning evidence)
- Change tracking (no change log evidence)

**Professional Validations:**
- Trade-specific rules (crosses boundary)
- Industry standards compliance (crosses boundary)
- Best practice adherence (crosses boundary)

---

## Deliverables

### Generated Artifacts

1. **Validation Rule Registry** — `data/reports/eq0013_spike1_validation_rule_registry.json`
   - 22 rules with complete provenance
   - Rule ID, category, evidence fields, boundary class, classification, status, finding, rationale, EQ source

2. **Evidence-to-Rule Mapping** — `data/reports/eq0013_spike1_evidence_to_rule_mapping.json`
   - Maps each evidence field to rules that consume it
   - Supports impact analysis for Contract evolution

3. **Classification Summary** — `data/reports/eq0013_spike1_classification_summary.json`
   - Classification distribution
   - Boundary class distribution
   - Evidence field coverage

4. **Discovery Tool** — `tools/eq0013_spike1_validation_capability_discovery.py`
   - Executable Python tool
   - Generates all artifacts
   - Reproducible evidence generation

---

## Key Insights

### 1. Most Validations Are Observational

16 of 18 implementable rules (89%) are pure observation or detection checks. Only 2 rules require cross-field relationship logic.

**Implication:** Validation Engine will be dominated by single-field observation logic.

### 2. Optional Evidence Requires Availability Checks

6 rules depend on optional evidence (hierarchy, detection). All include "or None if unavailable" in their findings.

**Implication:** Validation Engine must handle optional evidence gracefully.

### 3. Contract Invariants Enable Structural Validation

3 rules (V-001, V-002, V-003) derive directly from Contract invariants (SI-RC-01, SI-RC-04).

**Implication:** Contract invariants are validatable assertions, not just documentation.

### 4. Boundary Preservation Is Achievable

2/22 rules (9%) crossed EQ-0011 boundary, both easily identified and rejected.

**Implication:** Boundary violations are detectable during discovery.

### 5. Evidence Gaps Are Explicit

2 rules identified missing evidence (cost, drawing references). These define Contract v2.0 requirements.

**Implication:** Validation capability discovery reveals evidence gaps.

---

## Recommendations for Spike 2

### Validation Rule Taxonomy

Spike 2 should formalize rule categories discovered in Spike 1:
- **Structural** — Presence, type, shape checks
- **Consistency** — Cross-field arithmetic/logical consistency
- **Completeness** — Data population relative to total
- **Detection** — Pattern observation (from EQ-0011 detection evidence)

### Rule Status Lifecycle

Establish rule status transitions:
- Candidate → Approved → Deprecated → Retired

### Registry Evolution

Define how rules are added/modified/removed:
- New rules require provenance (evidence field + EQ source)
- Rule changes require Contract version update
- Deprecated rules remain in registry with status change

---

## Verification

### Tool Execution

```bash
$ python tools/eq0013_spike1_validation_capability_discovery.py
Discovered 22 validation rules

Rule Classifications:
  Supported: 16 rules
  Multiple Fields: 2 rules
  Insufficient Evidence: 2 rules
  Boundary Violation: 2 rules
  Speculative: 0 rules

✓ Saved Validation Rule Registry
✓ Saved Evidence-to-Rule Mapping
✓ Saved Classification Summary
```

**Result:** 100% reproducible artifact generation.

---

## Conclusion

Spike 1 successfully discovered 18 implementable validation rules from the frozen Public Evidence Contract v1.0. All rules preserve EQ-0011 boundary, trace to frozen evidence, and remain consumer-independent.

**Next:** Spike 2 will formalize the Validation Rule Taxonomy, define rule categories against EQ-0011 boundary, and establish governance for rule evolution.

---

## Document Control

**Evidence Report ID:** EQ-0013-S1-EVD
**Status:** Complete
**Date:** 2026-07-15
**Authority:** EQ-0013 Spike 1
**Distribution:** Engineering team, Project Owner

---

**End of Evidence Report**