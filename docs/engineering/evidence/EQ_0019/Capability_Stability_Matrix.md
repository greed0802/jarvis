# Capability Stability Matrix — EQ-0019
# BOQ Intelligence Increment 4

## Status
ACTIVE

## Purpose
Define stability classifications for every semantic capability in Increment 4 per the governance maturity model. This matrix describes governance maturity — it does NOT replace or override Production Ready classification from Spike 2.

## Authority
- EQ-0019 Authority Document
- EQ-0019 Final Architecture Review
- Engineering Governance v1.0
- BOQ Intelligence Public Evidence Contract v1.0

---

## Stability Definitions

| Level | Definition | Upgrade Policy | Downgrade Policy |
|---|---|---|---|
| **Experimental** | Early evidence. Expected to change. | As evidence matures, may be promoted to Candidate by completing required spike work and obtaining PO approval. | May be downgraded to Rejected if new evidence contradicts feasibility. Requires EQ. |
| **Candidate** | Engineering evidence exists. Implementation may still evolve. | As implementation matures, may be promoted to Stable by completing contract formalization and passing Quality Gates 1-2. Requires PO approval. | May be downgraded to Experimental or Rejected if new evidence reveals significant gaps. Requires new EQ. |
| **Stable** | Production implementation expected to remain compatible within the current MAJOR version. | May be promoted to Frozen by passing Increment 4 freeze criteria (Gates 1-3) and receiving explicit PO freeze authorization. Requires formal freeze declaration. | Breaking changes require MAJOR version bump. Requires new EQ + ADR + PO approval. Non-breaking changes permitted as MINOR/PATCH. |
| **Frozen** | Behavior becomes part of permanent engineering contract and may only change through a new Engineering Question. | No further promotion from Frozen — it is the terminal state. | Requires new EQ + ADR + contract MAJOR version change + deprecation lifecycle + PO approval. |

### Lifecycle Progression

```
Experimental → Candidate → Stable → Frozen
     ↓            ↓           ↓
    Rejected    Rejected    Rejected
```

All downgrades to Rejected require new Engineering Question evidence.

---

## Capability Stability Classifications

### Production Ready Capabilities (Increment 4 Implementation Scope)

| ID | Capability | Stability | Justification | Upgrade Policy | Downgrade Policy |
|---|---|---|---|---|---|
| SEM-PROD-01 | Vocabulary extraction (term frequency) | **Candidate** | Deterministic rules defined (Spike 3). Evidence exists from EQ-0018. Architecture verified (Final Architecture Review). Implementation not yet started. No production test suite exists. | Promotes to Stable upon: (1) Implementation completed, (2) 4 unit tests pass, (3) Production fixture verification passes, (4) Include in v1.1.0 contract MINOR release. | Downgrade to Rejected requires new EQ. |
| SEM-PROD-02 | Head1 text categorization | **Candidate** | Deterministic rules defined (Spike 3). Evidence exists from EQ-0018. Frozen administrative pattern list defined. Architecture verified. Awaiting implementation. | Promotes to Stable upon: (1) Implementation completed, (2) Tests pass, (3) Fixture verification passes, (4) Contract v1.1.0 released. | Downgrade requires new EQ + evidence of pattern misclassification. |
| SEM-PROD-04 | Administrative pattern detection (boilerplate) | **Candidate** | Deterministic rules defined (Spike 3). Frozen template list defined. Architecture verified (Final Architecture Review). Dependency resolution complete (requires hierarchy). Ready for implementation. | Promotes to Stable upon: (1) Implementation completed, (2) Hierarchy integration tested, (3) Fixture verification passes. | Requires new EQ + evidence that frozen patterns are invalid. Blocked by frozen template invariants (INV-ADM-04 et al). |
| SEM-PROD-05 | Section code enumeration | **Candidate** | Most foundational capability (P0 Priority). Evidence from EQ-0018 §3. 61 codes documented. Extension of existing `section_statistics` field. Architecture verified. Awaiting implementation. | Promotes to Stable upon: (1) Implementation completed, (2) Ordering invariants verified, (3) Fixture verification passes. | Requires new EQ + evidence of enumeration failure. |
| SEM-PROD-06 | UOM distribution reporting | **Candidate** | Evidence from EQ-0018 §5 (8 UOMs with exact counts). Frequency counting that is purely deterministic (no domain judgment). Architecture verified. Awaiting implementation. | Promotes to Stable upon: (1) Implementation completed, (2) Percentage sum invariant verified, (3) Fixture verification passes. | Requires new EQ + evidence of UOM classification change. |
| SEM-PROD-07 | Header level count distribution | **Candidate** | Evidence from EQ-0018 §4 (4 level counts). Extends existing `row_classification` field. Architecture verified. Awaiting implementation. | Promotes to Stable upon: (1) Implementation completed, (2) Consistency invariant verified (Head = Head1+2+3+4), (3) Fixture verification passes. | Requires new EQ + evidence of level convention change. |
| SEM-PROD-09 | "Items Always Quantify" enforcement | **Candidate** | P3 safety net. Evidence exists (0 of 2037 header rows carry quantities). Invariant check pattern. Architecture verified. Awaiting implementation. | Promotes to Stable upon: (1) Implementation completed, (2) Empty tuple default verified, (3) Invariant asserts pass. | Requires new EQ + detection evidence of header quantities in production. |
| SEM-PROD-12 | Head1 admin sub-template recognition | **Candidate** | Deterministic sequence matching rules (Spike 3). Frozen template sequence defined. Architecture verified. Awaiting implementation. | Promotes to Stable upon: (1) Implementation completed, (2) Sequence matching tests pass, (3) Fixture verification passes. | Requires new EQ + evidence templates are incorrect. |

