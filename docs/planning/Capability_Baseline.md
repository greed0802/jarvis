# Capability Baseline

Version: 1.0

---

## Approval Metadata

| Field | Value |
|-------|-------|
| **Status** | Accepted |
| **Owner** | Project Owner |
| **Effective** | 2026-07-22 |
| **Supersedes** | None |
| **Sprint Reference** | CB-0001 |

---

## Purpose

This document defines the Capability Baseline that governs all Capability Era engineering in the Jarvis Platform.

It is the canonical reference for:

- What a capability is and what it is not
- The standard capability lifecycle
- Acceptance and Freeze criteria
- Evidence and regression requirements
- Promotion rules between lifecycle states

Any capability implemented in Jarvis SHALL conform to this baseline unless an explicit ADR amends it.

---

## Scope

### What This Governs

- Capability lifecycle management
- Readiness assessment (evidence, implementation)
- Freeze criteria and release quality gates
- Evidence requirements for claiming readiness
- Regression expectations
- Promotion rules between lifecycle states

### What This Does NOT Govern

- Architecture — governed by Vision, Principles, Blueprint, Platform Kernel, and accepted ADRs
- Engineering Questions — governed by Engineering Governance
- Contracts — governed by EQ-0012 contract standards and the Evidence Contract framework
- Repository structure — governed by ADR-0012
- Quality gates — governed by the Quality Assurance Constitution

---

## What Is a Capability

A capability is a discrete, user-valuable unit of platform functionality.

A capability:

- Provides direct, tangible value to users or downstream consumers
- Has defined scope and acceptance criteria
- Has measurable completeness
- Has a lifecycle state

A capability is NOT:

- An architectural component (engines, frameworks, runtime services are not capabilities)
- An internal implementation detail
- A library or utility
- An experiment or investigation

---

## Capability Lifecycle

Every capability progresses through a defined lifecycle. Capabilities must not remain permanently in any intermediate state — they must reach a terminal state.

### Lifecycle States

```
Discovery
    ↓
Evaluation
    ↓
Project Owner Decision
    ↓
Candidate
    ↓
Active Investigation (if evidence gaps exist)
    ↓
Approved for Implementation
    ↓
Active (implementation in progress)
    ↓
Frozen (increments complete, under maintenance)
    ↓
Completed (all increments delivered, milestone closed)
```

Or, at any stage before Completed:

```
Rejected
Deferred
Superseded
```

### State Definitions

| State | Meaning | Exit Criterion |
|-------|---------|----------------|
| **Discovery** | Identified as a potential capability from production evidence, engineering backlog, or user needs | Recorded in a Capability Discovery document |
| **Proposal** | Formally documented with scope, stakeholders, and preliminary assessment | Entered into Capability Evaluation |
| **Candidate** | Evaluated against criteria. Awaiting Project Owner Decision. | Project Owner decision rendered |
| **Approved** | Project Owner has selected this capability for implementation | Scope defined, dependencies identified |
| **Active Investigation** | An Engineering Question or spike is underway to resolve evidence gaps | Gaps resolved or determined irreconcilable |
| **Approved for Implementation** | Evidence is sufficient. Authorization confirmed. | Implementation begins |
| **Implemented** | Production code, tests, documentation delivered. First increment complete. | Increment accepted |
| **Frozen Sub-capability** | Increment scope frozen. Public contract established. Consumers may depend. | Waits for next capability increment or dependency to advance |
| **Completed** | All increments delivered. Capability is part of the stable platform. | Terminal state reached |

### Terminal States

| State | Meaning |
|-------|---------|
| **Completed** | Successfully implemented, all increments complete |
| **Rejected** | Deliberately not pursued; reason recorded |
| **Deferred** | Valid but not currently prioritized; may be revisited |
| **Superseded** | Replaced by another approach or capability; reference to successor recorded |

---

## Readiness Checkpoints

Capabilities pass through distinct gauges. They do not conflate.

| Checkpoint | Definition |
|------------|------------|
| **Evidence Ready** | Sufficient evidence exists to implement without guessing. Engineering Questions answered. Domain rules documented. Feature traceability established. |
| **Implementation Ready** | Project Owner has selected the capability. Scope defined. Dependencies satisfied. Resources identified. |

