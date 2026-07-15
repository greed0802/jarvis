# EQ-0013 Spike 2: Validation Rule Taxonomy

**Evidence Report ID:** EQ-0013-S2-EVD
**Date:** 2026-07-15
**Status:** Complete
**Authority:** EQ-0013 (Validation Engine Investigation)
**Contract Version:** BOQ Intelligence Public Evidence Contract v1.0.0
**Engineering Boundary:** EQ-0011 (Observe/Reconstruct/Detect)
**Baseline:** EQ-0013 Spike 1 (22 rules)

---

## Executive Summary

Spike 2 formalized taxonomy, lifecycle, governance, provenance, dependency graph, and version compatibility for the 22 validation rules discovered in Spike 1. The Validation Rule Registry is now a governed engineering artifact with permanent Rule IDs, complete provenance, and stable dependency relationships.

**Key Findings:**
- **4 categories validated** (Structural, Consistency, Completeness, Detection)
- **4 categories rejected** (Assessment, Recommendation, Financial, Reference)
- **6 lifecycle states defined** (Candidate → Approved → Implemented → Verified → Deprecated → Retired)
- **7 finding types formalized** (presence, shape, count, ratio, range, discrepancy, flag)
- **5 eligible consumers identified** (CheckMate, Formatter, Builder, O&A, Reporting)
- **22/22 rules have complete provenance** (100%)
- **14/15 verification checks passed** (93%)

---

## Investigation Objective

**Question:** What engineering taxonomy, lifecycle, and governance model should manage deterministic validation rules while preserving contract stability and the EQ-0011 boundary?

**Not Asked:**
- What new validation rules exist (Spike 1 already discovered all rules)
- How to implement validations (belongs to future spikes)
- What consumers need (consumer-independent governance)

---

## Methodology

### Governance-First Approach

1. **Load Spike 1 Registry** — 22 rules baseline (no new rules permitted)
2. **Formalize categories** — Evidence-backed taxonomy from Spike 1 discovery
3. **Define lifecycle** — Candidate → Approved → Implemented → Verified → Deprecated → Retired
4. **Establish identity policy** — Permanent Rule IDs (never reused)
5. **Document provenance schema** — Required fields for all rules
6. **Build dependency graph** — Evidence fields → Rules → Categories → Finding types → Consumers
7. **Define version compatibility** — Contract vs Rule vs Engine version relationships
8. **Establish registry governance** — Adding, modifying, deprecating, retiring rules
9. **Verify taxonomy integrity** — 15 automated checks

---

## Rule Taxonomy

### Validated Categories (4)

#### 1. Structural (6 rules)

**Definition:** Validations that verify presence, type, shape, or range of evidence fields.

**Scope:** Single-field checks against Contract invariants.

**Rules:** V-001, V-002, V-003, V-010, V-011, V-012

**EQ Source:** EQ-0010 (Increments 1-2), EQ-0012 (Contract invariants)

**Boundary:** Always BoundaryClass.Observation — no assessment, no recommendation.

**Example Finding:** "Reports missing or unexpected keys" (V-002)

---

#### 2. Consistency (3 rules)

**Definition:** Validations that verify arithmetic or logical relationships between evidence fields.

**Scope:** Multi-field checks that detect internal contradictions.

**Rules:** V-004, V-005, V-006

**EQ Source:** EQ-0010 (Increment 1 cross-field dependencies)

**Boundary:** BoundaryClass.Observation or BoundaryClass.Relationship — no assessment.

**Example Finding:** "Reports discrepancy magnitude if sums don't match" (V-004)

---

#### 3. Completeness (3 rules)

**Definition:** Validations that calculate data population ratios from aggregate statistics.

**Scope:** Single-field ratios describing column completeness.

**Rules:** V-007, V-008, V-009

**EQ Source:** EQ-0010 (boq_statistics completeness indicators)

**Boundary:** Always BoundaryClass.Observation — ratios describe, not assess.

**Example Finding:** "Reports completeness ratio (0.0 to 1.0)" (V-007)

---

#### 4. Detection (6 rules)

**Definition:** Validations that observe patterns in EQ-0011 detection evidence.

**Scope:** Checks on optional Increment 3 detection evidence fields.

**Rules:** V-013, V-014, V-015, V-016, V-017, V-018

**EQ Source:** EQ-0011 (Increment 3 detection evidence)

**Boundary:** Always BoundaryClass.Detection — findings, not recommendations.

**Example Finding:** "Reports skip count or None if unavailable" (V-014)

---

### Rejected Categories (4)

#### 1. Assessment (1 rule) — REJECTED

**Definition:** Validations that assess professional quality or correctness.

**Rejection Reason:** Crosses EQ-0011 boundary (Assess/Judge).

