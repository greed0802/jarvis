# 04 — Engineering Governance

> **Purpose**: Summary of engineering governance — ADR system, agent operating rules, and governance framework.
> **Part of**: Jarvis Knowledge Consolidation

---

## Responsibilities

This document covers:
- ADR governance (what ADRs are, how they're used, current state)
- AI agent operating rules (from AGENTS.md and AI_Agent_Operating_Manual.md)
- Governance principles that constrain all engineering work

It does NOT cover detailed methodology steps (see `09_Methodology.md`) or individual ADR summaries (see [Appendix B](Appendices/B_ADR_Registry.md)).

---

## ADR Governance

**Architecture Decision Records** are the formal mechanism for architectural governance.

### ADR Principles
- ADRs are **permanent** once accepted
- ADRs may be **superseded** by newer ADRs (explicitly referencing the superseded ADR)
- ADRs take **precedence over architecture docs** in the Evidence Hierarchy
- Implementation **must conform** to accepted ADRs
- Architectural changes **require an ADR** — never silently modify architecture

### Current ADR State
- **26 ADRs Accepted** (all)
- **0 Proposed, 0 Deprecated, 0 Superseded**
- Foundation ADRs (0001-0024): 2026-07-08 — ontology, engines, lifecycle, governance
- Capability-era ADRs (0025-0026): 2026-07-14 — BOQ Intelligence contract, Evidence/Assessment boundary

### Key Governance ADRs

| ADR | Rule |
|-----|------|
| ADR-0010 | Human Control — Jarvis assists, never autonomously decides |
| ADR-0017 | Kernel Philosophy — Kernel is control plane only |
| ADR-0019 | Consumer Independence — capabilities expose public contracts |
| ADR-0020 | EQ Format — standardized investigation format |
| ADR-0021 | Capability Engineering Pattern — contract-first |
| ADR-0023 | Evidence Contract Engineering — evidence-backed, versioned contracts |
| ADR-0025 | Observation vs Assessment — Evidence/Assessment boundary |

---

## AI Agent Operating Rules

**Source**: `AGENTS.md` (Project Owner Verified) and `AI_Agent_Operating_Manual.md` (Project Owner Verified)

### Authority Model
- **Project Owner** is the final engineering authority
- AI agents: investigate, recommend, implement, review
- AI agents **never** determine architecture independently

### Source of Truth
1. `docs/00_Vision.md`
2. `docs/01_Principles.md`
3. `docs/02_System_Blueprint.md`
4. `docs/03_Core_Ontology_Relationships.md`
5. `docs/04_Platform_Kernel.md`
6. Accepted ADRs

These documents define architecture. Implementation must conform. Never reinterpret architecture during implementation.

### Required Reading (Before Significant Changes)
- Architecture documents (Vision, Principles, Blueprint, Platform Kernel, ADRs)
- Engineering documents (Engineering Questions, Spike Reports, Capability Register, Roadmap)
- Operational guidance (AI_Agent_Operating_Manual)

Do not ask the Project Owner for information that already exists in repository documentation.

### Multi-Agent Collaboration
- Multiple AI agents may contribute
- Agents shall preserve accepted engineering decisions
- Respect frozen investigations, accepted ADRs
- Avoid unnecessary rewrites
- Clearly identify disagreements
- Justify architectural recommendations with evidence
- Never overwrite previous engineering work without justification

### Context Management
- Prefer reading repository docs over asking Project Owner
- Prefer concise explanations
- Reference existing documentation rather than reproducing it
- Clearly distinguish: observations, evidence, assumptions, recommendations
- If uncertain, state the uncertainty — do not fabricate confidence

---

## Governance Principles

### Repository Purpose
Jarvis is a modular Professional Intelligence Platform:
- NOT a chatbot
- NOT an AI wrapper
- NOT an experimental playground

### Engineering Philosophy
- Documentation First
- Evidence Before Promotion
- ADR Driven
- Deterministic Engineering
- Human Authority
- YAGNI (smallest production-ready solution)
- Small Iterations
- Clarity over Cleverness
- Explicitness over Magic
- Maintainability over Novelty

### Documentation Responsibilities
If implementation changes architecture:
- STOP
- Explain the conflict
- Propose an ADR
- Wait for approval
- Do not silently modify architectural decisions

If implementation changes behavior:
- Review and update documentation as appropriate
- Examples: README, Architecture Status, Capability Register, Release Notes

### Implementation Rules
- Implement the smallest production-ready solution
- Prefer incremental improvement
- Avoid speculative features
- Avoid unnecessary abstraction
- Prefer explicit typing
- Keep modules focused
- Preserve existing behavior unless requested
- Do not rewrite working modules solely for style
- Avoid architecture expansion unless approved

---

## Evidence Hierarchy (Governance Enforcement)

When information conflicts:
```
1. Accepted ADRs          ← Highest authority
2. Architecture Documents
3. Production Code
4. Spike Evidence
5. Approved Documentation
6. External References
7. General AI Knowledge   ← Lowest authority
```

Higher-priority evidence always overrides lower-priority. This is a **governance rule**, not a guideline.

---

## Prohibited Without Project Owner Approval

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

## Repository Workflow (Every Milestone)

```
1. Review architecture
2. Review evidence
3. Implement smallest change
4. Execute tests
5. Review implementation
6. Verify documentation
7. Summarize changes
8. Commit
9. Update release documentation when appropriate
```

Avoid implementing multiple architectural milestones in a single change unless explicitly approved.

---

## Current Governance Status

| Aspect | Status |
|--------|--------|
| ADR System | 26 Accepted, active governance |
| AGENTS.md | Project Owner Verified, authoritative |
| AI Agent Manual | Project Owner Verified, active |
| Engineering Governance doc | AI-Generated, Pending Verification |
| Capability Roadmap | AI-Generated, Pending Verification |
| Architecture Compliance | Kernel + Validation Engine comply with ADRs |
| Test Coverage | No test suite for production code — governance gap |
| Documentation Drift | 82% of architecture docs are speculative — governance gap |

---

## Dependencies

```
AGENTS.md → AI_Agent_Operating_Manual → Engineering_Governance → ADRs → Implementation
```

---

## References

- `AGENTS.md` — AI agent engineering rules
- `docs/engineering/AI_Agent_Operating_Manual.md` — Operating procedures (406 lines)
- `docs/engineering/Engineering_Governance.md` — Governance rules
- `docs/decisions/` — All 26 ADRs
- `docs/knowledge/Appendices/B_ADR_Registry.md` — ADR summary
- `docs/knowledge/09_Methodology.md` — Detailed engineering playbook

---

## Verification Status

| Source | Status |
|--------|--------|
| `AGENTS.md` | **Project Owner Verified** |
| `AI_Agent_Operating_Manual.md` | **Project Owner Verified** |
| All 26 ADRs | **Project Owner Verified** (Accepted) |
| `Engineering_Governance.md` | AI-Generated, Pending Verification |
| `Capability_Roadmap.md` | AI-Generated, Pending Verification |

---

**Generated**: 2026-07-15 | **Part of**: Jarvis Knowledge Consolidation