Evidence Readiness is a precondition. It does not authorize implementation.

---

## Capability Evaluation Criteria

Every candidate capability is evaluated against four axes:

| Axis | Question |
|------|----------|
| **User Value** | Does this provide direct value to professional users or downstream consumers? |
| **Engineering Effort** | Can this be implemented with minimal code and zero speculative features? |
| **Evidence Completeness** | Does existing evidence answer practical engineering questions without a separate investigation? |
| **Architectural Impact** | Can this be implemented without new engines, frameworks, runtime components, or ADRs? |

Prefer capabilities that score **High User Value + Low Effort + High Evidence + Zero Architectural Impact**.

Capabilities that require architectural expansion are not disqual ified — but they require much stronger justification.

---

## Freeze Criteria

A capability in the **Implemented** state may become **Frozen Sub-capability** when:

1. All delivered increments pass their own acceptance criteria.
2. Evidence contract is stable and versioned.
3. Regression tests pass against the authoritative fixture(s).
4. At least one real consumer exercises the capability.
5. No open Engineering Questions remain within the scope of the delivered increments.
6. An architecture audit confirms no drift from the approved scope.

Freeze means:
- The delivered evidence and contract are stable.
- Consumers may depend on the contract.
- The capability may receive further increments in the future.
- A new investigation, Engineering Question, or Project Owner decision may add new work.

Freeze is NOT:
- A claim of permanent stability
- A prohibition on future expansion
- An endorsement of future features

---

## Regression Requirements

Regression tests SHALL be committed alongside production code.

Every capability increment SHALL:

- Introduce at least one regression test.
- Document test counts.
- Demonstrate that existing tests still pass.
- Update fixture metadata when fixtures change.

Regression is enforced by the repository quality verification tooling.

---

## Evidence and Promotion

Production evidence may be admitted only from sources of:

- Answered Engineering Questions (spike reports, traces)
- Documented domain rules with identified authority
- Field observations backed by fixture data
- Verifiable deterministic output

Claims about determinism, immutability, or contract stability require executable verification.

Promotion from a lower lifecycle state to a higher one requires explicit Project Owner approval.

---

## Governance

This baseline works with:

- `Capability_Register.md` — runtime record of current capability state
- `Capability_Roadmap.md` — sequencing and dependency governance
- `Capability_Discovery_XXX.md` — immutable discovery snapshots
- `Capability_Evaluation_XXX.md` — immutable evaluation records
- Individual Engineering Questions (EQ-XXXX)

The baseline does not supersede, rewrite, or violate repository architecture.

---

## Document Classification

| Document Type | Examples | Mutable? |
|---------------|----------|:--------:|
| **Architecture** | Vision, Principles, Blueprint, Kernel, ADRs | No |
| **Governance baseline** | Capability Baseline, Roadmap | Yes (by amendment only) |
| **Operational artifacts** | Capability Register, Implementation Status | Yes |
| **Historical artifacts** | Capability Discovery/Eval snapshots, Engineering Questions | No |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `docs/planning/Capability_Register.md` | Current capability states (single source of truth) |
| `docs/planning/Capability_Roadmap.md` | Sequencing and dependency governance |
| `docs/planning/Capability_Dependency_Graph.md` | Visual dependency map |
| `docs/planning/Capability_Discovery_001.md` | Immutable snapshot of first discovery |
| `docs/planning/Capability_Evaluation_001.md` | First evaluation and PO decision record |
| `docs/00_Vision.md` | Where Jarvis goes |
| `docs/01_Principles.md` | Governing principles |
| `docs/02_System_Blueprint.md` | High-level architecture |
| `docs/25_Roadmap.md` | Product roadmap |
| `docs/26_Implementation_Status.md` | Implementation tracker |

---

## Engineering Philosophy

The Capability Baseline embodies:

- Documentation Before Code
- Evidence Before Promotion
- Explicit Over Magic
- Deterministic Over Convenience
- Maintainability Over Novelty
- YAGNI

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1 | 2026-07-22 | Created. Establishes the Capability Baseline. Sprint CB-0001. |