**Rule:** V-901

**Prohibited Verbs:** assess, judge, evaluate, rate, rank, score

---

#### 2. Recommendation (1 rule) — REJECTED

**Definition:** Validations that recommend corrective actions.

**Rejection Reason:** Crosses EQ-0011 boundary (Recommend).

**Rule:** V-902

**Prohibited Verbs:** recommend, suggest, advise, propose, should

---

#### 3. Financial (1 rule) — REJECTED

**Definition:** Validations that check financial values.

**Rejection Reason:** No cost/price evidence in Contract v1.0.

**Rule:** V-801

---

#### 4. Reference (1 rule) — REJECTED

**Definition:** Validations that check external references.

**Rejection Reason:** No drawing/specification evidence in Contract v1.0.

**Rule:** V-802

---

## Rule Lifecycle

### Lifecycle States (6)

```
Candidate
    ↓
Approved
    ↓
Implemented
    ↓
Verified
    ↓
Deprecated
    ↓
Retired
```

### State Transitions

| State | Entry Criteria | Exit Criteria | Next State | Governance |
|-------|----------------|---------------|------------|------------|
| **Candidate** | Rule ID assigned, provenance documented, boundary classified, category assigned | Evidence report frozen, category validated, boundary verified, PO approval | Approved | Spike discovery + Evidence Report |
| **Approved** | PO Gate 2 approval, category confirmed, boundary confirmed, provenance complete | Implementation complete, passes verification, deterministic confirmed | Implemented | Gate 2 approval |
| **Implemented** | Production code exists, consumes Contract v1.0 only, follows EQ-0011, deterministic | Verification confirms spec match, invariants pass, boundary compliant, consumer-independent | Verified | Implementation + Verification |
| **Verified** | Implementation verified, verification status VERIFIED, anti-drift passes, compliance passes | Rule no longer needed, replaced by successor, evidence field removed | Deprecated | ADR or Contract evolution |
| **Deprecated** | Deprecation notice issued, successor identified, timeline established, migration guidance provided | Deprecation period expired, no active consumers, successor verified | Retired | MINOR Contract version |
| **Retired** | Deprecation expired, removed from active registry, historical record preserved | (terminal state) | None | Historical preservation |

### Forbidden Transitions (7)

- Candidate → Retired (skip lifecycle)
- Candidate → Deprecated (skip lifecycle)
- Approved → Retired (skip implementation)
- Implemented → Candidate (reverse)
- Verified → Candidate (reverse)
- Deprecated → Approved (undeprecate)
- Retired → Approved (revive retired)

---

## Rule Identity Policy

### Permanence

**Rule IDs are forever.** Once assigned, never reassigned.

### Format

**V-NNN** where NNN is sequential from 001-999.

### Reservation

| Range | Purpose |
|-------|---------|
| 001-899 | Implementable rules (Supported + Multiple Fields) |
| 900-999 | Rejected rules (Boundary Violation, Insufficient Evidence) |

### Retirement

Retired rules retain their ID permanently in historical index.

### Replacement

A successor rule receives a **NEW Rule ID**. Never reuse the retired ID.

### Historical Preservation

All rules (including rejected/retired) remain in registry history.

### Design Note: V-801 and V-802

V-801 and V-802 (Insufficient Evidence) fall in the implementable range (001-899) because they were discovered in Spike 1 before the reservation policy was formalized in Spike 2. This violates the ideal policy but preserves the permanence principle — Rule IDs cannot be changed retroactively. Future rejected rules will use 900-999.

**Lesson:** Reservation policies should be established before Rule ID assignment begins.

---

## Rule Provenance Schema

### Required Fields (13)

Every rule must document:

1. `rule_id` — Permanent identifier
2. `rule_version` — Rule evolution (starts at 1.0.0)
3. `category` — Taxonomy classification
4. `description` — Human-readable purpose
5. `evidence_fields` — Contract fields consumed
6. `boundary_class` — EQ-0011 classification
7. `contract_version` — Evidence dependency
8. `eq_source` — Engineering Question origin
9. `introduced_by` — Spike that discovered rule
10. `deterministic_finding` — Output specification
11. `rationale` — Why rule exists
12. `status` — Lifecycle state
13. `verification_status` — Implementation verification state

### Optional Fields (6)

14. `validation_engine_version` — First executable implementation
15. `dependency_rules` — Other rules this depends on
16. `deprecation_date` — When deprecated
17. `retirement_date` — When retired
18. `successor_rule_id` — Replacement rule (if applicable)
19. `consumers` — Known consumers using this rule

### Governance

Missing provenance = incomplete rule. Rules cannot transition Candidate → Approved without complete required fields.

---

## Rule Dependency Graph

