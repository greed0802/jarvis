# EQ-0011 — Spike 1 — Evidence Report — Domain Vocabulary Discovery

**Date:** 2026-07-14  
**Status:** Complete  
**Investigation:** EQ-0011 BOQ Semantic Intelligence Boundary  
**Governance:** Engineering_Governance.md v1.0

---

## Objective

Extract and analyze domain vocabulary from BOQ Structure documentation to identify terminology that distinguishes between:
- Structural facts (deterministic)
- Semantic interpretation (requires domain rules)
- Professional judgment (requires QS expertise)

Map domain concepts to the Engineering Decision Classification taxonomy.

---

## Methodology

Analyzed `docs/domain/02_BOQ_Structure.md` to extract domain terms, classify them by decision type, and examine how the vocabulary itself reveals the boundary between deterministic computation and professional judgment.

---

## Outcome: Key Finding

**All four Domain Dependent capabilities exhibit a Detection/Decision split.**

- **Detection:** Structurally Deterministic (observable from BOQRow + hierarchy)
- **Decision:** Requires either Semantically Deterministic rules (if formalized) or Professional Judgment (if project-specific or contextual)

---

## Domain Vocabulary Analysis

### Structural Terms (5)

Terms observable from BOQRow + reconstructed hierarchy:

| Term | Definition | Examples | Related Capabilities |
|------|------------|----------|---------------------|
| **Hierarchy Level** | Position in nested structure | Head1, Head2, Head3, Head4, Head5 | V-003, V-004 |
| **Parent-Child Relationship** | Structural connection between header levels | Head2 under Head1, Head3 under Head2 | V-001, V-002, V-003 |
| **Measured Item** | A measurable quantity with description, UOM, and quantity | Plain concrete 20MPa: m³: 12.50 | SEM-003 |
| **Header** | Hierarchy element providing context without quantification | SUBSTRUCTURE, Strip Footings, Concrete Work | SEM-001, SEM-002 |
| **Section** | Top-level organizational unit (Hierarchy Level 1) | SUBSTRUCTURE, SUPERSTRUCTURE, FINISHES | SEM-001, V-005 |

**Classification:** These terms map directly to BOQRow fields or derived hierarchy structure. They represent observable facts.

### Semantic Terms (5)

Terms requiring understanding of meaning/intent:

| Term | Definition | Examples | Related Capabilities |
|------|------------|----------|---------------------|
| **Semantic Inheritance** | Child elements inherit meaning from all parents | Full item meaning = context + specification | SEM-004, SEM-005, V-004 |
| **Scope** | The work package or domain an element represents | Scope: SUBSTRUCTURE, Element: Strip Footings | V-004 |
| **Completeness** | No missing work, all required work represented | All foundation work items present | V-005 |
| **Context** | Semantic meaning provided by hierarchy structure | Headers provide context only | SEM-002, V-004 |
| **Logical Consistency** | BOQ structure remains meaningful and sound | Hierarchy follows logical decomposition | V-003, V-004 |

**Classification:** These terms require interpretation of what the structure *means*, not just what it *is*.

### Judgment Terms (5)

Terms requiring professional QS interpretation:

| Term | Definition | Examples | Related Capabilities |
|------|------------|----------|---------------------|
| **Legitimate** | Acceptable according to professional QS standards | Legitimate organizational pattern | V-003, SEM-003 |
| **Error** | Violation requiring correction | Data entry error, structural violation | V-003, SEM-003 |
| **Project Complexity** | Characteristics requiring deeper hierarchy | Additional subdivision as required | V-003, V-005 |
| **Required Work** | Work items mandated by project scope | All required work represented | V-005 |
| **Acceptable** | Meeting professional QS standards | Acceptable level progression | V-003, SEM-003 |

**Classification:** These terms explicitly signal that human judgment is required. They appear precisely where the domain rules become context-dependent.

### Mixed Terms (4)

Terms exhibiting both structural detection and semantic/judgment validation:

| Term | Definition | Detection Component | Validation Component | Capabilities |
|------|------------|---------------------|---------------------|--------------|
| **Level Progression** | Sequence of hierarchy levels | Detect skip: `parent_level - child_level > 1` | Determine if skip is legitimate | V-003 |
| **Orphan** | Item without proper hierarchical parent | Detect: No preceding Head | Determine if this violates domain rules | V-002, SEM-003 |
| **Quantify** | Assign numerical measurement value | Detect: `quantity == 0` | Determine if zero is acceptable | SEM-003 |
| **Containment** | Child elements fit within parent scope | Detect: `child_level <= parent_level` | Determine semantic scope alignment | V-004 |

**Classification:** These terms reveal the Detection/Decision architectural pattern. Each has a deterministic detection component and a judgment-based validation component.

---

## Verb Analysis

### Detection Verbs

Verbs indicating observation/measurement (deterministic operations):

```
detect, observe, identify, measure, count
extract, find, locate, determine, calculate
exists, present, absent, equal, matches
```

These verbs appear in structural descriptions and algorithmic specifications.

### Validation Verbs

Verbs indicating assessment/judgment (require interpretation):

```
validate, verify, check, confirm, ensure
must, should, require, prohibit, allow
acceptable, legitimate, correct, proper, sound
```

These verbs appear in domain rules and validation specifications.

**Finding:** The vocabulary itself distinguishes between "what can be computed" (detection verbs) and "what must be judged" (validation verbs).

---

## Rule Pattern Analysis

From domain documentation, validation rules follow patterns:

| Pattern | Examples | Deterministic? |
|---------|----------|----------------|
| **"never" + action** | Sections never measure, Headers never quantify | ✅ Yes (SEM-001, SEM-002) |
| **"always" + action** | Items always quantify | ❌ No — requires judging zero-quantity legitimacy (SEM-003) |
| **"must" + exist/have** | Parent must exist, Items must have preceding Head | ✅ Yes (V-001, V-002) |
| **"should" + follow** | Levels should progress sequentially | ❌ No — requires judging skip legitimacy (V-003) |
| **"fit within" + scope** | Child fits within parent scope | ⚠️ Mixed — structural containment yes, semantic no (V-004) |
| **"all" + required** | All required work represented | ❌ No — requires project scope knowledge (V-005) |

**Finding:** Rules using absolute prohibitions ("never") are deterministic. Rules using normative expectations ("should", "always", "all required") require judgment about context and intent.

---

## Boundary Indicators

Terms signaling that professional judgment is required:

```
legitimate, acceptable, proper
as required, project complexity
professional standards, QS judgment
domain knowledge, interpretation
understanding
```

**Finding:** These terms appear precisely at the deterministic/judgment boundary. Their presence in a domain rule signals that the rule cannot be fully automated without context-specific decisions.

---

## Capability-Specific Boundary Analysis

### V-003: Level Progression Validation

**Detection Vocabulary:**
- "level skip detected"
- "Head1 → Head3 (no Head2)"
- "`parent_level - child_level > 1`"

**Judgment Vocabulary:**
- "legitimate organizational pattern"
- "project complexity requires"
- "acceptable level skip"

**Boundary:**  
Detection is structural (observable). Validation requires judging if skip is legitimate for this project context.

### SEM-003: Items Always Quantify

**Detection Vocabulary:**
- "`quantity == 0`"
- "zero-quantity item"
- "measured item with no measurement"

**Judgment Vocabulary:**
- "legitimate placeholder"
- "data entry error"
- "incomplete takeoff"
- "acceptable zero quantity"

**Boundary:**  
Detection is structural (quantity field value). Validation requires judging whether zero is error or intentional placeholder.

### V-004: Scope Containment

**Detection Vocabulary:**
- "`child_level <= parent_level`"
- "structural parent-child relationship"
- "hierarchy level consistency"

