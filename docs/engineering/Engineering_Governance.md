# Engineering Governance

**Status:** Accepted  
**Version:** 1.0  
**Date:** 2026-07-14  
**Owner:** Project Owner

---

## Purpose

This document establishes the methodology for engineering investigations in the Jarvis repository.

It defines:
- Engineering Question lifecycle
- Capability Matrix lifecycle
- Evidence collection process
- Artifact ownership and mutability
- Investigation chronology
- Approval gates

All Engineering Questions follow this governance unless explicitly approved otherwise by the Project Owner.

---

## Scope

This governance applies to:
- All Engineering Questions (EQ-0010 and beyond)
- Capability discovery investigations
- Evidence collection and validation
- Production recommendations
- Historical engineering preservation

---

## Engineering Investigation Lifecycle

```
1. Engineering Question (Specification)
   ↓
2. Project Owner Approval
   ↓
3. Capability Matrix (Initial state: mostly Unknown)
   ↓
4. Investigation Spikes (Evidence collection)
   ↓
5. Capability Matrix Updates (Evidence-based state transitions)
   ↓
6. Evidence Report (Findings, conclusions, recommendation)
   ↓
7. Project Owner Disposition
   ↓
8. Implementation (if approved)
```

---

## Artifact Definitions

### Engineering Question

**Purpose:** Investigation specification

**Answers:**
- Why are we investigating?
- What are we trying to prove?
- What evidence is required?
- When is the investigation complete?

**Mutable:** No (after Project Owner approval)

**Contains:**
- Problem Statement
- Research Question
- Scope and Non-Goals
- Investigation Plan
- Candidate Engineering Capabilities (initial list)
- Consumer Analysis
- Architecture Impact
- Success Criteria
- Exit Criteria
- Decision Framework

**Does NOT Contain:**
- Investigation results
- Evidence findings
- Production recommendations (these belong in Evidence Report)

---

### Capability Matrix

**Purpose:** Investigation state tracking

**Answers:**
- What has been observed?
- What has been derived?
- What requires Domain Knowledge?
- What remains unknown?
- What evidence supports each classification?

**Mutable:** Yes (during investigation)

**Usage:** A Capability Matrix is the preferred artifact when an investigation seeks to classify engineering capabilities. While commonly used with Engineering Questions, Capability Matrices may also be applied to other investigations (performance studies, parser benchmarks, regression analyses, fixture comparisons).

**Lifecycle:**
1. Created with initial state (most capabilities "Unknown")
2. Updated after each investigation spike
3. Timeline preserved (document evolution tracked)
4. Investigation concludes when all capabilities are either classified or explicitly deferred with documented justification

**Five-State Classification Model:**

Engineering Governance v1.0 adopts the Five-State Capability Classification Model. Future governance revisions may extend or refine this model where justified by production evidence.

| State | Meaning |
|-------|---------|
| **Observable** | Directly available in data structure fields |
| **Derivable** | Deterministically computable from available data |
| **Domain Dependent** | Requires Domain Knowledge Layer validation |
| **Not Determinable** | Cannot be determined from current data structure |
| **Unknown** | Evidence not yet collected |

**Matrix Format:**

| Candidate Engineering Capability | Obs | Der | Domain | Not Det | Unk | Consumer(s) | Evidence |
|----------------------------------|-----|-----|--------|---------|-----|-------------|----------|
| Example capability | ✓ | | | | | Consumer | Source |

**Update Requirements:**
- Document what changed (capability state transitions)
- Document what evidence was collected
- Document which spike produced the evidence
- Document when the update occurred

---

### Investigation Spikes

**Purpose:** Collect production evidence through focused investigation activities

**Characteristics:**
- Small, focused investigations
- Deterministic execution
- Reproducible results
- Evidence-based conclusions

**Investigation Structure:**
Investigations consist of one or more evidence collection activities ("spikes") defined by the Engineering Question. The number and scope of spikes is determined by the investigation requirements, not prescribed by governance.

**Output:**
- Spike evidence files (in `docs/engineering/evidence/`)
- Updated Capability Matrix
- Supporting data or analysis

**Not Permitted:**
- Heuristic approaches
- Speculative conclusions
- Implementation code
- Architecture proposals without evidence

---

### Evidence Report

**Purpose:** Summarize investigation findings and recommend disposition

**Answers:**
- What did the investigation discover?
- What evidence supports the conclusions?
- What should be implemented?

**Mutable:** No (once published, only factual corrections permitted)

**Created:** After investigation spikes complete

**Contains:**
1. Investigation Summary
2. Spikes Executed (with brief outcomes)
3. Final Capability Matrix State (reference)
4. Findings (what was observed and derived)
5. Conclusions (what the evidence demonstrates)
6. Production Recommendation (smallest meaningful implementation)

**Traceability Requirement:**
Every finding must include traceability: Finding → Evidence → Fixture → Spike → Capability Matrix update. This ensures all conclusions trace back to production evidence.

**Authority:** Evidence Reports provide the justification for production recommendations but do not authorize implementation. Project Owner Disposition is required.

**Possible Investigation Outcomes:**
- Capability promoted (Observable, Derivable, Domain Dependent)
- Capability deferred (Unknown with documented justification)
- Capability rejected (Not Determinable with evidence)
- Investigation inconclusive (insufficient evidence, alternative approach needed)

---

## Chronological Separation

### Planning Phase

**Activities:**
- Engineering Question created
- Capability Matrix initialized (mostly Unknown)
- Investigation plan defined
- Approval requested

**No Recommendations Made:** The EQ ends with a decision framework, not a recommendation.

### Investigation Phase

**Activities:**
- Spikes executed
- Evidence collected
- Capability Matrix updated
- Observations documented

**Recommendations Deferred:** Evidence accumulates but no disposition recommended yet.

