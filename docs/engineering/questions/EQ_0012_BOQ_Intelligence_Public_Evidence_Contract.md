# EQ-0012: BOQ Intelligence Public Evidence Contract

**Status:** COMPLETE — Gate 2 Approved
**Date Created:** 2026-07-15  
**Date Completed:** 2026-07-15  
**Governance:** Engineering_Governance.md v1.0  
**Owner:** Project Owner  
**Milestone:** M8 — Consumer Architecture

---

## Core Engineering Question

**"What constitutes a stable, versioned Public Evidence Contract for BOQ Intelligence that enables multiple consumers to depend on deterministic evidence without coupling to internal implementation details?"**

This investigation asks: How should BOQ Intelligence expose its evidence as a formal, stable API?

---

## Investigation Context

### Background

BOQ Intelligence (Increments 1-3) successfully produces deterministic structural evidence:
- Increment 1: Observation evidence (row classification, statistics, anomalies)
- Increment 2: Hierarchy evidence (tree reconstruction, depth, parent identification)
- Increment 3: Detection evidence (level skips, zero quantities, containment, completeness)

All evidence is produced through the `analyze_boq()` function which returns a `BOQIntelligenceResult` frozen dataclass.

### Current State

Evidence is **implicitly** exposed through `BOQIntelligenceResult` fields:
- No formal contract definition
- No versioning policy
- No backward compatibility guarantees
- No consumer migration guidance
- Internal structure exposed directly

**Authority:** EQ-0010 (Deterministic BOQ Structural Intelligence), EQ-0011 (BOQ Semantic Intelligence Boundary)

### The Engineering Challenge

M8 introduces the first consumer (CheckMate). Future consumers include:
- Formatter
- Builder
- Omission & Addition Analysis
- Reporting
- AI Review

**Problem:** Without a formal Evidence Contract, consumers may:
- Depend on internal implementation details
- Break when BOQ Intelligence evolves
- Duplicate detection logic
- Couple to unstable interfaces

**Solution Required:** Define a Public Evidence Contract that:
- Exposes only stable, deterministic evidence
- Hides internal implementation details
- Provides version guarantees
- Enables safe evolution
- Documents evidence semantics

---

## First Principle

**Evidence Contract is the stable API between Intelligence Producer and Intelligence Consumers. It must remain stable across versions while enabling producer evolution.**

## Evidence Admission Rule

Evidence Contract specifications may only include:
1. Evidence fields currently produced by BOQ Intelligence (Increments 1-3)
2. Evidence semantics documented in frozen EQ-0010/EQ-0011 evidence reports
3. Data structures directly observable in `BOQIntelligenceResult`

Speculative future evidence, implementation details, and internal algorithms are not permitted in the contract.

---

## Gate 1 Approval

**Date:** 2026-07-15  
**Status:** APPROVED  

**Conditions:**
1. Treat the output consistently as a Public Evidence Contract, not merely an API
2. Add Contract Invariants as an explicit investigation subject

Both conditions accepted and incorporated into investigation plan.

---

## Investigation Subjects

### Subject 1: Evidence Field Stability

**Current Evidence Fields (Increment 1):**
- `row_classification: dict[str, int]`
- `section_statistics: dict[str, dict[str, int]]`
- `boq_statistics: dict[str, int | float]`
- `known_anomalies: list[dict]`

**Current Evidence Fields (Increment 2):**
- `hierarchy: tuple[BOQHeaderNode, ...] | None`
- `hierarchy_statistics: dict[str, int | float] | None`

**Current Evidence Fields (Increment 3):**
- `detected_level_skips: tuple[dict, ...] | None`
- `zero_quantity_items: tuple[dict, ...] | None`
- `structural_containment_findings: tuple[dict, ...] | None`
- `completeness_findings: tuple[dict, ...] | None`

**Questions:**
- Which fields must remain stable across versions?
- Which fields can be safely extended?
- Which fields require deprecation support?
- What guarantees do consumers need?

### Subject 2: Contract Versioning

**Questions:**
- How should contract versions be numbered? (Semantic versioning? Sequential?)
- When does a version increment occur?
- What constitutes a breaking change?
- What constitutes a non-breaking change?
- How are version numbers exposed to consumers?

### Subject 3: Backward Compatibility

**Questions:**
- What backward compatibility guarantees are required?
- How long must deprecated fields be supported?
- How should deprecation be signaled?
- What migration path is provided for breaking changes?
- How are multiple contract versions supported?

### Subject 4: Evidence Semantics Documentation

**Questions:**
- What documentation is required for each evidence field?
- How are field semantics specified?
- How are data structure invariants documented?
- How are evidence constraints described?
- How is evidence traceability maintained?

### Subject 5: Contract Invariants

**Questions:**
- What invariants must hold for each evidence field?
- How are data structure constraints documented?
- What guarantees exist for evidence relationships?
- How are invariants verified?
- What happens when invariants are violated?

### Subject 6: Consumer Access Patterns

**Questions:**
- How should consumers import the contract?
- Should evidence be exposed through a dedicated module?
- How are internal implementation details hidden?
- What access controls prevent coupling?
- How is contract compliance verified?

---

## Investigation Approach

### Evidence-First Methodology

```
Spike 1: Current Evidence Inventory
         ↓
Spike 2: Contract Structure & Versioning Policy
         ↓
Spike 3: Contract Invariants
         ↓
Spike 4: Consumer Access Patterns
         ↓
Spike 5: Contract Documentation Standards
         ↓
Spike 6: Evidence Contract v1.0 Specification
```

