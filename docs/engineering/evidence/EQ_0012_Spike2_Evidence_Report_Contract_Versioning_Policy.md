# EQ-0012 — Spike 2 — Evidence Report — Contract Structure & Versioning Policy

**Date:** 2026-07-15  
**Status:** Approved and Frozen  
**Investigation:** EQ-0012 BOQ Intelligence Public Evidence Contract  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction

---

## Objective

Define the versioning scheme, compatibility rules, consumer guarantees, and deprecation lifecycle for the BOQ Intelligence Public Evidence Contract.

This spike answers the question: **"How is evidence governed as a stable Public Evidence Contract?"**

---

## Methodology

Systematic evaluation organized around four questions:

1. **Version Identity** — How is the contract version identified?
2. **Compatibility Rules** — What constitutes Major/Minor/Patch changes?
3. **Consumer Guarantees** — What can every consumer permanently rely on?
4. **Deprecation Lifecycle** — How is an obsolete field retired?

Tool: `tools/eq0012_spike2_contract_versioning_policy.py`

---

## Findings

### Question 1: Version Identity

**Recommendation: Semantic Versioning (MAJOR.MINOR.PATCH)**

**Initial Version:** Candidate 1.0.0 (final 1.0.0 reserved for Spike 6)

**Evaluated Alternatives:**

| Scheme | Format | Strength | Weakness |
|--------|--------|----------|----------|
| **Semantic** | X.Y.Z (1.0.0) | Industry standard, clear upgrade path, tooling support | Requires disciplined enforcement |
| **Calendar** | YEAR.RELEASE (2026.1) | Time-based predictability | Does not communicate compatibility |
| **Sequential** | v1, v2, v3 | Simple | No granularity, every change is MAJOR |

**Rationale for Semantic Versioning:**
1. The Evidence Contract is a formal API — semantic versioning is the established standard
2. Consumers need to know whether an upgrade is safe (patch/minor) or requires attention (major)
3. Industry tooling expects semantic versions
4. Three segments provide appropriate granularity for breaking vs. non-breaking changes

**Decision:** Semantic Versioning with initial version 1.0.0

---

### Question 2: Compatibility Rules

**MAJOR (X.0.0) — Breaking changes requiring consumer attention:**

| Change | Rationale |
|--------|-----------|
| Removing a required field | Breaks consuming code that expects the field |
| Changing type of a required field | Breaks consuming code that depends on the type |
| Renaming a required field | Breaks consuming code that references by name |
| Adding, removing, or changing a required field | Contract shape altered; strict consumers (generated clients, type systems, validators) consider required fields mandatory regardless of runtime defaults |
| Changing invariants consumers depend on | Changes behavior consumers may rely on |
| Removing optional field without deprecation | Violates deprecation contract |
| Removing documented dictionary keys | Breaks consumers expecting keys |
| Changing tuple element order or semantics | Breaks consumers using positional access |
| Extending tuple contents | Tuples are ordered, frozen structures; consumers often destructure (`a, b, c = result`) or index (`result[2]`); extension breaks these patterns |

**MINOR (0.Y.0) — Non-breaking additions:**

| Change | Rationale |
|--------|-----------|
| Adding new optional field | Consumer must opt-in to use |
| Adding new dict keys | Consumers iterating dynamically unaffected |
| Adding BOQHeaderNode fields (with defaults) | Backward compatible dataclass extension |
| Marking field as deprecated | Field still present and functional |

**PATCH (0.0.Z) — Internal corrections:**

| Change | Rationale |
|--------|-----------|
| Fixing documentation errors | No behavior change |
| Clarifying field semantics | No consumer impact |
| Adding invariant documentation | No consumer impact |
| Correcting type annotations | Matching actual behavior |
| Non-functional changes | No consumer impact |

**Key Insight:** Required vs. Optional distinction is critical. Changes to required fields are always MAJOR. Additions to optional fields can be MINOR. Removing optional fields without deprecation lifecycle is MAJOR.

---

### Question 3: Consumer Guarantees

**16 Permanent Guarantees across 5 categories:**

**Structural Guarantees (G-01 to G-03):**
- G-01: All documented fields will exist for the promised contract version
- G-02: Required fields will never be None
- G-03: Optional fields will never be removed without formal deprecation

**Type Guarantees (G-04 to G-07):**
- G-04: Field types as documented will not change within a MAJOR version
- G-05: Union types will not remove valid variants
- G-06: Documented dictionary keys will remain present
- G-07: Undocumented keys may appear (non-breaking addition)

**Semantic Guarantees (G-08 to G-10):**
- G-08: Documented field semantics will not change within a MAJOR version
- G-09: Evidence classification (Observation/Hierarchy/Detection) will not change
- G-10: EQ-0011 engineering boundary preserved in all evidence

**Determinism Guarantees (G-11 to G-13):**
- G-11: All evidence is deterministic — same input produces same output
- G-12: All evidence is immutable — consumers cannot modify evidence
- G-13: All evidence is traceable to frozen engineering evidence

