# 09 — Methodology (Engineering Playbook)

> **Purpose**: The engineering playbook for all Jarvis contributors — human and AI. Defines how work is done, verified, frozen, and governed.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- Complete engineering workflow (10 steps)
- Evidence admission rules and hierarchy
- Production verification gate
- Architecture consistency gate
- Capability lifecycle (9 states + 3 terminal)
- EQ lifecycle (3 gates + freeze)
- Verification classification system
- Artifact lifecycle and freeze process
- Prohibited practices

It is the **single reference for how engineering happens** in Jarvis.

---

## Engineering Workflow

Every implementation follows these 10 steps:

```
1. Review architecture (Vision, Principles, Blueprint, relevant ADRs)
2. Review existing evidence (EQs, spikes, contracts)
3. Review existing implementation
4. Review existing tests
5. Determine if sufficient evidence exists
   ├── YES → Proceed to step 6
   └── NO  → Propose Engineering Question or Spike → gather evidence
6. Implement the smallest production-ready change
7. Execute tests
8. Review implementation against architecture
9. Verify documentation consistency
10. Summarize changes (files, reasons, ADRs, tests, risks)
```

**Never guess.** If evidence is insufficient, stop and gather evidence.

---

## Evidence Admission Rule

Production implementation must **never** be assumption-driven.

**Evidence Hierarchy** (higher overrides lower):

```
1. Accepted ADRs          ← Highest authority
2. Architecture Documents (00_Vision, 01_Principles, etc.)
3. Production Code        (existing working implementation)
4. Spike Evidence         (EQ spike reports, tool output, verification audits)
5. Approved Documentation (Project Owner verified docs)
6. External References    (domain standards, external specs)
7. General AI Knowledge   ← Lowest authority
```

When information conflicts, higher-priority evidence always overrides lower-priority.

Never replace repository evidence with generic best practices.

---

## Production Verification Gate

Before ANY production code is written:

1. Architecture review — does the change align with Vision, Principles, Blueprint?
2. ADR review — is there a relevant ADR? Does the change conform?
3. Existing implementation review — does this duplicate or conflict with existing code?
4. Existing tests review — what tests cover this area?
5. Evidence sufficiency check — is there enough evidence to proceed?

**Gate fails** if any of these cannot be satisfactorily answered.

---

## Architecture Consistency Gate

If implementation would change architecture:

1. **STOP** — do not proceed
2. Explain the conflict between current architecture and proposed implementation
3. Propose an ADR describing the architectural change
4. **Wait for Project Owner approval**
5. Only proceed after ADR is accepted

Never silently modify architectural decisions.

---

## Capability Lifecycle

Every capability follows this path. No shortcuts.

```
Discovery        ← Identify candidate capability
    ↓
Evaluation       ← Assess against criteria (Domain Value, Engineering Complexity, etc.)
    ↓
PO Decision      ← Project Owner decides: Pursue / Defer / Reject
    ↓
Engineering Q    ← Formulate EQ, define investigation subjects
    ↓
Spike            ← Gather evidence through focused investigations
    ↓
Implementation   ← Build capability, conforming to architecture
    ↓
Validation       ← Verify against contract, tests, and evidence
    ↓
Promotion        ← Promote capability to active register
    ↓
Release          ← Capability available to consumers
```

**Terminal states**: Rejected, Deferred, Archived

Never bypass lifecycle stages without explicit Project Owner approval.

---

## EQ Lifecycle

```
1. EQ Formulation     — Engineering question documented with investigation subjects
2. Gate 1 Approval    — Investigation authorized, spikes defined
3. Spikes Executed    — Evidence gathered (tools, data reports, verification audits)
4. Gate 2 Review      — Evidence reviewed, decision options presented
5. Gate 3 Decision    — Decision made: Implement / Defer / Reject
6. Freeze             — Final Freeze Report documents all decisions, evidence, consumer obligations
```

Frozen EQs are permanent evidence. They are never deleted.

---

## Verification Classification

Used across all knowledge documents:

| Code | Meaning | Engineering Trust |
|------|---------|-------------------|
| `VP` | Verified by Project Owner | **Authoritative** — use without reservation |
| `EB` | Evidence-Backed (production/tests/spikes confirm) | **Trustworthy** — evidence corroborates |
| `IB` | Implementation-Backed (code matches doc) | **Trustworthy** — code confirms design |
| `AGV` | AI-generated, Project Owner verified | **Authoritative** after review |
| `AGP` | AI-generated, pending verification | **Do NOT use for engineering decisions** |
| `SP` | Speculative (future, not built) | **Reference only** — not production |
| `UN` | Unknown provenance | Treat as AGP |
| `OBS` | Obsolete/Superseded | Do not use |

---

## Artifact Lifecycle

| Artifact Type | Created | Frozen | Disposition |
|---------------|---------|--------|-------------|
| Engineering Question | Gate 1 | Gate 3 + Freeze Report | **Permanent evidence** — preserved |
| Spike Report | During investigation | When evidence complete | **Permanent evidence** — preserved |
| Public Contract | After EQ evidence | After verification | **Frozen + versioned** — never deleted |
| ADR | Proposed | Accepted | **Permanent** — may be superseded by newer ADR |
| Domain Document | AI or human authored | After Project Owner verification | **Frozen** — authoritative domain truth |
| Planning Document | During planning | After milestone completion | **Archive** after completion |
| Architecture Spec | During design | NOT frozen (evolves with ADRs) | Living document — ADRs take precedence |

---

## Freeze Process

**EQ Freeze**: Final Freeze Report documents all spike evidence, key decisions, consumer obligations, and remaining risks. EQ is closed.

**Contract Freeze**: Version assigned (MAJOR.MINOR.PATCH), invariants locked, consumer guarantees established. Breaking changes require MAJOR version bump.

**Domain Freeze**: Document reviewed and verified by Project Owner, tagged as authoritative. All dependent capabilities must reference frozen version.

**Architecture Freeze**: ADR accepted by Project Owner. Implementation must conform. Deviations require new ADR.

---

## Prohibited Without Approval

These may **never** be introduced without explicit Project Owner authorization:

- Dependency Injection frameworks
- Plugin frameworks
- Service Locators
- Event Buses
- Reflection-based discovery
- Dynamic loading
- Generic abstractions without production use
- Architecture rewrites
- Breaking behavioral changes
- Bypassing capability lifecycle stages

---

## Communication Guidelines (for AI Agents)

When interacting with the Project Owner:
- Prefer concise explanations
- Avoid repeating repository context already in docs
- Reference existing documentation rather than reproducing it
- Clearly distinguish: observations, evidence, assumptions, recommendations
- If uncertain, state the uncertainty — do not fabricate confidence

---

## Engineering Debt Categories

| Category | Definition | Example |
|----------|-----------|---------|
| Documentation Debt | Documented but unimplemented | 82% of architecture docs are speculative |
| Verification Debt | AI-generated, unverified | 69% of domain docs pending review |
| Structure Debt | Empty directories | `src/jarvis/engines/builder/` is empty |
| Test Debt | Production code without tests | Kernel, Application, ValidationEngine have no test suite |
| Reference Debt | Broken/missing references | "Result Framework" referenced but doesn't exist |

---

## Dependencies

```
AGENTS.md → AI_Agent_Operating_Manual → Engineering_Governance → Capability_Roadmap → ADRs 0020,0021,0023
```

---

## References

- `AGENTS.md` — AI agent engineering rules (Project Owner Verified)
- `docs/engineering/AI_Agent_Operating_Manual.md` — Operating procedures (Project Owner Verified)
- `docs/engineering/Engineering_Governance.md` — Governance rules (AGP)
- `docs/planning/Capability_Roadmap.md` — Capability lifecycle governance (AGP)
- `docs/reference/Engineering_Questions.md` — Master EQ registry (Evidence-Backed)
- ADRs: 0020 (EQ Format), 0021 (Capability Engineering Pattern), 0023 (Evidence Contract Engineering)
- `docs/knowledge/01_Project_Overview.md` — Project identity and principles

---

## Verification Status

| Source | Status |
|--------|--------|
| `AGENTS.md` | **Project Owner Verified** |
| `AI_Agent_Operating_Manual.md` | **Project Owner Verified** |
| `Engineering_Governance.md` | AI-Generated, Pending Verification |
| `Capability_Roadmap.md` | AI-Generated, Pending Verification |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation