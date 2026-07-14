# EQ-0011 — Spike 4 — Evidence Report — Engineering Boundary Synthesis

**Date:** 2026-07-14  
**Status:** Complete  
**Investigation:** EQ-0011 BOQ Semantic Intelligence Boundary  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction — No Architecture Proposals

---

## Objective

Using the validated evidence collected in Spikes 1-3, synthesize the engineering principles that define the boundary between deterministic evidence and professional assessment.

This spike produces engineering findings only. It is not an implementation spike. It is not an architecture proposal.

---

## Inputs

- EQ-0010 frozen evidence (all 5 spikes)
- EQ-0011 Spike 1: Domain Vocabulary Discovery
- EQ-0011 Spike 2: Evidence vs Assessment Decomposition
- EQ-0011 Spike 3: Boundary Validation Against Production Evidence
- Domain Knowledge Layer: `docs/domain/02_BOQ_Structure.md`

---

## Outcome: Engineering Boundary Defined

The investigation has produced:
- **7 engineering principles** governing boundary
- **6 responsibility boundaries** for specific domains
- **5 first principles** for future implementation guidance
- **8 allowable conclusions** for engineering
- **5 prohibited conclusions** where engineering must stop

---

## Engineering Principles

### P-001: Evidence Before Inference
**Statement:** Engineering evidence is permitted to detect facts, but it is not permitted to infer professional intent unless that inference has been demonstrated to be deterministic.
**Evidence:** EQ-0011 First Principle (approved by Project Owner)  
**Applies to:** V-003, V-004, V-005, SEM-003

### P-002: Structural Evidence Is Always Deterministic
**Statement:** Any observation obtainable from BOQRow fields or reconstructed hierarchy is structurally deterministic. Row type, quantity value, UOM, section, parent-child relationships, hierarchy depth, and level progression gaps are always deterministically computable.
**Evidence:** EQ-0011 Spikes 1-3 — all evidence components confirmed Structurally Deterministic  
**Applies to:** All capabilities

### P-003: Detection vs Decision Separation
**Statement:** Every validation capability decomposes into detection (evidence) and decision (assessment). Detection is always structurally deterministic. The decision may be semantically deterministic (with formalized rules) or require professional judgment.
**Evidence:** EQ-0011 Spike 2 — Evidence vs Assessment Decomposition confirmed for all 4 capabilities  
**Applies to:** V-003, V-004, V-005, SEM-003

### P-004: Judgment Terms Signal Boundary
**Statement:** Domain vocabulary terms such as 'legitimate', 'acceptable', 'required', 'proper', and 'as needed' signal where deterministic computation stops and professional interpretation begins. Rules using 'never' (absolute prohibition) are structurally deterministic. Rules using 'should' or 'always' (normative expectation) require judgment about context and intent.
**Evidence:** EQ-0011 Spike 1 — vocabulary analysis identified boundary indicators  
**Applies to:** V-003, SEM-003, Domain rule definition

### P-005: Professional Judgment Has Not Been Demonstrated to be Deterministic
**Statement:** Current engineering evidence does not support deterministic formalization of V-003 or SEM-003. Engineering may provide evidence, flag conditions, and present context, but final assessment remains with the Quantity Surveyor until contrary evidence exists.
**Evidence:** EQ-0011 Spike 3 — 0 counterexamples found within the investigated production fixture; all 12 skips and 5 zero-quantity items require interpretation  
**Applies to:** V-003, SEM-003

### P-006: Semantic Determinism Requires Explicit Rules
**Statement:** Some assessments could become semantically deterministic if explicit domain rules are defined: (1) scope containment requires a formal scope taxonomy, (2) completeness requires project scope definitions. Without these rules, assessment remains Professional Judgment. Any future attempt to formalize these semantic rules requires its own Engineering Question and evidence package before implementation.
**Evidence:** EQ-0011 Spike 2 — V-004 and V-005 could be formalized with rules; Spike 3 — Medium confidence  
**Applies to:** V-004, V-005

### P-007: Evidence Cannot Answer 'Should' Questions
**Statement:** BOQ structure reveals what work IS present but not what work SHOULD be present. Completeness, scope alignment, and correctness are assessment questions that require project context beyond structural observation.
**Evidence:** EQ-0011 Spike 3 — structural evidence reveals facts, not intent; Spike 1 — vocabulary analysis  
**Applies to:** V-004, V-005

---

## Responsibility Boundaries

### Row Classification
| Dimension | Responsibility |
|-----------|---------------|
| **Deterministic** | Classify row type (Head, Item, Note, Section, Other) from BOQRow field |
| **Judgment** | N/A — fully deterministic |
| **Boundary Rule** | Row type is observable, not assessed |
| **Example** | Row with UOM 'Head1' → row_type='Head' |

### Structural Observation
| Dimension | Responsibility |
|-----------|---------------|
| **Deterministic** | Extract and present structural facts from BOQRow + hierarchy |
| **Judgment** | N/A — fully deterministic |
| **Boundary Rule** | Observation is always permitted; inference of meaning is not |
| **Example** | Skip detected: Head1 → Head3 (gap = 2) |

