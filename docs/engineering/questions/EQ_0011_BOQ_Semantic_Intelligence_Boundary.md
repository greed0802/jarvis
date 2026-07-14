# EQ-0011: BOQ Semantic Intelligence Boundary

**Status:** Investigation Approved — Not Started  
**Date Created:** 2026-07-14  
**Governance:** Engineering_Governance.md v1.0  
**Owner:** Project Owner

---

## Core Engineering Question

**"Where is the engineering boundary between deterministic structural evidence and professional QS judgment, and how should that boundary define the scope of future validation capabilities?"**

This investigation does not ask: "Can these four rules be automated?"

This investigation asks: "Where does deterministic computation stop?"

---

## Investigation Context

### Background

EQ-0010 determined that deterministic structural intelligence is achievable from BOQRow data, producing:
- 8 Observable capabilities (directly available in BOQRow fields)
- 10 Derivable capabilities (deterministically computable via proven algorithms)
- 4 Domain Dependent capabilities (require Domain Knowledge Layer integration)

BOQ Intelligence Increment 2 successfully implemented the Derivable capabilities, specifically hierarchy reconstruction using the stack-based algorithm validated in EQ-0010 Spike 4.

### Current State

Production capabilities now available:
- BOQRow extraction (Increment 1)
- Row type classification (Increment 1)
- Hierarchy reconstruction (Increment 2)
- Structural statistics (Increment 2)

Four capabilities remain classified as "Domain Dependent":
1. **V-003:** Level Progression Validation
2. **V-004:** Scope Containment (semantic version)
3. **V-005:** Completeness (full QS version)
4. **SEM-003:** Items Always Quantify

### The Engineering Challenge

Unlike structural intelligence, these capabilities combine:
- Deterministic structure (from Increment 2)
- Reconstructed hierarchy (production-ready)
- QS domain knowledge (from Domain Layer)

The fundamental question: Which validations can be deterministic, and which always require professional judgment?

This boundary determines what Increment 3 is permitted to implement.

---

## First Principle

**Engineering evidence is permitted to detect facts, but it is not permitted to infer professional intent unless that inference has been demonstrated to be deterministic.**

## Evidence Admission Rule

A capability may only transition from Unknown when supported by one or more of:

1. Production fixture observations
2. Explicit Domain Knowledge documents
3. Published Quantity Surveying standards or specifications
4. Previously frozen engineering evidence

Engineering intuition, common practice, or undocumented professional experience are not sufficient evidence for capability classification.

### Examples

**Allowed:**
- `quantity == 0` (fact detection)
- `Head4 appears under Head2` (structural observation)

**Not automatically allowed:**
- "Therefore the estimator made a mistake" (requires evidence)

This principle will echo throughout every future validation engine.

---

## Engineering Decision Classification

This investigation will classify each capability using:

| Classification | Meaning |
|----------------|---------|
| **Structurally Deterministic** | Pure function over BOQRow + reconstructed hierarchy |
| **Semantically Deterministic** | Pure function once explicit domain rules have been formalized |
| **Professional Judgment** | Cannot currently be reduced to deterministic computation based on available evidence |

These are decision classes, not states. Future EQs may extend this taxonomy.

---

## Investigation Approach

### Boundary-First Methodology

```
Spike 1: Domain Vocabulary Discovery
         ↓
Spike 2: Structural vs Semantic Decomposition
         ↓
Spike 3: Evidence on Production Fixture
         ↓
Spike 4: Boundary Testing
         ↓
Spike 5: Capability Classification
```

The boundary is not discovered after everything — the boundary *is* the investigation.

### Detection vs Decision Architecture Pattern

A critical distinction this investigation must examine:

```
Detection              vs           Decision
   ↓                                   ↓
Evidence                          Professional
   ↓                              Interpretation
(Deterministic)                        ↓
                                  (Judgment?)
```

**Example:**
- **Detection:** `quantity == 0` → Structurally Deterministic
- **Decision:** "Is this acceptable?" → Professional Judgment

This architectural pattern could become fundamental to CheckMate's design.

---

## Investigation Subjects

The four Domain Dependent capabilities are **subjects** examined through the boundary lens, not isolated questions.

### V-003: Level Progression Validation

**EQ-0010 Evidence:**
- 12 skip violations detected in production fixture
- Patterns: Head1→Head3, Head2→Head4
- Spike 5 classified as "Domain Dependent"