### Deferred Capabilities

| ID | Capability | Stability | Justification | Upgrade Policy | Downgrade Policy |
|---|---|---|---|---|---|
| SEM-PROD-03 | Description tag extraction | **Experimental** | EQ-0018 identified tag patterns but insufficient systematic analysis exists. No tag taxonomy, no tag format consistency confirmation across all trades. Spike recommended (Spike 2: deferred). | Promotes to Candidate upon: (1) New spike on tag pattern analysis, (2) Evidence of tag format conventions documented. | N/A — already Experimental; no further downgrade. |
| SEM-PROD-08 | Cross-trade pattern verification | **Experimental** | EQ-0018 confirmed 6 universal patterns but only 16/61 sections verified. Pattern universality claim requires broader evidence base. Risk: patterns observed in 16 fixtures may not generalize to all 61. | Promotes to Candidate upon: (1) Fixture expansion to all 61 sections, (2) Pattern verification spike, (3) Universe evidence. | As above. |
| SEM-PROD-10 | Items-per-section distribution | **Experimental** | No systematic analysis performed in EQ-0018. No consumer has requested this capability. YAGNI applies — implement when consumer needs it. | Promotes to Candidate only when consumer request materializes with demonstrated value. No upgrade recommended until consumption motivation exists. | As above. |

### Consumer Feature

| ID | Capability | Stability | Justification | Upgrade Policy | Downgrade Policy |
|---|---|---|---|---|---|
| SEM-PROD-11 | Note frequency distribution by section | **Experimental** | Classified as Consumer Feature (Spike 2). Valuable for CheckMate note review but not as standalone BOQ Intelligence capability. Better implemented as part of CheckMate consumer design. | Promotes to Candidate through CheckMate consumer design interval, not through BOQ Intelligence. | N/A. |

---

## Capability Stability Matrix Summary

| Classification | Count | Capabilities |
|---|---|---|
| **Experimental** | 4 | SEM-PROD-03, SEM-PROD-08, SEM-PROD-10, SEM-PROD-11 |
| **Candidate** | 8 | SEM-PROD-01, SEM-PROD-02, SEM-PROD-04, SEM-PROD-05, SEM-PROD-06, SEM-PROD-07, SEM-PROD-09, SEM-PROD-12 |
| **Stable** | 0 | None (implementation not yet performed) |
| **Frozen** | 0 | None (Increment 4 not yet implemented) |

---

## Stability Classification Governance

### How Upgrages Work

- **Experimental → Candidate:** Requires new spike or evidence milestone + PO approval. Spike 1-7 evidence package demonstrates evidence readiness for 8 capabilities.
- **Candidate → Stable:** Requires implementation complete + test suite pass + Quality Gates 1-3 verified + PO approval.
- **Stable → Frozen:** Requires freeze declaration (per`Engineering_Question_Freeze_Checklist.md`) + Production Ready classification confirmed.

### How Downgrades Work

- Any downgrade requires: (1) New evidence contradicting previous classification, (2) New Engineering Question recommendation, (3) PO approval, (4) Contract deprecation lifecycle if field is already in contract.
- **Frozen capabilities**: Downgrade requires full architecture contract MAJOR version change + deprecation lifecycle + PO approval.
- Stable capabilities: Downgrade to Candidate or Experimental permitted with new evidence.
- Candidate capabilities: Downgrade to experimental or rejected with new evidence.

### Consistency with Evidence

| Document | Consistency Check | Status |
|---|---|---|
| Spike 2 Classification | 8 Production Ready = 8 Candidate | ✅ Consistent — all Production Ready receive Candidate stability |
| Spike 3 Rules | All canonical candidates have deterministic rules | ✅ Consistent |
| Spike 4 Contract Impact | All Candidate upgrades result in MINOR contract change | ✅ Consistent |
| Spike 5 Consumer Value | All candidates have consumer value justification | ✅ Consistent |
| Spike 6 Implementation Architecture | All candidates have module location and API definition | ✅ Consistent |
| Spike 7 Increment Definition | All capabilities mapped to Increment 4 | ✅ Consistent |
| Final Architecture Review | All eligible capabilities pass architecture audit | ✅ Consistent |
| Engineering Governance | Upgrades follow lifecycle. No bypass (without evidence) stages. | ✅ Consistent |

---

## Expected Upgrade Path (Increment 4 Implementation)

After EQ-0019 Increment 4 implementation completes:

| Upgrade | Action |
|---|---|
| All 8 Candidate capabilities → Stable | Upon: Implementation passes all 20 tests, production fixture verification, Quality Gates 1-2, PO approval |
| Contract v1.0 → v1.1.0 (MINOR) | Per Spike 4 findings: 9 new optional fields, 0 required pauses, backward compatibility preserved |

These upgrades are the next natural step after implementation, but the stability classifications remain at Candidate until implementation is complete.

---

## Document Control

| Property | Value |
|---|---|
| **Document ID** | EQ-0019-CAP-STABILITY-MATRIX-01 |
| **Status** | ACTIVE |
| **Version** | 1.0 |
| **Last Updated** | 2026-07-25 |
| **Owner** | Project Owner |
| **Governance** | Engineering Governance v1.0 |