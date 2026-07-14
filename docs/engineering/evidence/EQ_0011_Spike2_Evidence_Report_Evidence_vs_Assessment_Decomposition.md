# EQ-0011 — Spike 2 — Evidence Report — Evidence vs Assessment Decomposition

**Date:** 2026-07-14  
**Status:** Complete  
**Investigation:** EQ-0011 BOQ Semantic Intelligence Boundary  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction

---

## Objective

For each of the four Domain Dependent capabilities (V-003, V-004, V-005, SEM-003), decompose into:
1. Deterministic evidence obtainable from BOQRow + reconstructed hierarchy
2. Assessment required beyond that evidence
3. Whether assessment could become semantically deterministic or remains professional judgment

This spike produces evidence only. No architecture, engines, or abstractions.

---

## Methodology

Analyzed each capability using:
- **Evidence Source:** EQ-0010 Spike results (frozen evidence)
- **Domain Source:** docs/domain/02_BOQ_Structure.md (domain rules)
- **Fixture Evidence:** Production data observations

Decomposed each capability into Evidence (what can be observed) vs Assessment (what must be judged).

---

## Outcome: Key Finding

**All 4 capabilities exhibit Evidence/Assessment separation:**
- **Evidence components:** All Structurally Deterministic (observable from BOQRow + hierarchy)
- **Assessment components:**
  - 2 capabilities could become Semantically Deterministic with formal rules (V-004, V-005)
  - 2 capabilities remain Professional Judgment (V-003, SEM-003)

---

## Capability Decompositions

### V-003: Level Progression Validation

#### Evidence Component

**Description:** Level skip detection — identify when child level > parent level + 1

**Data Source:** BOQRow.uom field + reconstructed hierarchy parent relationships

**Computation:**
```
For each header:
  1. Extract level from UOM (Head1→1, Head2→2, Head3→3, etc.)
  2. Compare child_level to parent_level
  3. Flag if (parent_level - child_level) > 1
```

**Example from Fixture:**
- Row 1661: Head3 under Head1 (skip = 2)
- Rows 5709-5745: 7× Head4 under Head2 (skip = 2)

**Traceability:** EQ-0010 Spike 5 detected 12 skip violations deterministically

**Classification:** **Structurally Deterministic**

#### Assessment Component

**Description:** Determine whether detected skip is legitimate organizational pattern or structural error

**Why Not Deterministic:**  
Domain rule states levels "should" progress sequentially but allows "additional subdivision as required by project complexity"

**Context Required:**
1. Project organizational requirements
2. Whether skip serves legitimate purpose
3. QS office standards for this project type

**Could Formalize?** No — requires judgment

**Formalization Prerequisite:**  
Would require:
1. Project-specific organizational rules
2. Client-specific hierarchy standards
3. Definition of "legitimate" for each context

These vary per project and cannot be pre-formalized.

**Traceability:** Domain Layer: "Hierarchy Level N: Additional subdivision levels as required by project complexity" — "as required" signals judgment

**Classification:** **Professional Judgment**

#### Boundary Statement

Evidence: Skip detection is Structurally Deterministic (gap computation over hierarchy).  
Assessment: Skip legitimacy requires Professional Judgment (project-specific context).

---

### SEM-003: Items Always Quantify

#### Evidence Component

**Description:** Zero-quantity detection — identify items where quantity field == 0

**Data Source:** BOQRow.quantity field for rows where row_type == 'Item'

**Computation:**
```
For each Item row:
  1. Check if quantity == 0.0
  2. Flag if true
```

**Example from Fixture:**
- Rows 5698, 6088, 6091, 6130, 6133: all have quantity = 0.0

**Traceability:** EQ-0010 Spike 5 detected 5 zero-quantity items deterministically

**Classification:** **Structurally Deterministic**

#### Assessment Component

**Description:** Determine whether zero quantity is data entry error, incomplete takeoff, or legitimate placeholder

**Why Not Deterministic:**  
Domain rule states items "always" quantify but zero-quantity items exist in production. Disposition depends on QS intent and project stage.

**Context Required:**
1. Whether item is placeholder for future measurement
2. Whether takeoff is complete
3. Whether zero is intentional (e.g., omission item)

