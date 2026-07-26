# BOQ Consumer Boundaries

## EQ-0020 — BOQ Intelligence Consumer Architecture

### Spike 3 — Consumer Boundaries

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020 Spike 3

---

## 1. Purpose

Determine architectural boundaries for BOQ Intelligence consumers. Investigate:

- Who owns interpretation?
- Who owns presentation?
- Who owns validation?
- Who owns recommendations?
- Who owns assessment?

---

## 2. Boundary Principles

### 2.1 EQ-0011 Engineering Boundary

The EQ-0011 boundary is the foundational constraint for all consumer architecture:

```
Detection              vs           Decision
   ↓                                   ↓
Evidence                          Professional
   ↓                              Interpretation
(Deterministic)                        ↓
                                   (Judgment?)
```

**Evidence is permitted to detect facts, but it is not permitted to infer professional intent unless that inference has been demonstrated to be deterministic.**

### 2.2 Architecture Boundary Principles

1. **Production and interpretation are strictly separated.** The producer generates evidence; consumers interpret it.
2. **Validation is a separate consumer tier.** The Validation Engine evaluates evidence against rules; it does not interpret findings.
3. **Recommendations and assessments belong to consumers, not engines.** No engine may produce recommendations or assessments.
4. **Each component has exclusive ownership.** No responsibility overlap between producer, engine, and consumers.
5. **The Evidence Contract is the sole integration surface.** No consumer may access producer internals.

---

## 3. Boundary Analysis

### 3.1 Who Owns Interpretation?

**Answer:** Consumers own interpretation.

| Component | Owns Interpretation? | Evidence |
|-----------|----------------------|----------|
| BOQ Intelligence | ✗ | Producer only; does not interpret |
| Validation Engine | ✗ | Produces findings, not interpretations |
| CheckMate | ✓ | Applies application-specific meaning to findings |
| Formatter | ✓ | Interprets evidence for output rendering |
| Builder | ✓ | Interprets findings for CI/CD gates |
| O&A | ✓ | Interprets evidence for O&A analysis |
| Reporting | ✓ | Interprets evidence for summary reports |

**Interpretation Boundary:**
- The Validation Engine produces deterministic findings (facts).
- Consumers apply interpretation to findings (meaning).
- Example: V-014 produces "3 level skips detected" (finding). CheckMate interprets this as "review level 2→4 skips" (interpretation).

### 3.2 Who Owns Presentation?

**Answer:** Consumers own presentation.

| Component | Owns Presentation? | Evidence |
|-----------|---------------------|----------|
| BOQ Intelligence | ✗ | Produces evidence, not presentation |
| Validation Engine | ✗ | Produces findings, not presentation |
| CheckMate | ✓ | Owns UI presentation |
| Formatter | ✓ | Owns output format rendering |
| Builder | ✓ | Owns machine-readable output |
| O&A | ✓ | Owns O&A-specific presentation |
| Reporting | ✓ | Owns report formatting |

**Presentation Boundary:**
- No engine produces presentation.
- Each consumer owns its own presentation layer.
- The Evidence Contract and Validation Findings Contract define data structures, not presentation.

### 3.3 Who Owns Validation?

**Answer:** The Validation Engine owns validation.

| Component | Owns Validation? | Evidence |
|-----------|-------------------|----------|
| BOQ Intelligence | ✗ | Produces evidence, not validation |
| Validation Engine | ✓ | Owns rule evaluation and finding production |
| CheckMate | ✗ | Consumes findings; does not validate |
| Formatter | ✗ | Consumes findings; does not validate |
| Builder | ✗ | Consumes findings; does not validate |
| O&A | ✗ | Consumes findings; does not validate |
| Reporting | ✗ | Consumes findings; does not validate |

**Validation Boundary:**
- The Validation Engine is the sole owner of validation logic.
- Consumers consume findings; they do not re-implement validation.
- Validation rules are governed by the Validation Rule Registry.
- The Validation Findings Contract is the sole output surface.

### 3.4 Who Owns Recommendations?

**Answer:** No engine owns recommendations. Recommendations belong to human decision-makers, mediated by consumers.

| Component | Owns Recommendations? | Evidence |
|-----------|-----------------------|----------|
| BOQ Intelligence | ✗ | Evidence only; no recommendations |
| Validation Engine | ✗ | Findings only; no recommendations (SI-FR-08) |
| CheckMate | ✗ (human-mediated) | Presents findings; human makes recommendations |
| Formatter | ✗ | Renders findings; no recommendations |
| Builder | ✗ | Gates on findings; no recommendations |
| O&A | ✗ | Presents findings; human makes recommendations |
| Reporting | ✗ | Reports findings; no recommendations |

**Recommendation Boundary:**
- The Validation Findings Contract explicitly prohibits recommendations (SI-FR-08).
- Consumers may present findings that enable human recommendations.
- No automated recommendation is produced by any engine.

### 3.5 Who Owns Assessment?

**Answer:** No engine owns assessment. Assessment belongs to human decision-makers, mediated by consumers.

| Component | Owns Assessment? | Evidence |
|-----------|-------------------|----------|
| BOQ Intelligence | ✗ | Evidence only; no assessment |
| Validation Engine | ✗ | Findings only; no assessment (SI-FR-09) |
| CheckMate | ✗ (human-mediated) | Presents findings; human assesses |
| Formatter | ✗ | Renders findings; no assessment |
| Builder | ✗ | Gates on findings; no assessment |
| O&A | ✗ | Presents findings; human assesses |
| Reporting | ✗ | Reports findings; no assessment |

