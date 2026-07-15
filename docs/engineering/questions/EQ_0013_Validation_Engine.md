# EQ-0013: Validation Engine

**Status:** APPROVED — FROZEN — Complete (Gate 3 Approved)
**Date Created:** 2026-07-15
**Gate 1 Approval:** 2026-07-15
**Gate 2 Approval:** 2026-07-15 (Spike 3 Complete)
**Gate 3 Approval:** 2026-07-15 (Spike 4 Complete — Engine Implemented)
**Governance:** Engineering_Governance.md v1.0
**Owner:** Project Owner
**Milestone:** M8 — Consumer Architecture

---

## Core Engineering Question

**"What deterministic validation capabilities can consume the frozen Public Evidence Contract while preserving the EQ-0011 engineering boundary?"**

This investigation asks: What validation logic can be built as reusable infrastructure that multiple consumers (CheckMate, Formatter, Builder, O&A, Reporting) can depend on without duplicating BOQ Intelligence logic or violating engineering boundaries?

---

## Investigation Context

### Background

The repository has completed the Producer Era:
- BOQ Intelligence (Increments 1-3) produces deterministic structural evidence
- Public Evidence Contract v1.0.0 frozen (EQ-0012)
- Evidence Contract provides stable API for consumers
- EQ-0011 engineering boundary established (Observe/Reconstruct/Detect vs. Judge/Recommend/Assess)

**Software Version:** v0.0.1-alpha.10
**Architecture Version:** v0.1.0

### Current State

The repository transitions from Producer Era to Consumer Era:

```
Producer Era (Complete):
CostX Workbook → WorkbookParser → BOQRow[] → BOQ Intelligence → Evidence Contract

Consumer Era (Begins):
Evidence Contract → Validation Engine → Applications
```

**Authority:** EQ-0010 (Deterministic BOQ Structural Intelligence), EQ-0011 (BOQ Semantic Intelligence Boundary), EQ-0012 (Public Evidence Contract v1.0)

### The Engineering Challenge

M8 introduces multiple consumers of BOQ Intelligence evidence:
- CheckMate (BOQ validation application)
- Formatter (BOQ export formatting)
- Builder (Builder QA)
- Omission & Addition (O&A analysis)
- Reporting (BOQ reports)

**Problem:** Without shared validation infrastructure, consumers may:
- Duplicate validation logic
- Depend on BOQ Intelligence internals
- Violate EQ-0011 engineering boundary
- Implement inconsistent validation semantics
- Break when Evidence Contract evolves

**Solution Required:** Define a Validation Engine that:
- Consumes only the frozen Public Evidence Contract
- Preserves EQ-0011 boundary (no judge/recommend/assess)
- Provides reusable validation capabilities
- Enables consumer independence
- Remains deterministic and evidence-backed

---

## First Principle

**The Validation Engine is reusable deterministic infrastructure that evaluates evidence against rules. It provides findings, not recommendations. Human decision-making remains external to the engine.**

## Evidence Admission Rule

Validation Engine specifications may only include:
1. Validation capabilities implementable using frozen Evidence Contract v1.0
2. Rule categories supported by EQ-0011 engineering boundary
3. Deterministic evaluation logic without semantic reasoning

Speculative validations, consumer-specific logic, and boundary violations are not permitted.

---

## Investigation Subjects

### Subject 1: Validation Capability Inventory

**Current Evidence Available (from Evidence Contract v1.0):**
- Increment 1: row_classification, section_statistics, boq_statistics, known_anomalies
- Increment 2: hierarchy, hierarchy_statistics
- Increment 3: detected_level_skips, zero_quantity_items, structural_containment_findings, completeness_findings

**Questions:**
- What validation capabilities are possible using only frozen evidence?
- Which evidence fields support which validation categories?
- What validations require combinations of evidence fields?
- What validations are impossible without additional evidence?

### Subject 2: Validation Rule Taxonomy

**Questions:**
- How should validation rules be classified? (Structural, Consistency, Completeness, Relationship, Boundary, Other)
- What distinguishes each category?
- Which categories preserve EQ-0011 boundary?
- Which categories cross EQ-0011 boundary?
- How are categories verified against frozen evidence?

### Subject 3: Validation Engine Responsibilities

**Questions:**
- What belongs inside the Validation Engine?
- What belongs outside (in consumers)?
- Where is the boundary between engine and consumer?
- What is the engine's public API?
- What validation state (if any) does the engine maintain?

### Subject 4: Consumer Compliance

**Questions:**
- How do consumers interact with the Validation Engine?
- What is the expected usage pattern?
- How are validation results structured?
- How do consumers interpret findings?
- What is NOT the engine's responsibility?

### Subject 5: Consumer Independence

**Questions:**
- Can CheckMate, Formatter, Builder, O&A, and Reporting all consume the same engine?
- What ensures no application-specific logic enters the engine?
- How is consumer independence verified?
- What prevents coupling between engine and specific consumers?

### Subject 6: Boundary Preservation