### Level Progression (V-003)
| Dimension | Responsibility |
|-----------|---------------|
| **Deterministic** | Detect and report level skip magnitude and location |
| **Judgment** | Determine whether skip is legitimate or violates project requirements |
| **Boundary Rule** | Engineering detects skips; QS determines legitimacy |
| **Example** | Engineering: 'Rows 5709-5745: Head4 under Head2 (skip=2)'. QS: 'This is acceptable due to work package structure.' |

### Zero Quantity (SEM-003)
| Dimension | Responsibility |
|-----------|---------------|
| **Deterministic** | Detect and report items with quantity == 0.0 |
| **Judgment** | Determine whether zero is error, placeholder, or intentional |
| **Boundary Rule** | Engineering detects zeros; QS determines acceptability |
| **Example** | Engineering: 'Row 5698: quantity=0.0'. QS: 'This is an omission placeholder — will be measured later.' |

### Scope Containment (V-004)
| Dimension | Responsibility |
|-----------|---------------|
| **Deterministic** | Verify child_level <= parent_level (structural containment) |
| **Judgment** | Determine whether child work scope fits within parent scope semantically |
| **Boundary Rule** | Engineering checks level consistency; QS assesses semantic alignment |
| **Example** | Engineering: 'Level 3 under Level 2: structurally valid'. QS: 'Concrete Work under Floor Finishes: scope mismatch.' |

### Completeness (V-005)
| Dimension | Responsibility |
|-----------|---------------|
| **Deterministic** | Verify each section contains at least one measurable item |
| **Judgment** | Determine whether all required work for project scope is represented |
| **Boundary Rule** | Engineering checks structure; QS determines scope coverage |
| **Example** | Engineering: 'Section 2.0 EXCAVATE AND FILL: 15 items present'. QS: 'Missing bulk excavation — only trench excavation shown.' |

---

## First Principles

### FP-001
**Engineering evidence is permitted to detect facts, but it is not permitted to infer professional intent unless that inference has been demonstrated to be deterministic.**

### FP-002
**Every validation capability decomposes into detection (structurally deterministic) and decision (requires rules or judgment). These must never be conflated in implementation.**

### FP-003
**Professional Judgment capabilities (V-003 skip legitimacy, SEM-003 zero acceptability) must not be automated. Engineering may detect and present evidence, but the decision belongs to the QS.**

### FP-004
**Semantically Deterministic capabilities (V-004 semantic scope, V-005 full completeness) may be implemented only after explicit domain rules are formalized. Without formal rules, they remain Professional Judgment.**

### FP-005
**'Never' rules are structurally deterministic. 'Should' and 'always' rules require judgment about context and intent. Implementation must distinguish between absolute prohibitions and normative expectations.**

---

## What Engineering May Conclude

Engineering may conclude based on structural evidence:

1. "Row 1661: skip detected (Head1→Head3, gap=2)"
2. "Row 5698: quantity = 0.0"
3. "All parent-child relationships satisfy structural containment"
4. "All sections have at least one measurable item"
5. "Section X has Row type distribution: Head=x, Item=y"
6. "Parent-level consistency is valid for all pairs"
7. "Zero-quantity items detected: {list of rows}"
8. "Level progression skips detected: {list of rows}"

---

## Where Engineering Must Stop

Engineering must stop before concluding:

1. "This skip is a mistake" — requires project context (Professional Judgment)
2. "This zero-quantity item is an error" — requires QS intent (Professional Judgment)
3. "This work package is out of scope" — requires project scope knowledge (Professional Judgment or Semantic Rules)
4. "This BOQ is incomplete" — requires project scope definition (Professional Judgment or Semantic Rules)
5. "The estimator made an error" — requires understanding of intent (Professional Judgment)

---

## Tool

**Spike Implementation:** `tools/eq0011_spike4_engineering_boundary_synthesis.py`  
**Results:** `data/reports/eq0011_spike4_results.json`

---

## Spike 4 Conclusion

The engineering boundary has been defined:

| Question | Answer |
|----------|--------|
| What is engineering permitted to conclude? | Structural facts (observations) only |
| Where must engineering stop? | Before inferring professional intent |
| What information may be represented as evidence? | Any BOQRow field or derived hierarchy property |
| What information requires assessment? | Legitimacy, acceptability, scope alignment, completeness |
| Which responsibilities belong to deterministic computation? | Detection of all structural facts |
| Which responsibilities belong to semantic rules? | V-004 scope containment, V-005 completeness (if formalized) |
| Which responsibilities remain professional judgment? | V-003 skip legitimacy, SEM-003 zero acceptability |

These findings are ready for Spike 5 (Capability Classification) and the Engineering Boundary Report.

---

## Document Control

**Version:** 1.0 (Final)  
**Status:** Complete  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Authority:** EQ-0011 BOQ Semantic Intelligence Boundary