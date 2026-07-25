# Implementation Governance

**Document:** Implementation_Governance.md

**Status:** Active

**Version:** 1.0

**Authority:** EQ-0019 (Permanently Frozen)

**Applies To:** All Implementation Packages (IP) in the Jarvis repository.

---

## Purpose

This document defines the governance framework for **Implementation Packages** in the Jarvis repository.

An Implementation Package (IP) is the authoritative vehicle for transforming a frozen Engineering Question disposition into production code, tests, contracts, and verified evidence.

This governance ensures that every implementation is:

- traceable to a frozen Engineering Question
- bounded by frozen architecture
- verified against public contracts
- independently reproducible
- documented for future contributors

This is a **governance document**.

It is NOT an implementation specification.

It does NOT define any particular Implementation Package content.

---

## Relationship to Existing Governance

| Governance Layer | Purpose | Relationship |
|------------------|---------|--------------|
| **AGENTS.md** | Repository engineering rules | Authority root |
| **Engineering Governance** (`Engineering_Governance.md`) | Engineering Question lifecycle | IPs are downstream consumers of frozen EQs |
| **Quality Assurance Constitution** (`Quality_Assurance_Constitution.md`) | Verification gates | IPs must pass Quality Gates 1-5 |
| **Engineering Question Freeze Checklist** | EQ freeze requirements | Frozen EQ is a required IP input |
| **Repository Governance Automation** (`Repository_Governance_Automation.md`) | Automated compliance | IPs must comply with automated governance validation |
| **Implementation Governance** (this document) | Implementation Package lifecycle | THIS DOCUMENT |

---

## Scope

This governance applies to:

- All Implementation Packages created in the Jarvis repository
- Any production code, tests, contracts, or evidence generated under an IP
- The lifecycle from IP creation through IP freeze
- All contributors, AI agents, and automated systems executing implementation work

This governance does NOT apply to:

- Engineering Questions (governed by Engineering Governance)
- ADRs (governed by the ADR process)
- Spike investigations (governed by Engineering Governance)
- Routine maintenance, bug fixes, or documentation updates outside an IP

---

## Implementation Package Lifecycle

```
Draft
  │
  ▼
Active
  │
  ▼
Implementation Complete
  │
  ▼
Verification Complete
  │
  ▼
Frozen
```

### Draft

**Purpose:** Define the implementation scope before any production code is written.

**Entry Criteria:**
- Frozen Engineering Question with approved disposition
- Frozen architecture (applicable ADRs, contracts)
- Project Owner authorization to implement

**Activities:**
- Create IP authority document
- Define acceptance criteria traceable to EQ disposition
- Identify all inputs (see § Required Inputs)
- Identify all expected outputs (see § Required Outputs)
- Identify affected consumers and contracts
- Assess architecture impact

**Exit Criteria (→ Active):**
- IP authority document created and reviewed
- Acceptance criteria documented
- Inputs identified and available
- Outputs enumerated
- Architecture impact assessed
- Project Owner approval obtained

---

### Active

**Purpose:** Execute the implementation.

**Entry Criteria:**
- Draft phase completed and approved
- IP authority document in Active status

**Activities:**
- Write production code
- Write tests
- Verify against acceptance criteria
- Execute real fixture demonstration
- Perform architecture audit
- Document any deviations from architecture
- Update documentation

**Constraints:**
- Implementation must conform to the scope defined in Draft phase
- Scope changes require Draft re-approval
- No speculative features beyond defined scope
- Architecture deviations require ADR or EQ re-review

**Exit Criteria (→ Implementation Complete):**
- All production code written
- All tests committed
- Real fixture demonstration passed
- Architecture audit performed
- No blocking architecture violations discovered
- Documentation synchronized

---

### Implementation Complete

**Purpose:** Verify the implementation against all acceptance criteria, contracts, and governance requirements.

**Entry Criteria:**
- Active phase completed
- All code and tests written
- Real fixture demonstration successful

**Activities:**
- Execute full test suite
- Run verification tooling
- Verify contract compliance
- Verify determinism
- Verify documentation synchronization
- Verify version consistency
- Generate implementation evidence
- Generate regression evidence

**Exit Criteria (→ Verification Complete):**
- All acceptance criteria met
- Test suite passes
- Contracts verified
- Determinism verified
- Documentation synchronized
- Version consistent across all required locations
- Implementation evidence documented
- Regression evidence documented
- Engineering debt register updated

---

### Verification Complete

**Purpose:** Final review and freeze approval.

**Entry Criteria:**
- Verification Complete phase completed
- All verification artifacts generated

**Activities:**
- Architecture review
- Consumer readiness assessment
- Project Owner review
- Freeze decision

**Exit Criteria (→ Frozen):**
- All Quality Gates passed (G0–G5)
- Architecture review passed
- Consumer readiness assessed
- Engineering debt acknowledged
- Project Owner approved
- Freeze recorded

---

### Frozen

**Purpose:** Permanent record of completed implementation.

**Characteristics:**
- Immutable (factual corrections only)
- No further development under this IP
- Implementation deployed or ready for release
- Evidence available for future IPs and consumers

