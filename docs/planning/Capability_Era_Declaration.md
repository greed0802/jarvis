# Capability Era Declaration

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

## Declaration

The **Repository Foundation Era** is complete and frozen.

The **Capability Engineering Era** is now declared active.

Future engineering shall prioritize user-facing capabilities over architecture, runtime, frameworks, or speculation.

---

## What Has Ended

The Repository Foundation Era established:

- Vision, Principles, System Blueprint
- Core Ontology
- Platform Kernel architecture
- 25 Architecture Decision Records
- Engineering Governance
- Quality Assurance Constitution
- Repository Structure and verification tooling
- Parser Foundation (M5, M6)
- Lifecycle test framework (M4)
- Configuration (M3)

These are **frozen infrastructure**. They shall not be modified, restructured, or extended unless a new ADR or explicit Project Owner directive requires a change.

---

## What Has Begun

The Capability Engineering Era replaces milestone-driven development with **capability-driven governance**.

The active authority documents are:

| Document | Role |
|----------|------|
| `docs/planning/Capability_Baseline.md` | Canonical reference for all capability lifecycle management |
| `docs/planning/Capability_Register.md` | Single source of truth for current capability states |
| `docs/planning/Capability_Roadmap.md` | Sequencing and dependency governance |
| `docs/planning/Capability_Dependency_Graph.md` | Visual dependency map |
| `docs/planning/Capability_Metrics.md` | Objectively measurable capability metrics |
| `docs/planning/Capability_Release_Policy.md` | Versioning, compatibility, and deprecation rules |
| `docs/planning/BOQ_Intelligence_Readiness_Report.md` | Current readiness assessment for the active strategic capability |

Every future capability shall pass through the Capability Baseline lifecycle.

No capability may be implemented without:
1. Capability Discovery (immutable snapshot)
2. Capability Evaluation
3. Project Owner Decision
4. Evidence closure (or an Engineering Question if gaps exist)

---

## Current Active Capability

| Capability | State |
|------------|:-----:|
| BOQ Intelligence | **Active** — Increments 1–3 delivered, Evidence Contract Frozen, further increments pending |

## Current Frozen Capabilities

| Capability | State |
|------------|:-----:|
| Validation Engine | **Frozen Sub-capability** — Consumer ready, EQ-0013 frozen |

## Deferred

| Capability | Reason |
|------------|--------|
| Formatter | Depends on BOQ Intelligence trusted validation |
| CheckMate | Depends on BOQ Intelligence maturity + domain rule catalog |
| Cubit Parser | Awaiting fixtures |
| PDF Parser | Insufficient evidence |
| AI-Assisted Estimation | Multiple prerequisite foundations missing |

---

## What Shall Not Change

The following boundaries are **f**rozen** as part of the Foundation:

- Architecture Documents (00–04)
- All 25 ADRs (ADR_0001 through ADR_0025)
- Public Evidence Contracts (BOQ Intelligence v1.0.0, Validation Findings v1.0.0)
- Repository Governance and Quality Constitution
- Verification Framework (tools/quality/)
- Archive policy

Capability engineering SHALL NOT:
- Modify the parser foundation
- Introduce new engines, frameworks, runtime components, or interfaces without a new ADR
- Rewrite or restructure existing architecture documents
- Reinterpret existing ADRs
- Produce any production code that violates the Quality Assurance Constitution

---

## Transition Record

| Era | Status | Effective |
|-----|:------:|-----------|
| Repository Foundation | **Frozen** | 2026-07-08 |
| Capability Engineering | **Declared Active** | 2026-07-22 |

---

## Next Steps

- Continue BOQ Intelligence active development
- Scope next increment (CB-0002)
- Activate CheckMate when BOQ Intelligence is mature and domain rule catalog exists
- Produce the first Capability Era implementation before revising any existing documentation, including the README

The Capability Era began with this declaration.

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-22 | Created Sprint CB-0001. Capability Engineering Era declared active. |