**Assessment Boundary:**
- The Validation Findings Contract explicitly prohibits assessments (SI-FR-09).
- Consumers may present findings that enable human assessment.
- No automated assessment is produced by any engine.

---

## 4. Consumer Boundary Matrix

### 4.1 Responsibility Ownership by Component

| Responsibility | Owner | Contract Authority |
|----------------|-------|-------------------|
| Evidence production | BOQ Intelligence | Evidence Contract v1.1.0 |
| Evidence specification | Evidence Contract | Evidence Contract v1.1.0 |
| Evidence consumption | All consumers | Evidence Contract v1.1.0 |
| Evidence interpretation | Consumers | Evidence Contract v1.1.0 |
| Evidence presentation | Consumers | Consumer-specific |
| Validation rule logic | Validation Engine | Validation Rule Registry |
| Finding production | Validation Engine | Validation Findings Contract v1.0.0 |
| Finding consumption | Consumers | Validation Findings Contract v1.0.0 |
| Finding interpretation | Consumers | Validation Findings Contract v1.0.0 |
| Finding presentation | Consumers | Consumer-specific |
| Recommendations | Human (via consumers) | None (prohibited in contracts) |
| Assessment | Human (via consumers) | None (prohibited in contracts) |

### 4.2 No Boundary Overlap

| Component | Produces Evidence | Consumes Evidence | Produces Findings | Consumes Findings | Interprets | Presents | Recommends | Assesses |
|-----------|-------------------|-------------------|-------------------|-------------------|------------|----------|------------|----------|
| BOQ Intelligence | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Validation Engine | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| CheckMate | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ (human) | ✗ (human) |
| Formatter | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| Builder | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| O&A | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ (human) | ✗ (human) |
| Reporting | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |

---

## 5. Boundary Enforcement

### 5.1 Contract-Level Enforcement

| Contract | Boundary Enforced | Mechanism |
|----------|-------------------|-----------|
| Evidence Contract v1.1.0 | Evidence immutability | Frozen dataclass (`frozen=True`) |
| Evidence Contract v1.1.0 | Evidence/Assessment boundary | G-10: EQ-0011 boundary preserved |
| Evidence Contract v1.1.0 | Evidence determinism | G-11: Same input → same output |
| Evidence Contract v1.1.0 | No internal access | G-14–G-16: Stable import paths only |
| Validation Findings Contract v1.0.0 | No recommendations | SI-FR-08: No recommendation text |
| Validation Findings Contract v1.0.0 | No assessments | SI-FR-09: No quality assessments |
| Validation Findings Contract v1.0.0 | No consumer-specific fields | SI-FR-10: No CheckMate/Formatter/etc. fields |
| Validation Findings Contract v1.0.0 | Consumer independence | §10: Compliance verification |

### 5.2 Implementation-Level Enforcement

| Boundary | Enforcement Mechanism |
|----------|----------------------|
| No internal imports | Consumers must not import `_`-prefixed symbols |
| No parser dependency | Consumers must not import `WorkbookParser` |
| No extraction dependency | Consumers must not import `boq_extraction._*` |
| Evidence immutability | `BOQIntelligenceResult` is `frozen=True` |
| Finding immutability | `ValidationFinding` and `ValidationFindings` are `frozen=True` |
| No assessment/recommendation | Validation rules classified as Observation/Detection only |

### 5.3 Verification-Level Enforcement

| Boundary | Verification Mechanism |
|----------|----------------------|
| Consumer independence | Architecture Consistency Gate (EQ-0013 Spike 3) |
| Boundary preservation | EQ-0011 boundary verification in Validation Engine |
| No consumer-specific logic | Code review: no CheckMate/Formatter/Builder/O&A/Reporting references in engine |
| Contract compliance | Contract verification tools |

---

## 6. Boundary Violation Handling

### 6.1 Violation Detection

If a boundary violation is detected:

1. **Identify the violation** — Which boundary was crossed?
2. **Classify the violation** — Assessment, Recommendation, or Coupling?
3. **Trace to source** — Which component introduced the violation?
4. **File Engineering Question** — Document the violation and proposed resolution.
5. **Project Owner decision** — Approve resolution or reject.

### 6.2 Violation Categories

| Category | Example | Resolution |
|----------|---------|------------|
| Assessment violation | Engine produces "BOQ quality is poor" | Remove assessment; produce finding only |
| Recommendation violation | Engine produces "fix this row" | Remove recommendation; produce finding only |
| Coupling violation | Consumer imports `_internal_function` | Remove import; use contract path only |
| Ownership violation | Consumer modifies evidence | Enforce immutability; use frozen dataclass |

---

## 7. Deliverable

This document is the **Boundary Analysis** deliverable for EQ-0020 Spike 3.

---

## 8. Document Control

| Property | Value |
|----------|-------|
| **Document ID** | EQ-0020-S3-CONSUMER-BOUNDARIES |
| **EQ** | EQ-0020 |
| **Spike** | 3 |
| **Status** | Complete |
| **Date** | 2026-07-25 |
| **Owner** | Project Owner |
| **Authority** | EQ-0020 (BOQ Intelligence Consumer Architecture) |
| **References** | BOQ_Intelligence_Public_Evidence_Contract_v1.1.md, Validation_Findings_Contract_v1.0.md, EQ-0011 (Boundary), EQ-0013 Spike 3 (Engine Scope) |

---

**End of Consumer Boundaries**