### Conclusion Phase

**Activities:**
- Evidence Report written
- Findings documented
- Recommendation made based on evidence
- Project Owner disposition requested

**Authority Required:** Implementation requires explicit Project Owner approval.

---

## Artifact Ownership and Mutability

| Artifact | Mutable? | Purpose | Created |
|----------|----------|---------|---------|
| **Engineering Question** | No (after approval) | Investigation specification | Planning phase |
| **Capability Matrix** | Yes (during investigation) | Investigation state tracking | Planning phase |
| **Spike Evidence** | No | Individual investigation results | During investigation |
| **Evidence Report** | No (except factual corrections) | Summarizes findings, recommends disposition | After investigation |
| **ADR** | No (except factual corrections) | Records architectural decisions | When needed |

---

## Five-State Capability Model

Engineering capabilities are classified into one of five states based on production evidence.

### Observable

**Definition:** Directly available in data structure fields.

**Example:** `row_type` field in BOQRow

**Evidence Required:** Field existence in data structure

**Consumer Impact:** Can be read directly, exported, reported

---

### Derivable

**Definition:** Deterministically computable from available data.

**Example:** Row type transitions (computed from adjacent row types)

**Evidence Required:** Deterministic algorithm + production verification

**Consumer Impact:** Can be computed on demand, cached if needed

---

### Domain Dependent

**Definition:** Requires Domain Knowledge Layer validation to determine correctness.

**Example:** Trade assignment validity (requires office trade schedule)

**Evidence Required:** Mapping to specific Domain Knowledge document

**Consumer Impact:** Validation requires domain rules integration

---

### Not Determinable

**Definition:** Cannot be determined from current data structure.

**Example:** Engineering intent (requires human judgment)

**Evidence Required:** Demonstration that data structure lacks necessary information or that current evidence is insufficient

**Consumer Impact:** Explicitly out of scope for automated analysis

**Note:** This classification indicates current limitations, not permanent impossibility. Future data structures or evidence may enable determination.

---

### Unknown

**Definition:** Evidence not yet collected.

**Example:** Hierarchy depth (before investigation spike)

**Evidence Required:** None (investigation pending)

**Consumer Impact:** Cannot be used until evidence collected and state determined

**Transitions:** Unknown capabilities move to Observable/Derivable/Domain/Not Determinable after investigation, or remain Unknown with documented deferral justification.

---

## Investigation Approval Gates

### Gate 1: Investigation Authorization

**Before:** Engineering Question created  
**After:** Investigation spikes may begin

**Approval Required:** Project Owner

**Criteria:**
- Problem statement clear and justified
- Investigation plan feasible
- Capability Matrix initialized
- Success criteria defined

---

### Gate 2: Implementation Authorization

**Before:** Evidence Report published  
**After:** Production implementation may begin

**Approval Required:** Project Owner

**Criteria:**
- Investigation complete (exit criteria met)
- Evidence collected and documented
- Recommendation justified by evidence
- Architecture impact assessed

---

## Capability Classification

A capability moves from Unknown to an evidenced state when:

1. **Observable:** Data structure inspection confirms field exists
2. **Derivable:** Algorithm proven deterministic + verified against production fixture
3. **Domain Dependent:** Mapped to specific Domain Knowledge document
4. **Not Determinable:** Investigation demonstrates required information unavailable or evidence insufficient

A capability may remain **Unknown** with documented justification when:
- Evidence collection is deferred to a future investigation
- Current investigation scope does not include this capability
- Dependencies prevent classification at this time

**Evidence Standard:** Production verification against registered fixtures with deterministic, reproducible results.

---

## Historical Engineering Preservation

Engineering artifacts preserve the repository's engineering knowledge evolution.

**Preserved:**
- All Engineering Questions (investigation specifications)
- All Capability Matrices (investigation state evolution)
- All Evidence Reports (findings and recommendations)
- All Spike Evidence (individual investigation results)

**Purpose:**
- Future engineers understand why decisions were made
- Evidence remains available for re-evaluation
- Investigation methodology can be improved based on historical outcomes
- Prevents rediscovering known limitations

**Immutability:** Once published, engineering artifacts should not be modified except for factual corrections. If an investigation conclusion is later invalidated, create a new Engineering Question rather than editing historical artifacts.

---

## Version Management

This governance document is versioned to allow methodology evolution while preserving historical validity.

**Current Version:** 1.0

**Version History:**

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-14 | Initial governance established |

**Future Evolution:**
- Methodology improvements increment version (1.1, 2.0)
- Each EQ references the governance version it follows
- Historical EQs remain valid under their referenced version

---

## Relationship to Other Governance

This document complements existing repository governance:

| Governance Layer | Purpose |
|------------------|---------|
| **Principles** (`docs/01_Principles.md`) | Engineering philosophy |
| **ADRs** (`docs/decisions/`) | Architectural decisions |
| **Engineering Governance** (this document) | Investigation methodology |
| **Engineering Questions** | Capability-specific investigations |
| **Evidence Reports** | Implementation justification |

---

## References

- `docs/01_Principles.md` — Repository engineering principles
- `docs/decisions/TEMPLATE.md` — ADR template and process
- `docs/templates/Capability_Matrix_Template.md` — Reusable capability discovery template
- `docs/engineering/README.md` — Engineering workflow overview

---

## Document Control

**Owner:** Project Owner  
**Review Schedule:** Upon methodology improvement proposal  
**Distribution:** All contributors, AI agents

---

## TODO

- [ ] TODO(Project Owner): Define regression testing requirements for promoted capabilities
- [ ] TODO(Project Owner): Establish evidence quality standards for production recommendations
- [ ] TODO(Project Owner): Document procedure for invalidating historical investigation conclusions