**Could Formalize?** No — requires judgment

**Formalization Prerequisite:**  
Would require:
1. Project stage tracking (draft vs final)
2. QS intent capture (placeholder vs error)
3. Omission/addition context

These are project-state dependent and require QS interpretation.

**Traceability:** Domain Layer: "SEM-003: Items must have quantity and UOM" — production evidence shows 5 zero-quantity items; rule cannot be absolute without context

**Classification:** **Professional Judgment**

#### Boundary Statement

Evidence: Zero-quantity detection is Structurally Deterministic (field value comparison).  
Assessment: Zero-quantity acceptability requires Professional Judgment (QS intent and project state).

---

### V-004: Scope Containment

#### Evidence Component

**Description:** Parent-level consistency — verify child_level <= parent_level (structural containment)

**Data Source:** Reconstructed hierarchy with level assignments

**Computation:**
```
For each parent-child pair:
  1. Compare levels
  2. Flag if child_level > parent_level (structural inversion)
```

**Example from Fixture:**  
EQ-0010 Spike 5: 0 structural inversions detected (all parent-level relationships consistent)

**Traceability:** EQ-0010 Spike 5: Parent-level consistency classified as Derivable

**Classification:** **Structurally Deterministic** (already confirmed in EQ-0010)

#### Assessment Component

**Description:** Determine whether child work scope semantically fits within parent scope (semantic containment)

**Why Not Deterministic:**  
Structural containment ensures level consistency but not scope alignment. Requires understanding what each header represents, not just its level.

**Context Required:**
1. Semantic meaning of parent header
2. Semantic meaning of child header
3. Whether child scope is subset of parent scope

**Could Formalize?** Yes — with rules

**Formalization Prerequisite:**  
Would require:
1. Explicit scope definitions for standard headers (e.g., "SUBSTRUCTURE" contains foundation work)
2. Scope taxonomy (trade-based, location-based, element-based)
3. Containment rules (e.g., "Concrete Work" contains "Reinforcement")

These could be formalized as Semantic Rules for standard BOQ patterns.

**Caveat:** Non-standard organizational patterns still require judgment

**Traceability:** Domain Layer: "Hierarchy - Semantic Inheritance: Child elements inherit meaning from parents" — requires understanding meaning, not just observing structure

**Classification:** **Semantically Deterministic** (with formalized scope rules) or **Professional Judgment** (for non-standard structures)

#### Boundary Statement

Evidence: Parent-level consistency is Structurally Deterministic (already confirmed in EQ-0010).  
Assessment: Semantic scope containment could become Semantically Deterministic with formalized scope rules, otherwise requires Professional Judgment for non-standard structures.

---

### V-005: Completeness

#### Evidence Component

**Description:** Section-has-items — verify each section contains at least one measurable item

**Data Source:** BOQRow section field + row_type field

**Computation:**
```
Group rows by section
For each section:
  1. Count Item rows
  2. Flag if count == 0
```

**Example from Fixture:**  
EQ-0010 Spike 5: All sections contain at least one Item row (basic completeness satisfied)

**Traceability:** EQ-0010 Spike 5: Section-has-measurable-items classified as Derivable

**Classification:** **Structurally Deterministic** (already confirmed in EQ-0010)

#### Assessment Component

**Description:** Determine whether all required work for project scope is represented (full QS completeness)

**Why Not Deterministic:**  
Structural completeness (section has items) does not prove scope completeness (all required work present). Requires knowledge of project requirements.

**Context Required:**
1. Project scope and deliverables
2. Work breakdown structure requirements
3. Trade/element coverage expectations
4. Client-specific completeness criteria

**Could Formalize?** Yes — with rules

**Formalization Prerequisite:**  
Would require:
1. Project scope definition (deliverables, trades, elements)
2. Completeness checklist per project type
3. Required work packages mapped to BOQ structure

These could be formalized as Semantic Rules for standard project types, but vary per project and client.

**Caveat:** Project-specific requirements vary; formalization limited to standard project types

**Traceability:** Domain Layer: "Completeness: No missing work, all required measurable work represented" — "required work" is project-specific and cannot be determined from BOQ structure alone