**Freeze Effects:**
- IP authority document status set to Frozen
- Production code becomes reference implementation
- Tests become regression baseline
- Evidence becomes reference for future implementation
- Future changes require a new IP

---

## Required Inputs

Every Implementation Package MUST have the following inputs available before entering the Draft phase:

### Frozen Engineering Question

- The Engineering Question whose disposition authorizes this implementation
- The EQ must be Frozen (Completed with approved disposition)
- The EQ disposition must explicitly authorize implementation

**Authority Reference:**
- Engineering Governance § Investigation Lifecycle (Step 8: Implementation)
- EQ Freeze Checklist § Project Owner Approval Recorded

### Frozen Architecture

- All applicable ADRs
- Architecture documents specifying the implementation context
- Platform Kernel boundaries
- Component ownership model

**Purpose:** Ensures implementation conforms to documented architecture.

### Public Contracts

- All applicable public contracts (frozen or candidate)
- Evidence contracts
- Output contracts
- Consumer contracts

**Purpose:** Ensures implementation honors all contract commitments.

### Acceptance Criteria

- Derived from the Engineering Question disposition
- Defined in the IP authority document
- Must be objectively verifiable
- Must be testable

### Consumer Analysis (when applicable)

- Identification of affected consumers
- Consumer requirements
- Backward compatibility requirements
- Migration path (if breaking changes)

---

## Required Outputs

Every Implementation Package MUST produce the following outputs before requesting Freeze.

### Production Code

- All code implementing the accepted capabilities
- Located in `src/` (or other designated production directory)
- Conforms to architecture and contracts
- Deterministic where specified

### Tests

- Comprehensive test suite under `tests/`
- Tests for all acceptance criteria
- Tests for contract invariants
- Tests for edge cases and error conditions
- Tests for determinism (where applicable)
- Real fixture demonstration tests

### Implementation Evidence

- Evidence that all acceptance criteria are met
- Traceability: Acceptance Criterion → Test → Result
- Evidence of real fixture demonstration
- Evidence of architecture compliance

**Format:** IP package under `docs/implementation/` or `docs/engineering/evidence/`.

### Regression Evidence

- Evidence that existing behavior is preserved
- Full test suite results (PASS counts, comparison against baseline)
- Contract verification results
- Consumer compatibility evidence (where applicable)

### Updated Documentation

- Architecture documents (if implementation revealed gaps)
- Public contracts (if implementation required extension)
- Consumer documentation (if API changed)
- Knowledge base (if new capabilities promoted)
- Implementation Status updates

### Version Updates

- Version identifiers updated consistently across:
  - Version module
  - README
  - Implementation Status
  - Release documentation
  - Contracts (if applicable)
  - Capability register

### Engineering Debt Register

- All known engineering debt documented
- Severity and impact assessed
- Freeze-blocking debt identified
- Planned resolution documented

---

## Authority

### What an Implementation Package MAY Do

An Implementation Package MAY:

- Create new production code files in `src/`
- Create new test files in `tests/`
- Extend existing production types with new fields (subject to contract compatibility)
- Add new public functions (subject to architecture review)
- Create new contracts or extend existing contracts (subject to ADR if architecture change)
- Create implementation evidence packages
- Update documentation to reflect implementation
- Update version identifiers
- Register engineering debt

An Implementation Package MAY:

- Reference frozen Engineering Questions as implementation authority
- Reference frozen ADRs as architecture constraints
- Reference frozen contracts as output requirements
- Reference previous Implementation Packages as evidence or dependency

### What an Implementation Package MUST NOT Do

An Implementation Package MUST NOT:

- **Redesign architecture.** Implementation follows architecture. Architecture changes require ADR.
- **Replace Engineering Questions.** IPs do not investigate. IPs implement.
- **Introduce speculative features.** Only capabilities approved by the frozen EQ disposition may be implemented.
- **Modify frozen contracts without version extension.** Contracts may be extended (MINOR/PATCH) but not broken (MAJOR requires new contract version).
- **Silently deviate from acceptance criteria.** Any deviation must be documented and re-approved.
- **Skip verification gates.** All applicable Quality Gates must pass before freeze.
- **Hide engineering debt.** Known debt must be documented in the Engineering Debt Register.
- **Modify frozen architecture documents.** Architecture is governed by the ADR process, not by implementation.
- **Create hidden production dependencies.** No production code may depend on `docs/`, `tools/`, or `data/reports/` unless explicitly approved.

---

## Completion Criteria

An Implementation Package is **Complete** when:

- All acceptance criteria are met
- All required outputs are produced
- Production code is committed
- Tests are committed
- Real fixture demonstration evidence exists
- Architecture audit confirms compliance
- Documentation is synchronized

**Completion Status:** `Implementation Complete` in the IP lifecycle.

---

## Freeze Criteria

An Implementation Package may be **Frozen** when:

### Gate 1 — Mechanical Verification Passed

- Full test suite passes
- Acceptance criteria all met
- Determinism verified (where applicable)
- Contracts verified against implementation
- Documentation synchronized
- Version consistent