**Judgment Vocabulary:**
- "semantic scope alignment"
- "work package containment"
- "project intent"
- "understanding header meaning"

**Boundary:**  
Structural containment is derivable (parent-level consistency). Semantic containment requires understanding what each header represents.

### V-005: Completeness

**Detection Vocabulary:**
- "section has measurable items"
- "at least one Item row"
- "non-empty section"

**Judgment Vocabulary:**
- "all required work represented"
- "no missing work"
- "project scope knowledge"
- "complete work package"

**Boundary:**  
Structural completeness is derivable (section has items). Full QS completeness requires knowing what work should be present.

---

## Detection vs Decision Pattern Emergence

The vocabulary analysis reveals a consistent architectural pattern:

```
Detection                    Decision
    ↓                            ↓
Observable Fact           Professional
(Structurally            Interpretation
Deterministic)                  ↓
                          (Judgment or
                        Semantic Rules)
```

**Examples:**

| Capability | Detection | Decision |
|-----------|-----------|----------|
| V-003 | Skip detected | Is skip legitimate? |
| SEM-003 | Zero quantity detected | Is zero acceptable? |
| V-004 | Parent-level consistent | Is semantic scope aligned? |
| V-005 | Section has items | Is all required work present? |

This pattern suggests a fundamental architectural separation between:
1. **Detection Engine** (Structurally Deterministic)
2. **Decision Engine** (Semantically Deterministic or Professional Judgment)

---

## Implications for Engineering Decision Classification

### Structurally Deterministic

Capabilities using only:
- Structural terms
- Detection verbs
- Observable facts from BOQRow + hierarchy

**Examples from this spike:**
- Parent existence (V-001) — already confirmed Derivable in EQ-0010
- Orphan detection (V-002) — already confirmed Derivable in EQ-0010
- Zero-quantity detection (derived from SEM-003)
- Level skip detection (derived from V-003)

### Semantically Deterministic

Capabilities requiring:
- Semantic terms
- Formalized domain rules
- Interpretation of meaning, but rules are explicit and deterministic

**Examples from this spike:**
- Scope containment *if* semantic scope rules are formalized (V-004)
- Completeness *if* required work is defined in project scope (V-005)

### Professional Judgment

Capabilities requiring:
- Judgment terms
- Validation verbs indicating assessment
- Boundary indicators
- Context-specific decisions that cannot be formalized

**Examples from this spike:**
- Level skip legitimacy (V-003)
- Zero-quantity acceptability (SEM-003)
- Semantic scope without formalized rules (V-004)
- Completeness without defined project scope (V-005)

---

## Evidence for Next Spikes

This vocabulary analysis establishes:

1. **Spike 2 Focus:** Decompose each capability into Detection (structural) vs Decision (semantic/judgment) components
2. **Spike 3 Evidence:** Apply vocabulary to production fixture evidence from EQ-0010
3. **Spike 4 Testing:** Test boundary by attempting to formalize judgment terms
4. **Spike 5 Classification:** Final classification using vocabulary-based criteria

---

## Tool

**Spike Implementation:** `tools/eq0011_spike1_domain_vocabulary_discovery.py`

**Results:** `data/reports/eq0011_spike1_results.json`

**Determinism:** Yes (vocabulary extraction is reproducible)

---

## Spike 1 Conclusion

Domain vocabulary analysis confirms that all four Domain Dependent capabilities exhibit a Detection/Decision split:

- **Detection components** are Structurally Deterministic
- **Decision components** require either Semantically Deterministic rules (if formalized) or Professional Judgment (if context-dependent)

The vocabulary itself reveals the boundary. Terms like "legitimate," "acceptable," "required," and "as needed" signal where deterministic computation stops and professional interpretation begins.

This finding establishes the foundation for Spike 2: decomposing each capability into its Detection and Decision components.

---

## Document Control

**Version:** 1.0 (Final)  
**Status:** Complete  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Authority:** EQ-0011 BOQ Semantic Intelligence Boundary