### Spike Descriptions

**Spike 1: Current Evidence Inventory**
- Enumerate all evidence fields from Increments 1-3
- Document field types, semantics, and invariants
- Trace each field to EQ-0010/EQ-0011 evidence
- Identify stable vs. unstable fields
- Output: Complete evidence inventory

**Spike 2: Contract Structure & Versioning Policy**
- Define contract versioning scheme
- Establish breaking vs. non-breaking change criteria
- Design version increment triggers
- Define backward compatibility guarantees
- Design deprecation policy
- Output: Versioning policy specification

**Spike 3: Contract Invariants**
- Document invariants for each evidence field
- Define data structure constraints
- Document evidence field relationships
- Define invariant verification approach
- Document invariant violation handling
- Output: Contract invariants specification

**Spike 4: Consumer Access Patterns**
- Design consumer import model
- Design internal detail hiding strategy
- Evaluate evidence module separation
- Design contract compliance verification
- Output: Access pattern specification

**Spike 5: Contract Documentation Standards**
- Define evidence field documentation requirements
- Design semantics specification format
- Design invariant documentation format
- Design traceability documentation
- Output: Documentation standards

**Spike 6: Evidence Contract v1.0 Specification**
- Synthesize findings from Spikes 1-5
- Author Public Evidence Contract v1.0 document (not merely API documentation)
- Define all contract elements
- Document all evidence fields
- Document all contract invariants
- Establish version 1.0 baseline as formal contract
- Output: `docs/contracts/BOQ_Intelligence_Evidence_Contract.md` v1.0

---

## Success Criteria

Investigation is complete when:

1. ✅ All evidence fields from Increments 1-3 are inventoried with semantics
2. ✅ Contract versioning policy is defined
3. ✅ Contract invariants are documented
4. ✅ Backward compatibility guarantees are established
5. ✅ Consumer access patterns are specified
6. ✅ Documentation standards are established
7. ✅ Public Evidence Contract v1.0 is authored and frozen
8. ✅ Project Owner approves Evidence Contract v1.0

---

## Exit Criteria

This investigation concludes when:
- All 5 spikes complete
- Evidence Contract v1.0 is frozen
- Gate 2 approval obtained from Project Owner

If evidence is insufficient, the investigation may be paused pending additional research.

---

## Decision Framework

After investigation completes, Project Owner will decide:

**Option A: Approve Evidence Contract v1.0**
- Evidence Contract is frozen
- Consumers may begin depending on contract
- EQ-0013 (Validation Engine) may proceed

**Option B: Request Revisions**
- Specific revisions requested
- Investigation resumes to address feedback

**Option C: Defer**
- Evidence Contract deferred pending additional prerequisites

---

## Scope and Non-Goals

### In Scope
- Evidence fields currently produced by BOQ Intelligence
- Contract versioning policy
- Backward compatibility guarantees
- Consumer access patterns
- Documentation standards
- Evidence Contract v1.0 document

### Out of Scope
- Future evidence fields not yet implemented
- Validation rules (belongs to EQ-0013)
- CheckMate application design (belongs to EQ-0014)
- Evidence production implementation (already complete)
- Breaking changes to existing evidence (frozen in Increments 1-3)

---

## Consumer Analysis

**Primary Consumer:** M8 CheckMate (BOQ validation application)

**Future Consumers:**
- Formatter (BOQ export formatting)
- Builder (Builder QA)
- Omission & Addition (O&A analysis)
- Reporting (BOQ reports)
- AI Review (Future AI-assisted review)

All consumers require:
- Stable evidence API
- Version guarantees
- Clear semantics
- Deterministic evidence

---

## Architecture Impact

**Changes Required:**
- Create `docs/contracts/BOQ_Intelligence_Evidence_Contract.md` v1.0
- Potentially create evidence access module (if Spike 3 recommends)
- Document versioning in contract

**No Changes Required:**
- BOQ Intelligence implementation (frozen)
- Increment 1-3 evidence fields (frozen)
- Test suite (evidence semantics unchanged)

**ADR Required:** No (contract is documentation, not architecture change)

---

## References

- EQ-0010: Deterministic BOQ Structural Intelligence
- EQ-0011: BOQ Semantic Intelligence Boundary
- `src/jarvis/parsers/costx/boq_intelligence.py`
- `docs/planning/M8_Repository_Assessment_and_Consumer_Architecture_Planning.md`
- Engineering_Governance.md v1.0

---

## Investigation Timeline

**Estimated Duration:** 6 spikes

**Spike 1:** Evidence Inventory (1 day)  
**Spike 2:** Versioning Policy (1 day)  
**Spike 3:** Contract Invariants (1 day)  
**Spike 4:** Access Patterns (1 day)  
**Spike 5:** Documentation Standards (1 day)  
**Spike 6:** Contract v1.0 (1-2 days)

**Total:** 6-8 days

---

## Approval

**Gate 1 (Investigation Authorization):**
- [x] Project Owner approves investigation plan
- [x] Investigation may begin

**Gate 2 (Implementation Authorization):**
- [x] All 6 spikes complete
- [x] Public Evidence Contract v1.0 frozen
- [x] Contract invariants documented
- [x] Project Owner approves contract
- [x] EQ-0013 may begin

---

## Document Control

**Status:** COMPLETE — Gate 2 Approved
**Next Review:** Upon contract evolution (MAJOR version change)
**Distribution:** Engineering team, Project Owner, all consumers

---

**End of Engineering Question**