### Gate 2 — Architecture Verification Passed

- Responsibility boundaries preserved
- No hidden coupling introduced
- Contract integrity maintained
- Consumer independence preserved
- ADR compliance confirmed
- YAGNI compliance confirmed

### Gate 3 — Consumer Readiness Verified

- Stable public API
- Import stability
- Package boundaries respected
- Contract maturity assessed
- Consumer documentation available
- Backward compatibility assessed

### Gate 4 — Repository Consistency Verified

- Documentation matches implementation
- Version consistent across all locations
- Contracts match public API
- Test coverage adequate
- Knowledge base aligned
- Capability register consistent

### Gate 5 — Release Readiness Verified

- All previous gates passed
- Engineering debt register reviewed
- No critical debt
- All registers synchronized
- Release notes prepared (if applicable)

### Project Owner Approval

- Freeze request submitted with evidence
- Project Owner approves

---

## Relationship to Future Implementation Packages

### Sequential Independence

Each Implementation Package is independent.

Future IPs:

- MAY depend on outputs of previous frozen IPs
- MUST NOT modify frozen IPs
- MUST reference previous IPs as frozen dependencies (not mutable imports)
- MAY extend capabilities implemented by previous IPs (via new EQ disposition)

### Versioning Coordination

When IPs affect the same contracts or modules:

- Versioning MUST be coordinated across IPs
- Conflicting version changes require sequencing or merging
- The Capability Roadmap defines IP sequencing

### Dependency Chain

```
EQ Freeze Disposition
       │
       ▼
Implementation Package (current)
       │
       ▼
Frozen Implementation
       │
       ▼
Evidence for Future EQ / Future IP
       │
       ▼
Next Implementation Package
```

This chain ensures:

- Every IP traces to a frozen EQ
- Every frozen IP becomes evidence for future work
- No IP depends on non-frozen work
- Implementation proceeds in deterministic, auditable increments

### Scope Boundaries

An IP MUST NOT:

- Implement capabilities not authorized by its source EQ
- Expand its scope to cover work that belongs in a separate IP
- Preempt future IPs by implementing speculative features "in case they are needed"

**Scope violations require:**

1. Documentation of the scope deviation
2. Assessment of whether it constitutes a new IP
3. Project Owner decision on scope adjustment or new IP creation

---

## IP Authority Document Template

Every Implementation Package MUST have an authority document following this structure:

```
# IP-NNNN — [Title]

## Status
[ Draft | Active | Implementation Complete | Verification Complete | Frozen ]

## Source Engineering Question
[ EQ-XXXX — Title ]

## Source EQ Disposition
[ Summary of the approved disposition ]

## Architecture Constraints
- ADR-XXXX: [constraint description]
- ADR-XXXX: [constraint description]

## Applicable Contracts
- [Contract name] vX.Y.Z
- [Contract name] vX.Y.Z

## Acceptance Criteria
1. [Criterion 1 — objectively verifiable]
2. [Criterion 2 — objectively verifiable]
3. [Criterion 3 — objectively verifiable]

## Scope
### In Scope
- [Capability or module to implement]
- [Capability or module to implement]

### Out of Scope
- [Capability or module explicitly excluded]
- [Capability or module explicitly excluded]

## Inputs
- [Required input 1]
- [Required input 2]

## Outputs
- [Expected output 1]
- [Expected output 2]

## Consumers Affected
- [Consumer 1]
- [Consumer 2]

## Risk Assessment
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Engineering Debt (preliminary)
- Known constraints documented
- Identified limitations noted

## Freeze Checklist
[Checklist to be completed before freeze request]

## Document Control
Version | Date | Status | Owner
```

---

## Implementation Governance Version History

| Version | Date | Changes | Authority |
|---------|------|---------|-----------|
| 1.0 | 2026-07-25 | Initial Implementation Governance established | EQ-0019 |

---

## Success Criteria

Implementation Governance is successful when:

✅ Every implementation traces to a frozen Engineering Question disposition

✅ Implementation Packages are the single authoritative vehicle for production code

✅ All required inputs are available before implementation begins

✅ All required outputs are produced before freeze

✅ Quality Gates are consistently applied across all implementations

✅ Future implementation work references this document for process, authority, and constraints

✅ No implementation-specific assumptions exist in this framework

✅ Framework remains stable across repository evolution

---

## References

- `docs/engineering/Engineering_Governance.md` — Engineering Question lifecycle
- `docs/engineering/Quality_Assurance_Constitution.md` — Verification gates
- `docs/engineering/Engineering_Question_Freeze_Checklist.md` — EQ freeze requirements
- `docs/engineering/Repository_Governance_Automation.md` — Automated compliance
- `docs/engineering/Engineering_Register.md` — EQ registration and status
- `docs/engineering/AI_Agent_Operating_Manual.md` — Operational workflow
- `AGENTS.md` — Repository engineering rules

---

## Document Control

**Owner:** Project Owner  
**Review Schedule:** Upon governance evolution proposal  
**Distribution:** All contributors, AI agents, CI systems  
**Applies To:** All Implementation Packages in the Jarvis repository