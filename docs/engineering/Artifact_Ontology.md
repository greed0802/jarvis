# Artifact Ontology

**Version:** 1.0
**Date:** 2026-07-29
**Authority:** Product Engineering Workstream
**Frozen ADR Baseline:** ADR-0027 through ADR-0032

---

## 1. Purpose & Scope

This document establishes the unified mental model for all document artifacts
in the repository. It defines the authoritative taxonomy, authority hierarchy,
artifact lifecycles, state transitions, and anti-inflation rules that govern
how documents are created, used, and retired.

Every team member and AI agent operating in this repository MUST understand
which artifact type answers which question and what authority each type
carries.

---

## 2. The 7-Tier Authority Hierarchy

| Level | Artifact Type | Authority Scope | Owner | Primary Question |
|-------|--------------|----------------|-------|-----------------|
| 1 | **Vision / Principles / System Blueprint** | Permanent philosophy and architecture roadmap | Product Owner | Why does this system exist and what is its long-term direction? |
| 2 | **ADR (Architecture Decision Record)** | Frozen architectural authority | Capability Workstream | What must be true about this capability forever? |
| 3 | **EQ (Engineering Question)** | Architectural exploration and discovery | Capability Workstream | What do we need to discover to make a frozen architectural decision? |
| 4 | **AGENTS.md / Playbook** | Operational and execution governance | Product Engineering | How do agents and engineers operate in this repository? |
| 5 | **EP (Engineering Plan)** | Implementation intent | Product Engineering | What will be built and how does it map to frozen ADRs? |
| 6 | **EV (Engineering Evidence)** | Canonical execution and verification proof | Product Engineering | What actually happened when we ran the implementation? |
| 7 | **Code / Tests / CI** | Executable implementation | Engineering | Does the implementation conform to ADRs and pass all gates? |

### Authority Flow Rules

- Authority flows strictly downward: Level 2 (ADR) governs Level 5 (EP).
- Lower levels MUST NOT alter or redefine higher levels.
- An EP that disagrees with an ADR is wrong; the ADR is not amended by the EP.
- If a lower-level artifact reveals a genuine problem in a higher-level artifact,
  a new artifact at the appropriate higher level must be authored (new EQ → new
  ADR) — not a silent amendment to the lower-level artifact.

---

## 3. Artifact Lifecycles & State Transitions

### ADR (Architecture Decision Record)

```
PROPOSED (Pending PO Freeze)
        │
        │  Project Owner review
        ▼
    FROZEN  ────────────────────────────────────────────────────────
                                                                   │
                                           If genuine deficiency   │
                                           discovered, file new EQ └──► NEW EQ
```

| State | Description |
|-------|-------------|
| PROPOSED | Drafted from frozen EQ, pending Project Owner approval |
| FROZEN | Project Owner approved. Content is immutable. Only a new EQ can initiate amendment. |

### EQ (Engineering Question)

```
OPEN
  │
  │  All spikes completed, all invariants approved
  ▼
FROZEN
```

| State | Description |
|-------|-------------|
| OPEN | Active discovery underway. Spikes are being explored. |
| FROZEN | All spikes completed, all invariants approved. Content is immutable. Feeds ADRs. |

### EP (Engineering Plan)

```
OPEN
  │
  │  Implementation complete, all deliverables produced
  ▼
COMPLETE
```

| State | Description |
|-------|-------------|
| OPEN | Engineering plan authored, implementation in progress |
| COMPLETE | All deliverables produced. Promotion governed by paired EV-xxxx. |

### EV (Engineering Evidence)

```
PENDING_VERIFICATION
        │
        │  All AC results PASS, all quality gates pass, promotion signed off
        ▼
    PROMOTED
```

| State | Description |
|-------|-------------|
| PENDING_VERIFICATION | Scaffolded, awaiting execution results |
| PROMOTED | All acceptance criteria PASS, milestone promoted |

---

## 4. Anti-Inflation Rule

The Anti-Inflation Rule prevents document type proliferation and redundant
artifact creation. Before authoring any new document, the author MUST
answer:

> **Does an existing artifact type already own this concern?**

If yes, record it there. Do not create a new document type.

### Prohibited Redundant Documents

| Prohibited Document | Reason | Correct Location |
|--------------------|--------|-----------------|
| Separate Test Plan | AC and quality gates belong in EP; results belong in EV | EP (Section 4.6, 4.7) and EV (Section 3, 4) |
| Separate Release Plan | Promotion is a EV-xxxx concern | EV (Section 6: Promotion Sign-Off) |
| Separate Architecture Summary | This is what ADRs are | ADR files |
| Separate Engineering Debt Register | Debt is tracked in EP (ED-x) and EV (Section 5) | EP and EV |
| Separate Test Results Log | Test results belong in the EV | EV (Section 3: Quality Gate Execution Log) |
| Separate Design Document | Design decisions belong in EQs and ADRs | EQ → ADR |
| Separate Standards Document | Standards are architectural invariants | ADR invariants |

### The 3-Question Filter

Before creating any new document type:
1. Does a Level 1–7 artifact already own this concern? → Record it there.
2. Is this concern architectural? → File an EQ.
3. Is this concern implementation evidence? → Add to EV-xxxx.

If none of the above, escalate to Product Engineering governance before
creating a new artifact type.

---

## 5. Operational Governance Mapping

The three governance documents that operate together at Layer 4 are:

| Document | Responsibility | Does NOT Own |
|----------|---------------|-------------|
| **AGENTS.md** | AI agent behavior, tool usage rules, context protocol, output format standards | Feature lifecycles, document taxonomy, architectural decisions |
| **Engineering_Execution_Playbook.md** | 6-step feature lifecycle, EP structural standards, EV pairing rules, quality-first gate rule, frozen architecture firewall | Agent behavior, document taxonomy, architectural decisions |
| **Artifact_Ontology.md** (this document) | Document taxonomy, authority hierarchy, lifecycle state transitions, anti-inflation rules | Agent behavior, feature lifecycle procedures, architectural decisions |

### Non-Overlap Guarantee

These three documents are intentionally non-overlapping:
- `AGENTS.md` answers: *How should the AI agent behave?*
- `Engineering_Execution_Playbook.md` answers: *How do we execute a feature?*
- `Artifact_Ontology.md` answers: *What are our document types and what authority do they carry?*

No document defines the answer to another document's primary question.