**Questions:**
- How does every validation preserve: Observation → Evidence → Finding → Human Decision?
- How are automatic recommendations prevented?
- How is EQ-0011 boundary enforced in validation rules?
- What verification ensures boundary compliance?

### Subject 7: Consumer Compliance Suite

**Questions:**
- What is the Consumer Compliance Suite?
- How does it differ from the Validation Engine?
- What does the Compliance Suite verify?
- How do consumers demonstrate compliance?
- What regression protection does the suite provide?

---

## Investigation Approach

### Evidence-First Methodology

```
Spike 1: Validation Capability Discovery
         ↓
Spike 2: Validation Rule Taxonomy
         ↓
Spike 3: Validation Engine Scope & Responsibilities
         ↓
Spike 4: Consumer Interaction Patterns
         ↓
Spike 5: Consumer Compliance Suite Design
         ↓
Spike 6: Boundary Verification Framework
         ↓
Spike 7: Validation Engine Specification
```

### Spike Descriptions

**Spike 1: Validation Capability Discovery**
- Enumerate all possible validations using frozen Evidence Contract
- Map evidence fields to validation categories
- Identify validation combinations requiring multiple fields
- Document impossible validations (insufficient evidence)
- Establish draft Validation Rule Registry with provenance tracking
- Classify every validation: Supported, Multiple Fields, Insufficient Evidence, Boundary Violation, or Speculative
- Create Evidence-to-Rule Mapping
- Document Unsupported Validation Inventory
- Output: Validation capability inventory with complete provenance

**Spike 1 Deliverables:**
- Validation capability inventory
- Draft Validation Rule Registry (Rule ID, Category, Evidence Fields, Boundary Class, Introduced By, Contract Version, Status)
- Rule Provenance Matrix (every rule traces to frozen evidence)
- Evidence-to-Rule Mapping (Evidence Fields → Rule → Finding → Consumers)
- Unsupported Validation Inventory (validations impossible with current evidence)
- Boundary Classification Summary (EQ-0011 compliance verification)

**Spike 1 Engineering Discipline:**
- Every validation begins with Public Evidence Contract, never BOQ Intelligence internals
- Every validation has documented provenance (Evidence Fields, Contract Version, EQ Source, Supporting Spike)
- Every validation follows: Evidence → Deterministic Rule → Deterministic Finding → Human Interpretation
- No implementation, no consumer behavior design, no recommendations
- Consumer independence preserved (ask "What does evidence support?" not "What does CheckMate need?")
- Only Supported and Multiple Fields categories may proceed toward implementation

**Spike 2: Validation Rule Taxonomy**
- Define validation rule categories
- Classify each category against EQ-0011 boundary
- Provide evidence-backed examples for each category
- Document category distinctions
- Output: Validation rule taxonomy

**Spike 3: Validation Engine Scope & Responsibilities** (COMPLETE — 2026-07-15)
- Define engine responsibilities (inside scope)
- Define consumer responsibilities (outside scope)
- Design engine public API
- Document engine/consumer boundary
- Output: Validation Engine scope specification
- Evidence Report: `docs/engineering/evidence/EQ_0013_Spike3_Evidence_Report_Engine_Scope_and_Responsibilities.md`
- Scope Document: `data/reports/eq0013_spike3_engine_scope.json`
- Architecture Consistency Audit: `data/reports/eq0013_spike3_architecture_consistency.json`
- Tools: `tools/eq0013_spike3_engine_scope.py`, `tools/eq0013_spike3_architecture_consistency_audit.py`
- Architecture Consistency Gate: 9/9 PASS (0 FAIL, 0 DESIGN_NOTE)

**Spike 4: Consumer Interaction Patterns**
- Design consumer usage patterns
- Define validation result structures
- Document consumer interpretation responsibilities
- Establish consumer-independence constraints
- Output: Consumer interaction specification

**Spike 5: Consumer Compliance Suite Design**
- Define Compliance Suite purpose and scope
- Design compliance verification categories
- Establish verification tooling approach
- Document suite vs. engine separation
- Output: Consumer Compliance Suite specification

**Spike 6: Boundary Verification Framework**
- Design EQ-0011 boundary enforcement mechanism
- Define boundary violation detection
- Establish automatic recommendation prevention
- Document verification procedures
- Output: Boundary verification framework

**Spike 7: Validation Engine Specification**
- Synthesize findings from Spikes 1-6
- Author Validation Engine specification
- Document all validation capabilities
- Document all consumer compliance requirements
- Establish Validation Engine v1.0 baseline
- Output: `docs/engineering/capability_matrices/EQ_0013_Validation_Engine_Capability_Matrix.md`

---

## Success Criteria

Investigation is complete when:

1. ☒ All validation capabilities possible with Evidence Contract v1.0 are inventoried (Spike 1)
2. ☒ Validation rule taxonomy is defined and boundary-verified (Spike 2)
3. ☒ Validation Engine scope and responsibilities are specified (Spike 3)
4. ☐ Consumer interaction patterns are documented
5. ☐ Consumer Compliance Suite is defined
6. ☐ Boundary verification framework is established
7. ☐ Validation Engine specification is authored
8. ☐ Project Owner approves Validation Engine specification

