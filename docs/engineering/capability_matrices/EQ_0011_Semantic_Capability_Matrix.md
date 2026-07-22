# EQ-0011: Semantic Capability Matrix — Final State

**Engineering Question:** EQ-0011 BOQ Semantic Intelligence Boundary  
**Status:** Investigation Complete — All 5 Spikes Executed  
**Date Created:** 2026-07-14  
**Governance:** Engineering_Governance.md v1.0  
**Template:** Capability_Matrix_Template.md v1.0

---

## Purpose

This matrix tracks the discovery of semantic intelligence capabilities by investigating the boundary between deterministic structural evidence and professional QS judgment.

Each capability is classified using the Engineering Decision Classification as determined by evidence collected through the investigation spikes.

---

## Engineering Decision Classification

| Classification | Meaning |
|----------------|---------|
| **Structurally Deterministic** | Pure function over BOQRow + reconstructed hierarchy |
| **Semantically Deterministic** | Pure function once explicit domain rules have been formalized |
| **Professional Judgment** | Cannot currently be reduced to deterministic computation based on available evidence |

These are decision classes, not states. This taxonomy may be extended in future EQs.

---

## First Principle

**Engineering evidence is permitted to detect facts, but it is not permitted to infer professional intent unless that inference has been demonstrated to be deterministic.**

---

## Semantic Capability Matrix — Final State

### Validation Capabilities

| Candidate Engineering Capability | Struct | Semantic | Judgment | Consumer(s) | Evidence | Implementation |
|----------------------------------|--------|----------|----------|-------------|----------|---------------|
| Level progression validation (V-003) | ✓ | | ✓ | CheckMate | Spike 5: 12 skips confirmed Professional Judgment. Detection permitted, assessment not. | **Not Permitted** (FP-003) |
| Scope containment — semantic (V-004) | ✓ | ✓ | ✓ | CheckMate | Spike 5: Structural containment permitted. Semantic scope contingent on formal rules + new EQ. | **Contingent** (FP-004) |
| Completeness — full QS (V-005) | ✓ | ✓ | ✓ | CheckMate | Spike 5: Basic completeness permitted. Full completeness contingent on project scope + new EQ. | **Contingent** (FP-004) |
| Items always quantify (SEM-003) | ✓ | | ✓ | CheckMate | Spike 5: 5 zero-quantity items confirmed Professional Judgment. Detection permitted, assessment not. | **Not Permitted** (FP-003) |

### Detection Capabilities (Derived from Validation)

| Candidate Engineering Capability | Struct | Semantic | Judgment | Consumer(s) | Evidence | Implementation |
|----------------------------------|--------|----------|----------|-------------|----------|---------------|
| Level skip detection | ✓ | | | CheckMate | EQ-0010 Spike 5, EQ-0011 Spike 3: 12 skip occurrences detected deterministically | **Permitted** |
| Zero-quantity item detection | ✓ | | | CheckMate | EQ-0010 Spike 5, EQ-0011 Spike 3: 5 zero-quantity items detected deterministically | **Permitted** |
| Structural containment check | ✓ | | | CheckMate | EQ-0010 Spike 5, EQ-0011 Spike 3: 0 structural inversions; level consistency deterministic | **Permitted** |
| Basic completeness check | ✓ | | | CheckMate | EQ-0010 Spike 5, EQ-0011 Spike 3: All sections have Items; basic completeness deterministic | **Permitted** |

---

## Engineering Principles (P-001 through P-007)

| ID | Name | Statement |
|----|------|-----------|
| P-001 | Evidence Before Inference | Engineering evidence is permitted to detect facts, but is not permitted to infer professional intent unless demonstrated to be deterministic |
| P-002 | Structural Evidence Is Always Deterministic | Any observation from BOQRow fields or reconstructed hierarchy is structurally deterministic |
| P-003 | Detection vs Decision Separation | Every validation capability decomposes into detection (deterministic) and decision (rules/judgment) |
| P-004 | Judgment Terms Signal Boundary | 'Legitimate', 'acceptable', 'required' signal where determinism stops |
| P-005 | Professional Judgment Has Not Been Demonstrated Deterministic | V-003, SEM-003 remain with QS until contrary evidence |
| P-006 | Semantic Determinism Requires Explicit Rules | V-004, V-005 formalization requires new EQ |
| P-007 | Evidence Cannot Answer 'Should' Questions | Structure reveals what IS, not what SHOULD be |

---

## First Principles (FP-001 through FP-005)

| ID | Rule |
|----|------|
| FP-001 | Evidence before inference |
| FP-002 | Never conflate detection with decision |
| FP-003 | Do not automate Professional Judgment |
| FP-004 | Semantic determinism requires explicit rules + new EQ |
| FP-005 | Distinguish 'never' (deterministic) from 'should' (judgment) |

---

## Responsibility Boundaries

| Domain | Deterministic | Judgment |
|--------|---------------|----------|
| Row Classification | Classify row type from BOQRow field | N/A — fully deterministic |
| Structural Observation | Extract and present structural facts | N/A — fully deterministic |
| V-003 Level Progression | Detect skip magnitude and location | Determine legitimacy (QS) |
| SEM-003 Items Always Quantify | Detect items with quantity == 0.0 | Determine acceptability (QS) |
| V-004 Scope Containment | Verify child_level <= parent_level | Determine semantic scope alignment (rules/judgment) |
| V-005 Completeness | Verify section has measurable items | Determine all required work present (rules/judgment) |

---

## Investigation Summary

| State | Count | % |
|-------|-------|---|
| **Structurally Deterministic (permitted)** | **5** | **56%** |
| **Semantically Deterministic (contingent)** | **2** | **22%** |
| **Professional Judgment (not permitted)** | **2** | **22%** |
| **Total scoped** | **9** | **100%** |

---

## Increment 3 Scope Recommendation

### ✅ Permitted (5)
1. Level skip detection
2. Zero-quantity item detection
3. Structural containment check
4. Section-has-items basic completeness check
5. Structural evidence presentation

### ❓ Contingent (2 — require new EQ + formal rules)
1. Semantic scope containment (V-004)
2. Full QS completeness (V-005)

### ❌ Not Permitted (6)
1. V-003 skip legitimacy assessment
2. SEM-003 zero-quantity acceptability assessment
3. V-004 semantic scope without formal rules (FP-004)
4. V-005 full completeness without project scope (FP-004)
5. Any automated inference of professional intent (FP-001)
6. Any 'should' conclusion without formalized rules (FP-005)

---

## Update History

### 2026-07-14 — Spike 5 Final

**Status:** Investigation Complete

**Core Question Answered:**
*"Where is the engineering boundary between deterministic structural evidence and professional QS judgment?"*

**Answer:** The boundary is defined by 7 engineering principles (P-001 through P-007), 5 first principles (FP-001 through FP-005), and 6 responsibility boundaries. Detection is always Structurally Deterministic. Assessment is either Semantically Deterministic (with future formal rules via new EQ) or Professional Judgment (cannot be automated).

**Capability Transitions:**
- V-003: Unknown → Structurally Deterministic (evidence) + Professional Judgment (assessment)
- SEM-003: Unknown → Structurally Deterministic (evidence) + Professional Judgment (assessment)
- V-004: Unknown → Structurally Deterministic (evidence) + Semantically Deterministic (future, contingent)
- V-005: Unknown → Structurally Deterministic (evidence) + Semantically Deterministic (future, contingent)

**Investigation Conclusion:** Ready for Gate 2 review.

---

## Document Control

**Version:** 2.0 (Final)  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Status:** Investigation Complete