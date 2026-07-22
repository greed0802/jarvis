# BOQ Intelligence Increment 2 — Implementation Design Document

**Status:** Approved
**Date:** 2026-07-14
**Engineering Authority:** EQ-0010 Deterministic BOQ Structural Intelligence
**Gate 2:** Approved
**Increment:** BOQ Intelligence Increment 2

---

# Purpose

This document translates the frozen engineering evidence produced during EQ-0010 into an implementation plan for BOQ Intelligence Increment 2.

Its purpose is implementation planning only.

It is **not**:

* an architecture proposal
* a new engineering investigation
* a capability discovery document

EQ-0010 is complete.

All engineering artifacts are frozen and serve as implementation authority.

---

# Engineering Authority

Implementation shall be traceable to the following frozen artifacts.

* Engineering Governance v1.0
* EQ-0010 Investigation
* EQ-0010 Capability Matrix v2.0
* Spike 1 Evidence Report
* Spike 2 Evidence Report
* Spike 3 Evidence Report
* Spike 4 Evidence Report
* Spike 5 Evidence Report

These artifacts shall **not** be modified.

---

# Scope

Increment 2 implements only capabilities that EQ-0010 classified as **Derivable**.

Specifically:

* hierarchy reconstruction
* hierarchy depth
* parent header identification
* heading tree structure
* items-per-header ratio

These capabilities shall operate purely over:

```
list[BOQRow]
```

No parser modifications.

No runtime modifications.

No architecture modifications.

---

# Out of Scope

Increment 2 shall not implement:

* Domain Dependent capabilities
* V-003
* semantic V-004
* semantic V-005
* SEM-003
* SEM-004
* SEM-005

These remain responsibilities of the Domain Knowledge Layer.

---

# Architecture Constraints

Implementation shall preserve Increment 1 architecture.

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

YAGNI applies throughout implementation.

---

# Evidence Traceability Matrix

| Production Capability  | Evidence Authority |
| ---------------------- | ------------------ |
| BOQRow observations    | Spike 1            |
| Head1–Head5 indicators | Spike 2            |
| Row sequence behaviour | Spike 3            |
| Empty header detection | Spike 3            |
| Heading statistics     | Spike 3            |
| Stack reconstruction   | Spike 4            |
| Hierarchy depth        | Spike 4            |
| Parent assignment      | Spike 4            |
| Heading tree           | Spike 4            |
| Domain boundaries      | Spike 5            |

Every production capability shall reference one or more approved engineering spikes.

---

# Reuse Analysis

Before introducing any new production module, function, or data structure, implementation shall evaluate:

* Can Increment 1 already represent this?
* Can an existing production function be extended?
* Can BOQIntelligenceResult be extended?
* Can BOQRow be reused?
* Would a new structure duplicate existing information?

No new production abstraction shall be introduced without explicit justification.

The Rule of Three remains in force.

---

# Production Module Plan

Implementation shall minimise architectural impact.

The implementation may:

* extend existing Increment 1 production modules
* introduce one additional production module if justified

Module placement shall be determined during implementation review.

The engineering investigation authorises capabilities, not filenames.

---

# Data Model Review

Hierarchy reconstruction requires a production representation of reconstructed hierarchy.

The exact implementation representation shall be determined after reuse analysis.

Possible approaches include:

* extending existing production models
* introducing one minimal hierarchy representation
* another equivalent implementation

The investigation requires a deterministic tree representation.

It does **not** mandate a specific dataclass.

Any new production type shall satisfy:

* justified by reuse analysis
* minimal surface area
* directly traceable to EQ-0010 evidence
* Rule of Three satisfied

---

# Algorithm

Implement the deterministic stack-based reconstruction algorithm exactly as investigated.

Evidence:

**EQ-0010 Spike 4**

**Section: Deterministic Stack-Based Reconstruction Algorithm**

Algorithm:

1. Extract numeric level from Head1–Head5.
2. Pop stack while top level is greater than or equal to current level.
3. If stack is non-empty, assign current header as child of stack top.
4. Otherwise create a root header.
5. Push current header.
6. Attach Item rows to the current stack top.

No alternative reconstruction algorithm shall be introduced.

No optimisation shall alter observable behaviour.

---

# Integration Plan

Increment 2 extends Increment 1.

It does not replace Increment 1.

It does not duplicate Increment 1.

Existing production functionality shall remain unchanged except where extended to expose approved Increment 2 capabilities.

---

# Testing Strategy

Production tests shall be evidence-driven.

Every production test shall reference the engineering evidence it validates.

Examples include:

| Test                       | Evidence |
| -------------------------- | -------- |
| Reconstruction determinism | Spike 4  |
| Parent assignment          | Spike 4  |
| Depth computation          | Spike 4  |
| Heading statistics         | Spike 3  |
| Empty header detection     | Spike 3  |
| Items-per-header ratio     | Spike 4  |
| Fixture verification       | Spike 4  |

Testing shall follow Increment 1 patterns.

---

# Documentation

Implementation documentation shall:

* reference EQ-0010
* reference relevant spike evidence
* explain deterministic behaviour
* explain production responsibilities

Frozen engineering artifacts shall not be modified.

---

# Acceptance Criteria

Implementation shall be accepted only if:

* deterministic
* all production tests pass
* no parser modifications
* no runtime modifications
* architecture unchanged
* pure functions over `list[BOQRow]`
* every production capability traceable to EQ-0010 evidence
* no speculative functionality beyond investigated scope

If additional functionality is required beyond EQ-0010:

1. Pause implementation.
2. Register a new Engineering Question.
3. Collect engineering evidence.
4. Obtain Gate approval.
5. Resume implementation only after approval.

---

# Non-Goals

Increment 2 shall not introduce:

* performance optimisation
* caching
* tree visualisation
* tree serialisation
* alternative hierarchy algorithms
* speculative validation rules
* additional architecture

These require separate engineering investigation if needed.

---

# Implementation Sequence

1. Perform reuse analysis.
2. Select minimal production representation.
3. Implement deterministic stack reconstruction.
4. Implement hierarchy statistics.
5. Integrate with Increment 1.
6. Add production tests.
7. Verify determinism.
8. Verify production fixtures.
9. Update production documentation.
10. Obtain implementation review.

---

# Document Control

**Owner:** Project Owner

**Status:** Approved

**Authority:** Gate 2 Approved

**Approved:** 2026-07-14

**Next Step:** Production implementation authorized.