---

## Exit Criteria

This investigation concludes when:
- All 7 spikes complete
- Validation Engine specification is frozen
- Gate 2 approval obtained from Project Owner

If evidence is insufficient, the investigation may be paused pending additional research.

---

## Decision Framework

After investigation completes, Project Owner will decide:

**Option A: Approve Validation Engine Specification**
- Validation Engine specification is frozen
- Implementation phase may begin
- Consumer development may proceed

**Option B: Request Revisions**
- Specific revisions requested
- Investigation resumes to address feedback

**Option C: Defer**
- Validation Engine deferred pending additional prerequisites

---

## Scope and Non-Goals

### In Scope
- Validation capabilities using frozen Evidence Contract v1.0
- Validation rule taxonomy
- Validation Engine scope and API
- Consumer interaction patterns
- Consumer Compliance Suite design
- Boundary verification framework
- Evidence-backed validation examples

### Out of Scope
- CheckMate implementation
- User interface design
- Runtime service architecture
- Recommendation engines
- Semantic reasoning
- AI assessment
- BOQ Intelligence modifications
- Evidence Contract modifications
- Consumer-specific application logic
- Speculative validation capabilities

---

## Architectural Principles

### Consumer Independence

The Validation Engine must remain consumer-independent. No application-specific logic (CheckMate, Formatter, Builder, O&A, Reporting) may enter the engine. Consumer-specific interpretation belongs in consumers, not the engine.

### Evidence Contract Dependency

The Validation Engine depends ONLY on the frozen Public Evidence Contract v1.0. No BOQ Intelligence internals may be accessed. No unstable imports. No internal implementation coupling.

### Boundary Preservation

Every validation must preserve the EQ-0011 boundary:
- Observation → Evidence → Deterministic Finding → Human Decision

Never:
- Observation → Automatic Recommendation

### Deterministic Evaluation

All validation logic must be deterministic. Same evidence input produces same finding output. No probabilistic reasoning. No semantic interpretation. No AI assessment.

### Verification-First

Every validation capability must be verifiable against frozen evidence. Verification tooling precedes specification finalization.

---

## Consumer Analysis

**Primary Consumer:** M8 CheckMate (BOQ validation application)

**Future Consumers:**
- Formatter (BOQ export formatting)
- Builder (Builder QA)
- Omission & Addition (O&A analysis)
- Reporting (BOQ reports)

All consumers require:
- Deterministic validation logic
- Evidence Contract v1.0 compliance
- EQ-0011 boundary preservation
- Consumer independence

---

## Architecture Impact

**Changes Required:**
- Create `docs/engineering/capability_matrices/EQ_0013_Validation_Engine_Capability_Matrix.md`
- Potentially create validation engine module (if investigation recommends)
- Document validation capabilities and consumer compliance

**No Changes Required:**
- BOQ Intelligence implementation (frozen)
- Evidence Contract v1.0 (frozen)
- Test suite (validation semantics are new)

**ADR Required:** TBD (depends on investigation findings)

---

## References

- EQ-0010: Deterministic BOQ Structural Intelligence
- EQ-0011: BOQ Semantic Intelligence Boundary
- EQ-0012: BOQ Intelligence Public Evidence Contract
- `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md`
- `src/jarvis/parsers/costx/boq_intelligence.py`
- `docs/planning/M8_Repository_Assessment_and_Consumer_Architecture_Planning.md`
- Engineering_Governance.md v1.0

---

## Investigation Timeline

**Estimated Duration:** 7 spikes

**Spike 1:** Validation Capability Discovery (Complete — 2026-07-15)
**Spike 2:** Validation Rule Taxonomy (Complete — 2026-07-15)
**Spike 3:** Engine Scope & Responsibilities (Complete — 2026-07-15)
**Spike 4:** Consumer Interaction Patterns (1 day)
**Spike 5:** Consumer Compliance Suite Design (1 day)
**Spike 6:** Boundary Verification Framework (1 day)
**Spike 7:** Validation Engine Specification (1-2 days)

**Total:** 7-8 days

---

## Approval

**Gate 1 (Investigation Authorization):**
- [x] Project Owner approves investigation plan
- [x] Reinforcement guidance applied
- [x] Investigation may begin

**Gate 2 (Implementation Authorization):**
- [ ] All 7 spikes complete
- [ ] Validation Engine specification frozen
- [ ] Project Owner approves specification
- [ ] Implementation may begin

---

## Document Control

**Status:** APPROVED — FROZEN — Complete (Gate 3 Approved)
**Final Freeze Report:** `docs/engineering/evidence/EQ_0013_Final_Freeze_Report.md`
**Evidence Contract:** `docs/contracts/Validation_Findings_Contract_v1.0.md`
**Spike 4 Evidence:** `docs/engineering/evidence/EQ_0013_Spike4_Evidence_Report_Validation_Engine_Implementation.md`
**Production Code:** `src/jarvis/engines/validation/engine.py`
**Distribution:** Engineering team, Project Owner

---

**End of Engineering Question — EQ-0013 Frozen**