### Dependency Model

```
Evidence Field
    ↓
Validation Rule
    ↓
Rule Category
    ↓
Finding Type
    ↓
Eligible Consumers
```

### Finding Types (7)

| Type | Description |
|------|-------------|
| **presence** | Boolean: field exists / None |
| **shape** | List: missing/unexpected keys |
| **count** | Integer: occurrence frequency |
| **ratio** | Float: 0.0-1.0 completeness |
| **range** | Tuple: (min, max) distribution |
| **discrepancy** | Integer: deviation from expected |
| **flag** | List: invalid elements found |

### Eligible Consumers (5)

- CheckMate (BOQ validation application)
- Formatter (BOQ export formatting)
- Builder (Builder QA)
- O&A (Omission & Addition analysis)
- Reporting (BOQ reports)

### Purpose

1. **Impact analysis** — When Contract evolves, identify affected rules
2. **Regression planning** — When rule changes, identify affected consumers
3. **Dependency visibility** — Consumers know which rules use which evidence

---

## Version Compatibility Rules

### Contract vs Rule

| Contract Change | Rule Impact | Rule Version |
|-----------------|-------------|--------------|
| PATCH (documentation fix, clarification) | NONE — Rule unchanged | No increment |
| MINOR (new optional field, field deprecation) | PATCH (new rule added) or MINOR (rule deprecated) | Depends on change |
| MAJOR (remove/rename/retype required field) | MAJOR — Rule retired or replaced | New Rule ID |

### Rule vs Engine

| Rule Change | Engine Impact | Engine Version |
|-------------|---------------|----------------|
| Rule added | New capability | MINOR |
| Rule deprecated | Marked deprecated | MINOR |
| Rule retired | Functionality removed | MAJOR |
| Finding changed | Breaking change | MAJOR |
| Category changed | Structural change | MAJOR |
| Verification status changed | Non-functional | PATCH |

### Independent Versions

**Contract Version**, **Validation Rule Version**, and **Validation Engine Version** are independent engineering concepts.

A MAJOR Contract change may not require a MAJOR Engine change if all affected rules are already deprecated.

---

## Registry Governance

### Adding Rules

**Process:**
1. Rule discovered via Spike investigation
2. Evidence Report documents candidate rule
3. Category validated (Spike 2 taxonomy)
4. Boundary classification confirmed
5. Provenance complete (all required fields)
6. Project Owner approval (Gate 2)
7. Added to registry as APPROVED

**Authority:** Engineering Question + Spike + Project Owner Approval

**Traceability:** Every addition traces to EQ number + Spike number

---

### Modifying Rules

**Process:**
1. Change proposal via Engineering Question
2. Impact analysis (Contract, Engine, Consumers)
3. Version increment determined
4. Project Owner approval
5. Registry updated with new rule_version

**Authority:** Engineering Question + Impact Analysis + Project Owner

**Traceability:** Every modification traces to EQ number + version change

**Forbidden Modifications:**
- Changing Rule ID (permanent identity)
- Changing boundary_class from valid to Violation
- Changing category to rejected category
- Removing required provenance fields

---

### Deprecating Rules

**Process:**
1. Deprecation notice issued (MINOR Contract or Engine update)
2. Rule status: VERIFIED → DEPRECATED
3. Deprecation reason documented
4. Migration guidance provided to consumers
5. Timeline established (consumer migration deadline)

**Authority:** ADR or Contract version evolution

---

### Retiring Rules

**Process:**
1. Deprecation period expired
2. No active consumers confirmed
3. Successor rule verified (if applicable)
4. Rule removed from active registry
5. Historical index preserved
6. Rule ID permanently retired

**Authority:** Project Owner after deprecation period

---

## Consumer Compatibility Model

### Verification Chain

1. Consumer identifies required rules
2. Consumer verifies Rule IDs present in Engine
3. Consumer verifies Contract Version compatibility
4. Consumer verifies Finding Types match expectations
5. Consumer passes Compliance Suite (EQ-0013) for contract compliance

### Compatibility Assertions

- **Rule IDs stable** — Permanent identity
- **Finding types deterministic** — Same input → same output
- **Contract version documented** — Consumer checks compatibility
- **Boundary class preserved** — No assessment/recommendation drift

---

## Verification Results

### Verification Summary

**15 checks performed:**
- 14 checks PASSED (93%)
- 1 check FAILED (7%)

### Passed Checks (14)

✓ No New Rules Invented
✓ Rule ID Uniqueness
✓ Rule ID Format
✓ Provenance Complete
✓ Categories Valid
✓ Boundary Classification
✓ Lifecycle Valid
✓ Dependency Graph Complete
✓ Dependency Fields Match
✓ No Speculative Rules
✓ Rejected Rules Documented
✓ Boundary Preservation
✓ Finding Types Valid
✓ Contract Version Consistent

