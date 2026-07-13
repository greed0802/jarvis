# Professional Research Backlog

## Purpose

This document records where the next Engineering Question could come from. It is a lightweight planning document — not an ontology, not architecture, and not a taxonomy. No hierarchy, relationships, or categorization beyond a flat list of domains.

The Research Backlog exists to answer one question: **Where could the next Engineering Question come from?**

The existence of a domain in this backlog does not imply that investigation is necessary or scheduled.

---

## Research Workflow

```
Vision
    │
    ▼
Research Backlog
    │
    ▼
Engineering Question
    │
    ▼
Engineering Spike
    │
    ▼
Engineering Evidence
    │
    ▼
Engineering Knowledge
    │
    ▼
ADR (only if architecture is affected)
```

Engineering Questions may be proposed from any domain. Architectural review determines whether a proposed question becomes an active investigation.

---

## Professional Domains

### Quantity Surveying

| Field | Value |
|-------|-------|
| **Why it matters** | Initial focus domain. BOQ development, cost estimating, quantity takeoff, engineering QA. |
| **Evidence Sources** | CostX BOQ exports, QS workflows, office BOQ templates |
| **Investigation status** | Multiple EQs |
| **Candidate Initial Engineering Question** | EQ-0001 — BOQ row identification (answered) |

### Civil Engineering

| Field | Value |
|-------|-------|
| **Why it matters** | Initial focus domain. Engineering computations, engineering documentation. |
| **Evidence Sources** | Engineering calculations, design notes, standards references |
| **Investigation status** | No EQ yet |
| **Candidate Initial Engineering Question** | TBD |

### CostX

| Field | Value |
|-------|-------|
| **Why it matters** | Primary data source for initial CostX acquisition. |
| **Evidence Sources** | Export workbooks, CostX documentation, office exports |
| **Investigation status** | Multiple EQs |
| **Candidate Initial Engineering Question** | EQ-0003 — CostX export format characteristics (answered) |

### Cubit

| Field | Value |
|-------|-------|
| **Why it matters** | Initial focus domain. Cost estimating platform. |
| **Evidence Sources** | Cubit exports, Cubit documentation, office Cubit templates |
| **Investigation status** | No EQ yet |
| **Candidate Initial Engineering Question** | TBD |

### Engineering Standards

| Field | Value |
|-------|-------|
| **Why it matters** | Engineering correctness depends on standards compliance. |
| **Evidence Sources** | AS, ISO, ASTM, NCC, office standards register |
| **Investigation status** | No EQ yet |
| **Candidate Initial Engineering Question** | TBD |

### Engineering Formulae

| Field | Value |
|-------|-------|
| **Why it matters** | Engineering computations require formula management. |
| **Evidence Sources** | Formula workbooks, calculation sheets, reference manuals |
| **Investigation status** | No EQ yet |
| **Candidate Initial Engineering Question** | TBD |

### Office Standards

| Field | Value |
|-------|-------|
| **Why it matters** | Professional work follows office-specific conventions. |
| **Evidence Sources** | Internal templates, SOPs, QA checklists |
| **Investigation status** | No EQ yet |
| **Candidate Initial Engineering Question** | TBD |

### Cost Libraries

| Field | Value |
|-------|-------|
| **Why it matters** | Professional cost estimation depends on reliable cost data. |
| **Evidence Sources** | Company database, historical estimates, supplier quotations |
| **Investigation status** | No EQ yet |
| **Candidate Initial Engineering Question** | TBD |

---

## Platform Domains

### Software Engineering

| Field | Value |
|-------|-------|
| **Why it matters** | Jarvis itself is a software platform. Software engineering practices govern its evolution. |
| **Evidence Sources** | Repository history, ADR index, implementation patterns |
| **Investigation status** | Multiple EQs |
| **Candidate Initial Engineering Question** | TBD |

### Artificial Intelligence

| Field | Value |
|-------|-------|
| **Why it matters** | AI is one capability within the platform, not the platform itself. |
| **Evidence Sources** | AI framework documentation, capability evaluations |
| **Investigation status** | No EQ yet |
| **Candidate Initial Engineering Question** | TBD |

---

## Status Summary

| Domain | Type | Status |
|--------|------|--------|
| Quantity Surveying | Professional | Multiple EQs |
| Civil Engineering | Professional | No EQ yet |
| CostX | Professional | Multiple EQs |
| Cubit | Professional | No EQ yet |
| Engineering Standards | Professional | No EQ yet |
| Engineering Formulae | Professional | No EQ yet |
| Office Standards | Professional | No EQ yet |
| Cost Libraries | Professional | No EQ yet |
| Software Engineering | Platform | Multiple EQs |
| Artificial Intelligence | Platform | No EQ yet |

---

## Governance

- Engineering Questions may be proposed from any domain. Architectural review determines whether a proposed question becomes an active investigation.
- The existence of a domain in this backlog does not imply that investigation is necessary or scheduled.
- No ontology or taxonomy shall be introduced ahead of engineering evidence.
- This backlog is a planning aid, not a commitment. Domains may be added, removed, or reordered as evidence accumulates.