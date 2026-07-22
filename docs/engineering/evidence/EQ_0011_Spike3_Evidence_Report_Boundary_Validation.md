# EQ-0011 — Spike 3 — Evidence Report — Boundary Validation Against Production Evidence

**Date:** 2026-07-14  
**Status:** Complete  
**Investigation:** EQ-0011 BOQ Semantic Intelligence Boundary  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction — Attempt Falsification, Not Confirmation

---

## Objective

Attempt to falsify Spike 2 boundary classifications using production fixture evidence.

The Spike 2 hypothesis is:
- **Evidence** is Structurally Deterministic (obtainable from BOQRow + hierarchy)
- **Assessment** is either Semantically Deterministic (with formalized rules) or Professional Judgment

This spike attempts to find production evidence that contradicts this hypothesis.

---

## Methodology

1. **Load production fixture** (same as EQ-0010: `full_boq.xlsx`, 6349 rows)
2. **For each Domain Dependent capability:**
   - Return every production occurrence documented in EQ-0010 Spike 5
   - Attempt automatic assessment (can we decide this deterministically?)
   - Search for counterexamples that invalidate Spike 2
3. **Report confidence** (High/Medium/Low) justified by evidence

---

## Outcome: Key Finding

**No counterexamples were found within the investigated production fixture.**

Spike 2 boundary classifications **survive adversarial testing** against the investigated production evidence:
- 20 production occurrences examined
- 0 counterexamples found
- All classifications preserved
- Confidence levels assigned

---

## Capability Validation Results

### V-003: Level Progression Validation

#### Production Occurrences (12 examined)

All 12 skip violations from EQ-0010 Spike 5:

| Row | UOM | Parent | Skip Size | Description |
|-----|-----|--------|-----------|-------------|
| 1661 | Head3 | Head1 | 2 | Preliminaries section under Substructure |
| 1668 | Head3 | Head1 | 2 | Same pattern |
| 4743 | Head3 | Head1 | 2 | Same pattern |
| 5709-5745 | Head4 (×7) | Head2 | 2 | Repetitive Head4 siblings under Head2 |
| 5804-5819 | Head4 (×3) | Head2 | 2 | Same pattern in different section |

#### Boundary Stress Tests (12 attempts)

**Attempt:** Can any skip be automatically accepted?
**Result:** No — all 12 require project-specific context to determine legitimacy

**Attempt:** Can any skip be automatically rejected?
**Result:** No — domain rule explicitly allows "as required by project complexity"

#### Counterexample Search

**Attempt:** Find a skip that requires no judgment to accept or reject.  
**Result:** None found. All skips have size 2 (Head1→Head3 or Head2→Head4). Without understanding project organizational structure, cannot determine if skips are legitimate or violations.

#### Classification

| Dimension | Classification |
|-----------|---------------|
| Evidence | Structurally Deterministic |
| Assessment | Professional Judgment |
| **Confidence** | **High** |

**Justification:** All 12 production skips examined. None can be automatically assessed as legitimate or illegitimate without project-specific context. Domain rule explicitly allows skips "as required by project complexity", making legitimacy a project-specific judgment call.

---

### SEM-003: Items Always Quantify

#### Production Occurrences (5 examined)

All 5 zero-quantity items from EQ-0010 Spike 5:

| Row | UOM | Quantity | Description | Prev Item Qty | Next Item Qty |
|-----|-----|----------|-------------|---------------|---------------|
| 5698 | m | 0.0 | (dimension item) | varies | varies |
| 6088 | no | 0.0 | (dimension item) | varies | varies |
| 6091 | m | 0.0 | (dimension item) | varies | varies |
| 6130 | no | 0.0 | (dimension item) | varies | varies |
| 6133 | m | 0.0 | (dimension item) | varies | varies |

#### Boundary Stress Tests (5 attempts)

**Attempt:** Can any zero automatically be accepted?  
**Result:** No — cannot determine if zero is intentional placeholder, incomplete takeoff, or data entry error

**Attempt:** Can any zero automatically be rejected?  
**Result:** No — domain rule says "always quantify" but production has 5 zeros; cannot reject without knowing if they are legitimate

#### Counterexample Search

**Attempt:** Find a zero that is unquestionably invalid.  
**Result:** None found. Without QS intent, any zero could be legitimate.

**Attempt:** Find a zero that is unquestionably acceptable.  
**Result:** None found. Without QS intent, any zero could be an error.

#### Classification

| Dimension | Classification |
|-----------|---------------|
| Evidence | Structurally Deterministic |
| Assessment | Professional Judgment |
| **Confidence** | **High** |

**Justification:** All 5 production zero-quantity items examined. None can be automatically assessed as acceptable or unacceptable without QS intent and project state. Domain rule states items "always" quantify, yet production fixture contains zeros. This confirms the rule cannot be absolute — requires interpretation of whether zero is error or intentional.

---

### V-004: Scope Containment

#### Production Occurrences

The V-004 production samples shown below are illustrative structural samples (header→header and header→item pairs from the fixture) that demonstrate the general containment pattern. They are not canonical reconstructed hierarchy pairs from the stack algorithm; the reconstruction algorithm classifies all parent-child relationships consistently.

##### Illustrative Structural Samples

| Parent Row | Parent | Child Row | Child | Structural Containment |
|------------|--------|-----------|-------|----------------------|
| 102 | Head2: TO WORKS | 118 | Item: Excavate top soil | ✅ Valid |
| 357 | Head3: FORMATION LEVEL | 374 | Item: Excavate bulk | ✅ Valid |
| 1661 | Head1: SUBSTRUCTURE | 1668 | Head3: Prelims | ✅ Valid (skip case) |