### Failed Checks (1)

✗ Rule ID Reservation Policy

**Issue:** V-801 and V-802 (Insufficient Evidence) are in implementable range (001-899) instead of rejected range (900-999).

**Resolution:** Acceptable design decision. Rule IDs are permanent and cannot be changed retroactively. V-801 and V-802 were assigned before the reservation policy was formalized. Future rejected rules will use 900-999. This is documented as a design note rather than a governance violation.

**Lesson:** Establish reservation policies before assigning Rule IDs.

---

## Deliverables

### Generated Artifacts

1. **Rule Taxonomy** — `data/reports/eq0013_spike2_rule_taxonomy.json`
   - 8 categories (4 validated + 4 rejected)
   - 6 lifecycle states with transitions
   - Identity policy, provenance schema, version compatibility rules
   - Registry governance procedures

2. **Dependency Graph** — `data/reports/eq0013_spike2_dependency_graph.json`
   - 22 rule entries
   - Evidence field → Rule → Category → Finding Type → Consumers mapping
   - 7 finding types, 5 eligible consumers

3. **Verification Report** — `data/reports/eq0013_spike2_verification.json`
   - 15 verification checks
   - 14/15 passed (93%)
   - Detailed issue reporting

4. **Taxonomy Tool** — `tools/eq0013_spike2_validation_rule_taxonomy.py`
   - Executable Python tool
   - Generates taxonomy + dependency graph
   - Reproducible artifact generation

5. **Verification Audit** — `tools/eq0013_spike2_verification_audit.py`
   - Executable Python tool
   - 15 automated integrity checks
   - Anti-drift tooling

---

## Key Insights

### 1. Categories Are Evidence-Backed

All 4 validated categories (Structural, Consistency, Completeness, Detection) trace directly to EQ-0010/EQ-0011 evidence. No speculative categories introduced.

**Implication:** Taxonomy expansion requires new EQ investigation producing new evidence.

### 2. Lifecycle Enforces Discipline

6-state lifecycle (Candidate → Approved → Implemented → Verified → Deprecated → Retired) with explicit entry/exit criteria prevents ad-hoc rule changes.

**Implication:** Rules cannot skip states or reverse without governance approval.

### 3. Rule IDs Are Permanent

Once assigned, Rule IDs never change. Retired rules preserve their ID in historical index.

**Implication:** ID assignment is a one-time, irreversible decision. Must be correct.

### 4. Provenance Is Complete

22/22 rules have complete provenance (100%). Every rule traces to EQ source + Spike + Contract version.

**Implication:** Rules without provenance cannot be approved.

### 5. Dependency Graph Enables Impact Analysis

Evidence field → Rule → Finding type → Consumers mapping supports Contract evolution impact analysis.

**Implication:** When Contract changes, affected rules and consumers are immediately identifiable.

### 6. Version Compatibility Is Independent

Contract, Rule, and Engine versions evolve independently. MAJOR Contract change may not require MAJOR Engine change.

**Implication:** Version impact must be analyzed per-component, not assumed globally.

### 7. Boundary Preservation Is Verifiable

Automated checks confirm no prohibited verbs (assess, judge, recommend) in implementable rules.

**Implication:** EQ-0011 boundary violations are detectable at governance time, not implementation time.

---

## Recommendations for Spike 3

### Validation Engine Scope & Responsibilities

Spike 3 should define:
- What belongs inside Validation Engine (rule evaluation)
- What belongs outside (consumer interpretation)
- Engine public API (how consumers interact with rules)
- Engine state management (if any)

### Engine/Consumer Boundary

Establish clear separation:
- Engine provides findings (deterministic outputs)
- Consumers interpret findings (application-specific logic)
- No consumer-specific logic in Engine

---

## Conclusion

Spike 2 successfully formalized taxonomy, lifecycle, governance, provenance, dependency graph, and version compatibility for the 22 rules discovered in Spike 1. The Validation Rule Registry is now a governed engineering artifact with:

- Permanent Rule IDs
- Complete provenance
- Evidence-backed categories
- Enforced lifecycle
- Stable dependencies
- Version compatibility rules
- Registry governance procedures

**Verification:** 14/15 checks passed (93%). 1 acceptable design note (V-801/V-802 ID placement).

**Next:** Spike 3 will define Validation Engine scope, responsibilities, and public API.

---

## Document Control

**Evidence Report ID:** EQ-0013-S2-EVD
**Status:** Complete
**Date:** 2026-07-15
**Authority:** EQ-0013 Spike 2
**Distribution:** Engineering team, Project Owner

---

**End of Evidence Report**