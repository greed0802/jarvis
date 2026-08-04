# Jarvis

Jarvis is a modular AI platform designed to provide deterministic, explainable, and extensible intelligent workflows.

## Current Status

| Property | Value |
|----------|-------|
| Architecture Version | v1.0 (Permanently Frozen) |
| Software Version | 0.0.1-alpha.13 |
| Repository Status | Production Alpha |
| Architecture | Frozen (26 ADRs + Architecture v1.0) |
| Tests | 944 passing (8 skipped) |
| Governance | Workstream Governance v1.0 (Register-Driven) |

---

## Completed Engineering Questions

| EQ | Title | Status |
|----|-------|--------|
| EQ-0010 | Deterministic BOQ Structural Intelligence | Completed |
| EQ-0011 | BOQ Semantic Intelligence Boundary | Completed |
| EQ-0012 | BOQ Intelligence Public Evidence Contract | Completed — Frozen v1.0 |
| EQ-0013 | Validation Engine | Completed — Frozen |
| EQ-0014 | Parser Regression Investigation | Completed |
| EQ-0015 | Structural Containment Investigation | Completed |
| EQ-0016 | Trade Classification Authority | Completed |
| EQ-0017 | Repository Governance Migration | Completed — Frozen v1.0 |
| EQ-0018 | BOQ Semantic Intelligence | Completed |
| EQ-0019 | BOQ Semantic Intelligence Increment 1 | COMPLETE — PERMANENTLY FROZEN |
| EQ-0020 | BOQ Intelligence Consumer Architecture | Complete — Frozen |
| EQ-0021 | CheckMate Application Architecture | Complete — PERMANENTLY FROZEN |

---

## Completed Implementation Packages

| IP | Title | Status |
|----|-------|--------|
| IP-0001 | BOQ Intelligence Increment 4 — Semantic Intelligence | PERMANENTLY FROZEN |
| IP-0002 | CheckMate Application — Consumer Architecture | Implemented — Active |

---

## BOQ Intelligence

| Increment | Capabilities | Status |
|-----------|-------------|--------|
| Increment 1 | Observe — Classification, Statistics, Anomalies | Complete |
| Increment 2 | Reconstruct — Hierarchy | Complete |
| Increment 3 | Detect — Structural Evidence | Complete |
| Increment 4 | Semantic — 8 Semantic Capabilities | **PERMANENTLY FROZEN** |

### Semantic Capabilities (Increment 4 — IP-0001)

| ID | Capability | Status |
|----|-----------|--------|
| SEM-PROD-01 | Vocabulary Extraction | Implemented — Frozen |
| SEM-PROD-02 | Head1 Text Categorization | Implemented — Frozen |
| SEM-PROD-04 | Administrative Pattern Detection | Implemented — Frozen |
| SEM-PROD-05 | Section Code Enumeration | Implemented — Frozen |
| SEM-PROD-06 | UOM Distribution Reporting | Implemented — Frozen |
| SEM-PROD-07 | Header Level Count Distribution | Implemented — Frozen |
| SEM-PROD-09 | "Items Always Quantify" Enforcement | Implemented — Frozen |
| SEM-PROD-12 | Administrative Sub-Template Recognition | Implemented — Frozen |

**Deferred:** SEM-PROD-03, SEM-PROD-08, SEM-PROD-10, SEM-PROD-11

---

## Governance

| Document | Version | Status |
|----------|---------|--------|
| Engineering Governance | v1.0 | Active |
| Implementation Governance | v1.0 | Active |
| Quality Assurance Constitution | 1.0 | Active |
| Engineering Question Freeze Checklist | 1.0 | Active |
| Repository Governance Automation | v1.0 | Active |

---

## Repository

```
docs/          — Architecture, ADRs, Engineering, Contracts, Implementation, Knowledge Governance
knowledge/     — Knowledge Engineering workspace (registry, evidence, ontology, governance)
knowledge_inbox/ — Temporary staging area used during Knowledge Engineering ingestion
src/           — Platform source code (BOQ Intelligence, Validation Engine, Kernel)
tests/         — 944 tests, 0 failures (8 skipped)
tools/         — Quality verification suite, governance tooling, knowledge utilities
```

---

## Latest Release

[v0.0.1-alpha.13](docs/releases/v0.0.1-alpha.13.md) — Repository Governance Complete

## Repository Status

Repository governance is complete.

The repository now operates using a register-driven workstream model with
Engineering Questions, Architecture Decisions, Knowledge Engineering,
Capability Projects, and Releases governed independently through the
[Workstream Governance Charter](docs/governance/WORKSTREAM_GOVERNANCE.md).

The next milestone is Execution Architecture.

## Roadmap

Phase 2 — Capability Era (current) — Building capabilities under ADR governance

### Current Phase: Execution Architecture

```
Execution Architecture (EQ-0023)
        ↓
ADR-0027 — Capability Planning
ADR-0028 — Execution Runtime Lifecycle
ADR-0029 — Durable Execution Journal
        ↓
Execution Runtime Foundation
```

---

## License

Private repository.
