# BOQ Intelligence Increment 3 — Implementation Design Document

**Status:** Approved  
**Date:** 2026-07-14  
**Engineering Authority:** EQ-0010 + EQ-0011  
**Gate 2:** Approved  
**Increment:** BOQ Intelligence Increment 3 — Structural Detection Evidence

---

# Purpose

This document translates the frozen engineering evidence produced during EQ-0010 and EQ-0011 into an implementation plan for BOQ Intelligence Increment 3.

Its purpose is implementation planning only.

It is **not**:

* an architecture proposal
* a new engineering investigation
* a validation framework
* a semantic assessment engine

EQ-0010 and EQ-0011 are complete.

All engineering artifacts are frozen and serve as implementation authority.

Increment 3 records engineering evidence rather than validation status.

---

# Engineering Authority

Implementation shall be traceable to the following frozen artifacts.

* Engineering Governance v1.0
* EQ-0010 Investigation (Deterministic BOQ Structural Intelligence)
* EQ-0010 Capability Matrix v2.0
* EQ-0010 Spike 1–5 Evidence Reports
* EQ-0011 Investigation (BOQ Semantic Intelligence Boundary)
* EQ-0011 Capability Matrix v2.0
* EQ-0011 Spike 1–5 Evidence Reports
* BOQ Intelligence Increment 1 (Approved)
* BOQ Intelligence Increment 2 (Approved)

These artifacts shall **not** be modified.

---

# Scope

Increment 3 implements only the **Permitted** capabilities classified by EQ-0011 Spike 5.

Specifically:

1. Structural Detection Evidence: Level Skip
2. Structural Detection Evidence: Zero Quantity
3. Structural Detection Evidence: Structural Containment
4. Structural Detection Evidence: Basic Completeness
5. Structural Evidence Presentation

These capabilities shall operate purely over:

```
list[BOQRow] + Reconstructed Hierarchy (from Increment 2)
```

No parser modifications.

No runtime modifications.

No architecture modifications.

---

# Out of Scope

Increment 3 shall not implement:

* Skip legitimacy assessment (Professional Judgment — EQ-0011 FP-003)
* Zero-quantity acceptability assessment (Professional Judgment — EQ-0011 FP-003)
* Semantic scope containment (Contingent — requires new EQ per EQ-0011 FP-004)
* Full QS completeness validation (Contingent — requires new EQ per EQ-0011 FP-004)
* Any semantic assessment
* Any professional judgment automation
* Any 'should' conclusions
* Rule engine
* Scoring system
* Severity classification
* Recommendations
* AI reasoning

---

# Architecture Constraints

Implementation shall preserve Increment 1 and Increment 2 architecture.

Specifically:

* pure functions
* deterministic execution
* no parser changes
* no runtime changes
* no Observation Runtime
* no service layer
* no plugin architecture
* no manager classes
* no visitor pattern
* no factory abstractions
* no validation framework
* no assessment engine

YAGNI applies throughout implementation.

---

# Evidence Traceability Matrix

| Production Capability | Engineering Authority |
| --------------------- | --------------------- |
| Level skip detection | EQ-0010 Spike 4, EQ-0011 Spike 2 |
| Zero quantity detection | EQ-0010 Spike 1, EQ-0011 Spike 2 |
| Structural containment | EQ-0010 Spike 4, EQ-0011 Spike 3 |
| Basic completeness | EQ-0010 Spike 3, EQ-0011 Spike 3 |
| Evidence presentation | EQ-0011 Spike 4 |

Every production capability shall reference one or more approved engineering spikes.

---

# Reuse Analysis

Existing Increment 1 and Increment 2 data structures shall be reused wherever possible. New dataclasses require explicit Rule-of-Three justification.

Before introducing any new production module, function, or data structure, implementation shall evaluate:

* Can Increment 1 or Increment 2 already represent this?
* Can an existing production function be extended?
* Can BOQIntelligenceResult be extended?
* Can BOQRow be reused?
* Can BOQHeaderNode be reused?
* Would a new structure duplicate existing information?