**Access Guarantees (G-14 to G-16):**
- G-14: Consumers may depend on the Evidence Contract directly
- G-15: Consumers may import evidence types without importing internal implementation
- G-16: Consumers will not need access to internal BOQ Intelligence functions

---

### Question 4: Deprecation Lifecycle

**Three-Phase Deprecation Model:**

```
Phase 1: Deprecation Announcement (MINOR version bump)
    ↓
Phase 2: Removal Notice (same MAJOR version)
    ↓
Phase 3: Removal (next MAJOR version bump)
```

**Phase 1 — Deprecation Announcement:**
- Trigger: Engineering Question determines field is obsolete
- Action: Field marked `@deprecated` in contract documentation
- Version: MINOR version bump (field still present and functional)
- Duration: One full MAJOR version cycle minimum

**Phase 2 — Removal Notice:**
- Trigger: Next MAJOR version planning
- Action: Explicit notification with target removal version
- Version: Still present in current MAJOR version
- Consumer impact: Field still present, consumers should migrate

**Phase 3 — Removal:**
- Trigger: MAJOR version bump
- Action: Field removed from Evidence Contract
- Version: MAJOR version bump
- Consumer impact: Breaking change — consumers must migrate

**Governance Gate (before any deprecation can begin):**
1. Engineering Question must classify the field as obsolete
2. Project Owner must approve deprecation
3. All consumers must be notified
4. Migration path must be documented
5. Minimum deprecation period: one full MAJOR version

---

## Versioning Policy Specification

### 1. Version Identity

| Property | Value |
|----------|-------|
| Scheme | Semantic Versioning |
| Format | MAJOR.MINOR.PATCH |
| Initial Version | 1.0.0 (Candidate) |
| Location | `docs/contracts/BOQ_Intelligence_Evidence_Contract.md` |

### 2. Compatibility Rules

**MAJOR breaking changes:**
- Adding, removing, or changing required fields
- Removing or renaming required fields
- Changing required field types
- Changing documented invariants
- Removing optional fields without deprecation lifecycle
- Removing documented dictionary keys
- Changing tuple element order or semantics
- Extending tuple contents

**Policy Notes:**
- **Required fields:** Contract evolution optimizes for strict consumers (generated clients, type systems, validators). Required fields alter contract shape regardless of runtime defaults.
- **Tuples:** Ordered, frozen structures. Future extensible evidence should prefer named structures (dataclasses, dictionaries). If a tuple must grow, explicit append-only semantics required in contract.

**MINOR non-breaking additions:**
- Adding new optional fields
- Adding new dictionary keys
- Adding dataclass fields (with defaults)
- Marking fields as deprecated

**PATCH internal corrections:**
- Documentation fixes and clarifications
- Invariant documentation additions
- Type annotation corrections
- Changes with no consumer impact

### 3. Consumer Guarantees

16 guarantees (G-01 through G-16) as documented in findings above.

### 4. Deprecation Lifecycle

Three-phase model with minimum one full MAJOR version deprecation period. Governance gate requires Engineering Question, Project Owner approval, consumer notification, and documented migration path.

---

## Contract Implications

### Impact on Evidence Contract v1.0

The versioning policy establishes:

1. **Initial Version:** Candidate 1.0.0
2. **Stability:** All 10 evidence fields frozen at 1.0.0
3. **Forward Compatibility:** Additions allowed via MINOR bumps
4. **Safety:** Breaking changes require MAJOR bumps
5. **Consumer Trust:** 16 permanent guarantees
6. **Evolution Path:** Deprecation lifecycle enables responsible retirement

### Risk Mitigation

**Risk:** Semantic versioning scope creep (MAJOR bumps for non-breaking changes)
**Mitigation:** Compatibility rules explicitly define what constitutes each level

**Risk:** Optional fields treated as unstable
**Mitigation:** G-03 guarantees optional fields will not be removed without deprecation

**Risk:** Inconsistent deprecation
**Mitigation:** Governance gate requires Project Owner approval

---

## Next Steps

1. **Spike 3:** Contract Invariants
   - Document invariants for each evidence field
   - Define invariant verification approach
   - Define invariant violation handling

2. **Spike 4:** Consumer Access Patterns
   - Design consumer import model
   - Design internal detail hiding strategy

3. **Spike 5:** Contract Documentation Standards
   - Define evidence field documentation requirements
   - Design semantics specification format

4. **Spike 6:** Evidence Contract v1.0 Specification
   - Synthesize all findings
   - Author Public Evidence Contract v1.0

---

## Conclusion

**Status:** Spike 2 Complete

**Key Findings:**
- Semantic Versioning selected (MAJOR.MINOR.PATCH)
- 16 consumer guarantees established
- Three-phase deprecation lifecycle defined
- Compatibility rules explicitly documented
- Required vs. Optional distinction embedded in all policies

**Recommendation:** Proceed to Spike 3 (Contract Invariants).

---

## Tool

**Spike Implementation:** `tools/eq0012_spike2_contract_versioning_policy.py`

---

**End of Evidence Report**