**Classification:** **Semantically Deterministic** (for standard project types with defined scope) or **Professional Judgment** (for project-specific requirements)

#### Boundary Statement

Evidence: Section-has-items is Structurally Deterministic (already confirmed in EQ-0010).  
Assessment: Full completeness could become Semantically Deterministic with project scope definitions, otherwise requires Professional Judgment based on project knowledge.

---

## Formalization Analysis

### Potentially Formalizable (2 capabilities)

**V-004: Scope Containment (semantic)**
- Evidence: Parent-level consistency already deterministic
- Formalization Path: Define scope taxonomy + containment rules for standard BOQ patterns
- Prerequisite: Explicit scope definitions and containment mappings
- Caveat: Non-standard organizational patterns still require judgment
- Classification if Formalized: **Semantically Deterministic**

**V-005: Completeness (full QS)**
- Evidence: Section-has-items already deterministic
- Formalization Path: Define required work packages per project type
- Prerequisite: Project scope definition and completeness checklists
- Caveat: Project-specific requirements vary; formalization limited to standard project types
- Classification if Formalized: **Semantically Deterministic** (for standard projects)

### Not Formalizable (2 capabilities)

**V-003: Level Progression (skip legitimacy)**
- Evidence: Skip detection already deterministic
- Why Not Formalizable: Legitimacy depends on project-specific organizational decisions that vary per project and cannot be pre-defined
- Classification: **Professional Judgment**

**SEM-003: Items Always Quantify (zero acceptability)**
- Evidence: Zero-quantity detection already deterministic
- Why Not Formalizable: Acceptability depends on QS intent, project stage, and whether zero is error or placeholder — context-specific interpretation required
- Classification: **Professional Judgment**

---

## Summary

### Evidence Classification

All 4 evidence components: **Structurally Deterministic**

| Capability | Evidence | Data Source | Already Confirmed? |
|------------|----------|-------------|-------------------|
| V-003 | Skip detection | BOQRow.uom + hierarchy | Yes (EQ-0010 Spike 5) |
| SEM-003 | Zero-quantity detection | BOQRow.quantity | Yes (EQ-0010 Spike 5) |
| V-004 | Parent-level consistency | Hierarchy levels | Yes (EQ-0010 Spike 5) |
| V-005 | Section-has-items | BOQRow section + type | Yes (EQ-0010 Spike 5) |

### Assessment Classification

| Capability | Assessment | Classification |
|------------|------------|---------------|
| V-003 | Skip legitimacy | **Professional Judgment** |
| SEM-003 | Zero acceptability | **Professional Judgment** |
| V-004 | Semantic scope containment | **Semantically Deterministic** (with rules) or **Professional Judgment** |
| V-005 | Full completeness | **Semantically Deterministic** (with scope) or **Professional Judgment** |

### Key Distinction

**Evidence (what is) vs Assessment (what it means)**

- **Evidence** is always structural and deterministic
- **Assessment** requires either formalized semantic rules or professional judgment

This decomposition reveals the boundary:
- Structural facts can always be observed deterministically
- Interpreting those facts requires either explicit rules or human judgment

---

## Tool

**Spike Implementation:** `tools/eq0011_spike2_evidence_vs_assessment_decomposition.py`

**Results:** `data/reports/eq0011_spike2_results.json`

**Determinism:** Yes (decomposition is reproducible from EQ-0010 evidence)

---

## Spike 2 Conclusion

Evidence vs Assessment decomposition confirms:

1. **All evidence components are Structurally Deterministic** — observable from BOQRow + hierarchy
2. **Assessment components split into two categories:**
   - **2 capabilities potentially Semantically Deterministic** (V-004, V-005) — could be formalized with explicit rules
   - **2 capabilities remain Professional Judgment** (V-003, SEM-003) — context-dependent, cannot be pre-formalized

The boundary is clear: **structural observation** (evidence) is deterministic, but **interpretation of meaning** (assessment) requires either explicit semantic rules or professional judgment.

This finding establishes the foundation for Spike 3: examining production fixture evidence to test these boundary classifications.

---

## Document Control

**Version:** 1.0 (Final)  
**Status:** Complete  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Authority:** EQ-0011 BOQ Semantic Intelligence Boundary