No new production abstraction shall be introduced without explicit justification.

The Rule of Three remains in force.

---

# Production Module Plan

Implementation shall minimise architectural impact.

The implementation may:

* extend existing Increment 1 + Increment 2 production modules
* introduce helper functions within `boq_intelligence.py` if justified

Module placement shall be determined during implementation review.

The engineering investigation authorises capabilities, not filenames.

---

# Data Model Review

Structural detection evidence requires production representation of detected findings.

Evidence fields shall be added to `BOQIntelligenceResult` using names that describe observations:

* `detected_level_skips`
* `zero_quantity_items`
* `structural_containment_findings`
* `completeness_findings`

Avoid names like:

* violations
* failures
* errors
* invalid
* passed

These imply assessment rather than evidence.

Any new production type shall satisfy:

* justified by reuse analysis
* minimal surface area
* directly traceable to EQ-0010 or EQ-0011 evidence
* Rule of Three satisfied

---

# Forbidden Conclusions

Increment 3 shall never emit:

* Invalid
* Correct
* Incorrect
* Acceptable
* Legitimate
* Error
* Defect
* Should
* Must
* Non-compliant
* Warning
* Recommendation
* Risk
* Severity

Instead it emits observable facts.

**Example:**

✓ **Permitted:**

```
Level skip detected: Head1 (row 10) → Head3 (row 15), magnitude 2
```

✗ **Not Permitted:**

```
Invalid hierarchy at row 15
```

---

# Production Algorithms

Implement deterministic detection algorithms as investigated.

## Structural Detection Evidence: Level Skip

**Evidence:** EQ-0010 Spike 4, EQ-0011 Spike 2, EQ-0011 Spike 3

**Algorithm:**

1. Extract hierarchy from Increment 2 reconstruction.
2. For each parent-child header pair, compute level delta.
3. If delta > 1, record skip occurrence with location and magnitude.
4. Record observable facts only: row numbers, levels, magnitude.
5. Do not assess legitimacy.

## Structural Detection Evidence: Zero Quantity

**Evidence:** EQ-0010 Spike 1, EQ-0011 Spike 2, EQ-0011 Spike 3

**Algorithm:**

1. Filter rows where row_type == "Item".
2. For each Item, check if quantity == 0.0.
3. If zero, record occurrence with row context.
4. Record observable facts only: row number, description, section.
5. Do not assess acceptability.

## Structural Detection Evidence: Structural Containment

**Evidence:** EQ-0010 Spike 4, EQ-0011 Spike 3

**Algorithm:**

1. Extract hierarchy from Increment 2 reconstruction.
2. For each parent-child relationship, verify child_level <= parent_level.
3. If child_level > parent_level, record structural inversion.
4. Record observable facts only: row numbers, levels, relationship.
5. Do not perform semantic scope assessment.

Increment 3 verifies structural hierarchy relationships only. It does not determine semantic scope containment as defined by EQ-0011.

## Structural Detection Evidence: Basic Completeness

**Evidence:** EQ-0010 Spike 3, EQ-0011 Spike 3

**Algorithm:**

1. Group rows by section.
2. For each section, count Item rows.
3. If Item count == 0, record section with zero items.
4. Record observable facts only: section name, item count.
5. Do not assess project completeness.

## Evidence Presentation

**Evidence:** EQ-0011 Spike 4

**Algorithm:**

1. Collect all structural detection evidence.
2. Format as deterministic, reproducible evidence objects.
3. Present facts without interpretation.
4. No scoring, no severity, no recommendations.

Evidence presentation shall not alter, summarize, rank, merge, or interpret evidence.

No alternative detection algorithm shall be introduced.

No optimisation shall alter observable behaviour.

---

# Integration Plan

Increment 3 extends Increment 2.

It does not replace Increment 1 or Increment 2.

