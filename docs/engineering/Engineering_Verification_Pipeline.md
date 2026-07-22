# Engineering Verification Pipeline

**Status:** Active — Hardening Sprint (Post EQ-0013)
**Version:** 1.0
**Authority:** Repository Hardening Sprint (Post EQ-0013)
**Governance:** Quality_Assurance_Constitution.md

---

## 1. Purpose

This document defines the mandatory verification pipeline for every Engineering Question (EQ), capability, milestone, and production change in the Jarvis repository.

It replaces ad-hoc verification with a repeatable, automated pipeline.

---

## 2. Core Principle

**Documentation follows verified implementation.**

Engineering documentation may describe architecture, plans, or frozen contracts, but implementation-specific behavior must only be documented after it has been verified by automated tests and quality gates.

---

## 3. Mandatory Pipeline

Every EQ SHALL pass through the following stages in order:

```
EQ
 ↓
Spike Investigation
 ↓
Evidence Report
 ↓
Verification Audit
 ↓
Regression Tests (committed under tests/)
 ↓
Quality Gates (Gates 1-4)
 ↓
Repository Drift Audit
 ↓
Freeze
 ↓
Git Tag
 ↓
Release
```

Stages may not be skipped.

Stages may not be reordered.

---

## 4. Stage Descriptions

### 4.1 EQ — Engineering Question

- Define the engineering question
- Reference existing architecture and ADRs
- Identify evidence requirements
- Obtain Project Owner approval

### 4.2 Spike Investigation

- Conduct spike per EQ requirements
- Produce evidence reports under `docs/engineering/evidence/`
- Produce verification tools under `tools/`

### 4.3 Evidence Report

- Document findings as committed reports
- Classify every claim as Evidence, Observation, Assumption, or Recommendation
- Only evidence justifies production implementation

### 4.4 Verification Audit

- Verify evidence against contracts
- Verify architecture consistency
- Verify boundary compliance
- Run existing verification tools

### 4.5 Regression Tests

- All production code SHALL have committed tests under `tests/`
- Tests SHALL be pytest-based
- Tools under `tools/` are supporting evidence, not proof
- Regression tests must pass before proceeding

### 4.6 Quality Gates

Every change SHALL satisfy four quality gates:

**Gate 1 — Mechanical Verification:**
- Committed production test suite exists
- Deterministic behavior verified
- Contract verification passes
- Documentation synchronized with implementation
- Version consistency across repository
- Architecture integrity (no production dependency on docs/, tools/, data/reports/)

**Gate 2 — Architecture Verification:**
- Responsibility boundaries preserved
- No hidden coupling
- Consumer independence maintained
- ADR compliance
- YAGNI compliance

**Gate 3 — Consumer Readiness:**
- Stable public API
- Package boundaries maintained
- Contract maturity established
- Backward compatibility maintained

**Gate 4 — Repository Consistency:**
- Documentation synchronized with implementation
- Version references consistent
- Contracts match public API
- Tests cover all committed contracts
- Knowledge base aligned with implementation
- Capability Register matches Implementation Status
- Artifact Synchronization: every engineering claim traces to exactly one authoritative artifact

### 4.7 Repository Drift Audit

Before freeze, conduct a drift audit covering:

- Implementation Drift
- Documentation Drift
- Architecture Drift
- Contract Drift
- Knowledge Drift
- Version Drift
- Test Drift

The audit produces a `Repository_Drift_Report.md` as the final verification artifact.

### 4.8 Freeze

- All blocking debt items resolved or explicitly classified
- Regression verification passes
- Repository Drift Audit reports no unresolved blocking inconsistencies
- Engineering Debt Register is current
- Project Owner approves

### 4.9 Git Tag

- Tag the repository with the version number
- Include the freeze report reference in the tag message

### 4.10 Release

- Produce release notes
- Update RELEASE document
- Promote to consumers

---

## 5. Artifact Synchronization

Every engineering claim must trace to exactly one authoritative artifact.

```
Implementation
 ↓
Tests
 ↓
Evidence Report
 ↓
Contract (if applicable)
 ↓
Knowledge Base
```

Downstream artifacts must not contradict upstream artifacts.

Artifact Synchronization asks: **"Is every downstream artifact saying the same thing?"**

---

## 6. Review Cadence

| Event | Review Type | Responsible |
|-------|-------------|-------------|
| Every Spike | Quality Gates + Drift tools | Cline |
| Every completed EQ | Independent reviewer | Claude / Copilot / Grok / ChatGPT |
| Every tagged release | Full adversarial architecture review | External reviewer |

---

## 7. Pipeline Status Indicators

| Stage | Status | Definition |
|-------|--------|------------|
| EQ | ☐ / ☒ | Engineering Question approved |
| Spike | ☐ / ☒ | Investigation complete |
| Evidence | ☐ / ☒ | Evidence report committed |
| Audit | ☐ / ☒ | Verification audit passed |
| Tests | ☐ / ☒ | Regression tests committed and passing |
| Gates | ☐ / ☒ | All 4 Quality Gates pass |
| Drift | ☐ / ☒ | Repository Drift Audit complete |
| Freeze | ☐ / ☒ | Freeze approved |
| Tag | ☐ / ☒ | Git tag created |
| Release | ☐ / ☒ | Release notes published |

---

## 8. Relationship to Other Documents

| Document | Relationship |
|----------|--------------|
| AGENTS.md | Defines mandatory repository rules |
| AI_Agent_Operating_Manual.md | Defines recommended operating procedures |
| Quality_Assurance_Constitution.md | Defines mandatory quality gates |
| This Document | Defines the verification pipeline connecting engineering process to quality gates |
| Engineering_Debt_Register.md | Tracks all known engineering debt |

---

## 9. Change Log

| Date | Version | Changes |
|------|---------|---------|
| 2026-07-16 | 1.0 | Initial creation — Repository Hardening Sprint |

---

**End of Engineering Verification Pipeline**