**Questions:**
- Are level skips always errors?
- Can legitimate organizational patterns skip levels?
- Is there a deterministic rule for when skips are valid?
- Or does every skip require QS judgment?

### V-004: Scope Containment

**EQ-0010 Evidence:**
- Parent-level consistency is Derivable (already confirmed)
- Semantic scope requires understanding what each header represents
- Spike 5 classified semantic version as "Domain Dependent"

**Questions:**
- Beyond parent-level consistency, what is semantic scope?
- Can scope violations be detected deterministically?
- Or does scope require understanding project intent?

### V-005: Completeness

**EQ-0010 Evidence:**
- Section-has-measurable-items is Derivable (already confirmed)
- Full QS completeness requires project scope knowledge
- Spike 5 classified full version as "Domain Dependent"

**Questions:**
- Beyond "section has items," what is QS completeness?
- Can missing work be detected deterministically?
- Or does completeness require project knowledge?

### SEM-003: Items Always Quantify

**EQ-0010 Evidence:**
- 5 zero-quantity items detected in production fixture
- Rows: 5698, 6088, 6091, 6130, 6133
- Spike 5 classified as "Domain Dependent"

**Questions:**
- Are zero-quantity items ever legitimate?
- Can we distinguish errors from placeholders deterministically?
- Or does disposition require QS interpretation?

---

## Expected Deliverables

1. **EQ-0011 Engineering Question** (this document)
2. **Semantic Capability Matrix** (using Engineering Decision Classification)
3. **Five Evidence Reports** (boundary-focused, not capability-focused)
4. **Engineering Boundary Report** (deterministic vs judgment boundary definition)
5. **Detection vs Decision Architectural Pattern** (reusable for future validation)
6. **Recommendation for Increment 3 Scope** (exactly what is allowed to be implemented)

The sixth deliverable makes this investigation actionable.

---

## Explicit Non-Goal

**This investigation does not attempt to convert professional Quantity Surveyor judgment into deterministic rules.**

This protects against overconfident automation drift.

---

## Success Criteria

### Gate 1 (Investigation Planning) — ✅ COMPLETE

Investigation plan approved by Project Owner.

### Gate 2 (Investigation Complete)

- All 5 spikes executed
- All evidence reports frozen
- Semantic Capability Matrix v1.0 complete
- Engineering Boundary Report complete
- Detection vs Decision pattern documented
- Increment 3 scope recommendation documented
- Project Owner approval obtained

### Gate 3 (Implementation Authorization)

Separate gate. Implementation requires:
- Gate 2 complete
- Implementation design approved
- Architecture impact assessed
- Project Owner authorization

---

## Long-Term Roadmap Context

```
EQ-0010: Structural Intelligence (Complete)
    ↓
Increment 2: Hierarchy Reconstruction (Complete)
    ↓
EQ-0011: Semantic Intelligence Boundary ← Investigation phase
    ↓
Increment 3: Semantic Detection Engine (not validation)
    ↓
EQ-0012: Cross-document Intelligence
    ↓
Increment 4: CheckMate Validation Engine
```

**Critical distinction:** Increment 3 will build **detection**, not **validation**.

Validation comes later, after understanding what can and cannot be decided algorithmically.

---

## Emerging Engineering Methodology

This investigation continues the evolution from:

```
Parser → Formatter → QA
```

To:

```
Evidence → Capability → Implementation → Validation
```

The governance framework (Capability Discovery → Evaluation → EQ → Implementation) has become a reusable engineering discipline applicable beyond BOQ intelligence.

---

## Investigation Timeline

**Target Duration:** 5 spikes, evidence-driven progression

**Estimated Timeline:**
- Spike 1: Domain Vocabulary Discovery
- Spike 2: Structural vs Semantic Decomposition  
- Spike 3: Evidence on Production Fixture
- Spike 4: Boundary Testing
- Spike 5: Capability Classification

Each spike produces frozen evidence before the next begins.

---

## Authority and Approval

**Investigation Authority:** Engineering_Governance.md v1.0

**Gate 1 Approval:** Project Owner (2026-07-14)

**Gate 2 Approval:** Pending investigation completion

**Gate 3 Authorization:** Separate authorization required for implementation

---

## Document Control

**Version:** 1.0  
**Status:** Investigation Approved — Not Started  
**Last Updated:** 2026-07-14  
**Owner:** Project Owner  
**Next Review:** Upon investigation completion