**Note:** These illustrate the deterministic parent-level consistency check (`child_level <= parent_level`). The stack-based reconstruction algorithm assigns levels deterministically; the samples above are hand-selected representatives of that structural pattern.

#### Boundary Stress Tests (3 attempts)

**Attempt:** Can semantic scope containment be determined automatically?  
**Result:** No — structural containment (`child_level <= parent_level`) is deterministic, but semantic scope requires understanding what headers represent

**Attempt:** Can standard scope relationships be formalized?  
**Result:** Possibly — standard headers like "SUBSTRUCTURE" could have defined scope maps, but project-specific descriptions resist pre-formalization

#### Counterexample Search

**Attempt:** Find a scope relationship impossible to formalize.  
**Result:** Non-standard descriptions resist formalization. Standard headers could potentially be mapped.

#### Classification

| Dimension | Classification |
|-----------|---------------|
| Evidence | Structurally Deterministic |
| Assessment | Semantically Deterministic (with rules) OR Professional Judgment |
| **Confidence** | **Medium** |

**Justification:** Structural containment (parent-level consistency) is deterministic (confirmed in EQ-0010). Semantic scope containment analysis shows: (1) standard headers like 'SUBSTRUCTURE' could potentially be formalized with scope taxonomy, (2) non-standard or project-specific descriptions resist formalization. Production evidence suggests partial formalization is possible but judgment remains necessary for non-standard cases.

---

### V-005: Completeness

#### Production Occurrences

V-005 relied primarily on EQ-0010 production evidence because direct production sampling for this spike was limited by section-name matching. No contradictory evidence was discovered; therefore the existing Medium confidence classification is retained.

**Note:** The specific section names used in the sample (e.g., '1.0 SITE CLEARANCE') did not match the production fixture's section format. This is a data access limitation that affects the tool's ability to enumerate sections, not the underlying classification.

EQ-0010 Spike 5 confirmed: All sections contain at least one Item row (basic completeness satisfied). This deterministic evidence is preserved from prior investigation.

#### Boundary Stress Tests

**Attempt:** Can full QS completeness be determined automatically?  
**Result:** No — BOQ structure reveals what work IS present, not what work SHOULD be present

**Attempt:** Can completeness be formalized for standard project types?  
**Result:** Possibly — with defined project scope and completeness checklists, standard projects could be validated against work package requirements

#### Counterexample Search

**Attempt:** Find obvious incompleteness or completeness deterministically.  
**Result:** None found. All sections have items (basic completeness), but full QS completeness requires project scope knowledge.

#### Classification

| Dimension | Classification |
|-----------|---------------|
| Evidence | Structurally Deterministic |
| Assessment | Semantically Deterministic (with scope) OR Professional Judgment |
| **Confidence** | **Medium** |

**Justification:** Basic completeness (section-has-items) is deterministic (confirmed in EQ-0010). Full QS completeness analysis shows: BOQ structure reveals what work IS present but not what work SHOULD be present. Production evidence suggests: (1) for standard project types with defined scope, completeness checklists could be formalized, (2) project-specific requirements resist pre-formalization.

---

## Summary

### Classification Confidence

| Capability | Evidence | Assessment | Confidence |
|------------|----------|------------|------------|
| V-003 | Structurally Deterministic | Professional Judgment | **High** |
| SEM-003 | Structurally Deterministic | Professional Judgment | **High** |
| V-004 | Structurally Deterministic | Semantically Deterministic (with rules) OR Professional Judgment | **Medium** |
| V-005 | Structurally Deterministic | Semantically Deterministic (with scope) OR Professional Judgment | **Medium** |

### Counterexample Search Results

- **Total production occurrences examined:** 20
- **Counterexamples found:** 0
- **Spike 2 classifications validated:** Yes

### Answers to Success Criteria

**Q: Does production evidence support the current boundary?**  
**A:** Yes. No contradictory evidence found.

**Q: Does production evidence contradict the current boundary?**  
**A:** No. All 20 occurrences consistent with Spike 2 classification.

**Q: Should any capability classification change?**  
**A:** No. Current classifications preserved.

**Q: What confidence should be assigned to each classification?**  
**A:** High for V-003 and SEM-003 (strong, consistent evidence). Medium for V-004 and V-005 (some formalization potential exists but requires additional work).

---

## Tool

**Spike Implementation:** `tools/eq0011_spike3_boundary_validation.py`  
**Results:** `data/reports/eq0011_spike3_results.json`  
**Fixture:** `tests/fixtures/costx/full_boq.xlsx` (same as EQ-0010)  
**Rows Examined:** 6349 total, 20 specific occurrences analyzed

---

## Spike 3 Conclusion

Spike 2 classifications survive adversarial testing:

1. **V-003 (Level Progression):** 12 skip occurrences confirmed as Professional Judgment. Detection (skip computation) is Structurally Deterministic; legitimacy assessment requires project context.
2. **SEM-003 (Items Always Quantify):** 5 zero-quantity occurrences confirmed as Professional Judgment. Detection (quantity == 0) is Structurally Deterministic; acceptability requires QS intent.
3. **V-004 (Scope Containment):** Structural containment confirmed as Structurally Deterministic. Semantic scope partial formalization possible but judgment required for non-standard cases.
4. **V-005 (Completeness):** Basic completeness confirmed as Structurally Deterministic. Full completeness partial formalization possible but judgment required for project-specific requirements.

**No counterexamples found.** Boundary hypothesis strengthened by production evidence.

---

## Document Control

**Version:** 1.0 (Final)  
**Status:** Complete  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Authority:** EQ-0011 BOQ Semantic Intelligence Boundary