It does not duplicate Increment 1 or Increment 2.

Existing production functionality shall remain unchanged except where extended to expose approved Increment 3 capabilities.

`BOQIntelligenceResult` shall be extended with new evidence fields while preserving backward compatibility.

Increment 3 shall only add evidence. It shall never modify or reinterpret evidence produced by Increment 1 or Increment 2.

---

# Testing Strategy

Production tests shall be evidence-driven.

Every production test shall reference the engineering evidence it validates.

Examples include:

| Test | Evidence |
| ---- | -------- |
| Level skip detection determinism | EQ-0011 Spike 3 |
| Zero quantity detection | EQ-0011 Spike 3 |
| Structural containment detection | EQ-0011 Spike 3 |
| Basic completeness detection | EQ-0011 Spike 3 |
| Fixture verification | EQ-0011 Spike 3 |
| Backward compatibility | Increment 1, Increment 2 |
| No forbidden language | EQ-0011 Spike 4 |
| Forbidden language regression | EQ-0011 Spike 4 |

Testing shall follow Increment 1 and Increment 2 patterns.

---

# Documentation

Implementation documentation shall:

* reference EQ-0010 and EQ-0011
* reference relevant spike evidence
* explain deterministic behaviour
* explain production responsibilities
* clarify evidence vs assessment boundary

Frozen engineering artifacts shall not be modified.

---

# Acceptance Criteria

Implementation shall be accepted only if:

* ✓ deterministic
* ✓ all production tests pass
* ✓ no parser modifications
* ✓ no runtime modifications
* ✓ architecture unchanged
* ✓ pure functions over `list[BOQRow]` + hierarchy
* ✓ every production capability traceable to EQ-0010/EQ-0011 evidence
* ✓ no speculative functionality beyond investigated scope
* ✓ engineering boundary preserved — no implementation may convert evidence into semantic assessment or professional judgment
* ✓ backward compatible with Increment 1 and Increment 2
* ✓ Increment 1 and Increment 2 outputs remain bit-for-bit identical when Increment 3 evidence generation is disabled
* ✓ no forbidden language in outputs

If additional functionality is required beyond EQ-0010 and EQ-0011:

1. Pause implementation.
2. Register a new Engineering Question.
3. Collect engineering evidence.
4. Obtain Gate approval.
5. Resume implementation only after approval.

Future semantic capabilities shall follow the Engineering Question workflow established by EQ-0010 and EQ-0011.

---

# Non-Goals

Increment 3 shall not introduce:

* performance optimisation
* caching
* visualisation
* serialisation
* alternative detection algorithms
* semantic rules
* domain rule formalization
* assessment logic
* validation framework
* scoring system
* severity classification
* recommendation engine

These require separate engineering investigation if needed.

---

# Non-Goals Verification Checklist

Implementation review shall verify absence of:

- [ ] Semantic assessment
- [ ] Rule engine
- [ ] Scoring
- [ ] Severity
- [ ] Recommendations
- [ ] AI reasoning
- [ ] Architecture expansion
- [ ] Parser modification
- [ ] Runtime modification
- [ ] Validation status (vs evidence)
- [ ] Professional judgment automation
- [ ] Forbidden language

---

# Implementation Sequence

1. Perform reuse analysis.
2. Extend `BOQIntelligenceResult` with evidence fields.
3. Implement level skip detection.
4. Implement zero quantity detection.
5. Implement structural containment detection.
6. Implement basic completeness detection.
7. Implement evidence presentation.
8. Integrate with Increment 2.
9. Add production tests.
10. Verify determinism.
11. Verify backward compatibility.
12. Verify production fixtures.
13. Verify no forbidden language.
14. Update production documentation.
15. Obtain implementation review.

---

# Document Control

**Owner:** Project Owner

**Status:** Approved

**Authority:** Gate 2 Approved

**Approved:** 2026-07-14

**Next Step:** Production implementation authorized.