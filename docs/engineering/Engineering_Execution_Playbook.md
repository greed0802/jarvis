# Engineering Execution Playbook

**Phase:** Phase 2 — Product Engineering Era
**Version:** 1.0
**Date:** 2026-07-29
**Authority:** Product Engineering Workstream
**Frozen ADR Baseline:** ADR-0027 through ADR-0032

---

## 1. Phase 2 Engineering Philosophy

Phase 1 (Architecture Discovery Era) produced a frozen architectural baseline:

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0027 | Capability Planning and Feasibility Architecture | FROZEN |
| ADR-0028 | Execution Runtime Lifecycle Architecture | FROZEN |
| ADR-0029 | Durable Execution Journal Architecture | FROZEN |
| ADR-0030 | CheckMate Capability Architecture | FROZEN |
| ADR-0031 | FindingReport & Public Capability Contract | FROZEN |
| ADR-0032 | Rule Model, Registry & Evidence Contract | FROZEN |

Phase 2 transitions from architectural discovery to product engineering.
Phase 2 engineering work implements frozen architectural decisions. It does
not create architecture.

---

## 2. Authority Hierarchy

| Layer | Artifact | Authority |
|-------|----------|-----------|
| Architecture | ADR (frozen) | Sole architectural authority. Defines capability boundaries, invariants, and contracts. |
| Discovery | Engineering Question (EQ) | Architecture exploration. Feeds ADRs. No implementation authority. |
| Engineering | Engineering Plan (EP) | Implementation authority only. Zero architectural authority. |
| Implementation | Code, Tests, CI | Governed by EPs and frozen ADRs. |

**Engineering Plans (EPs):**
- SHALL implement frozen architecture decisions.
- SHALL NOT create new capability boundaries or architectural invariants.
- SHALL NOT supersede, amend, or extend frozen ADRs.
- MAY identify engineering debt for tracking.
- MAY recommend future Engineering Questions or ADR amendments via the
  feedback mechanism, not inline modification.

---

## 3. Feature Lifecycle (6 Steps)

### Step 1: Planning (EP-xxxx)
Author an Engineering Plan document defining objective, scope, architecture
traceability matrix, out of scope, acceptance criteria, and quality gates.
The plan MUST reference the frozen ADR baseline.

### Step 2: Implementation
Implement the deliverables defined in the EP. All implementation work MUST
conform to frozen architectural boundaries and invariants. Engineering debt
identified during implementation is recorded in the EP's engineering debt
section, not resolved by modifying ADRs.

### Step 3: Automated Quality Gates
All CI tests, static analysis, and documentation verifiers MUST pass before
any human or AI code review occurs. Quality gates are a prerequisite for
review, not a parallel activity.

### Step 4: Invariant Conformance Review
Each implemented capability invariant is verified against the corresponding
ADR invariant definition. Conformance evidence is collected and referenced
in the EP.

### Step 5: Evidence Collection
Execution proof is recorded in the corresponding **EV-xxxx Engineering
Evidence Package** (`docs/engineering/evidence/`). The EV document records
actual test outputs, verifier log snippets, and pass/fail results mapped to
EP acceptance criteria. The EV document is the authoritative verification
artifact for the milestone — it is NOT the EP itself.

### Step 6: Promotion
Milestone promotion is governed exclusively by the **EV-xxxx verification
record**, not raw code changes or EP plan completion alone. Promotion
requires a completed EV-xxxx with all acceptance criteria recorded as PASS
and a signed promotion recommendation. Engineering debt items are tracked
in the EV-xxxx and assigned to future EPs.

---

## 4. Mandatory EP Structural Standards

Every Engineering Plan MUST contain the following sections:

### 4.1 Header
- EP identifier (EP-xxxx)
- Milestone (e.g., M10.1)
- Status
- Date
- Frozen ADR baseline references

### 4.2 Objective
A clear statement of what the EP delivers and why.

### 4.3 Scope & Deliverables
An explicit list of what is in scope and what will be delivered.

### 4.4 Architecture Traceability Matrix

A table mapping each frozen ADR decision or invariant to its planned
implementation and verification method:

| ADR Reference | Decision / Invariant | Planned Implementation | Verification |
|---------------|---------------------|----------------------|-------------|
| ADR-xxxx | Invariant name | Implementation approach | Test/verifier |

### 4.5 Out of Scope
An explicit list of decisions, capabilities, or concerns excluded from this
EP. This section MUST explicitly prohibit:
- Unrecorded architectural changes.
- Runtime modifications to frozen ADR boundaries.
- New capability boundaries not derived from frozen ADRs.

### 4.6 Acceptance Criteria
A list of verifiable pass/fail conditions that define when the EP is
complete.

### 4.7 Quality Gates

Quality gates are classified into two tiers:

**Tier 1 — Mandatory Baseline Gates (MUST pass before promotion):**
- Documentation verifier (`tools/quality/verify_documentation.py`)
- Unit test suite (`pytest` or project-configured test runner)
- Integration tests (where applicable to the milestone)

**Tier 2 — Extended Quality Gates (MAY be DEFERRED during early milestone setup):**
- Static type checker (project-configured, e.g., `mypy`, `pyright`)
- Import boundary analysis (project-configured)

Tier 2 gates that are not yet configured for a milestone SHALL be marked
`DEFERRED` in the EV-xxxx record, not `PENDING`. Deferred gates must be
activated before the completion of the milestone sequence.

### 4.8 Engineering Debt (Optional)
Known limitations, deferred concerns, or future EP candidates identified
during implementation.

### 4.9 Evidence Packages (EV-xxxx)
Each EP is paired with a canonical EV-xxxx Engineering Evidence Package.
The EV document is the execution proof record that governs milestone
promotion. Its structure SHALL contain:

| Section | Content |
|---------|---------|
| **Execution Metadata** | Commit SHA, branch, build ID, execution date/time, tool versions, OS/environment |
| **Acceptance Criteria Results** | Mapping of EP AC-x identifiers to PASS/FAIL/PENDING with timestamps and log references |
| **Quality Gate Execution Log** | Actual output snippets from each quality gate tool |
| **Architecture Conformance Audit** | Per-ADR invariant verification with evidence references |
| **Engineering Debt Audit** | Status of each EP engineering debt item (Outstanding/Resolved/Deferred) |
| **Promotion Recommendation** | Summary verdict and sign-off for milestone promotion |

**Rule of Non-Duplication:** EV-xxxx SHALL NOT duplicate planning definitions
from EP-xxxx. It SHALL reference EP identifiers (AC-x, ED-x) and record
execution outcomes only.

---

## 5. Quality-First Gate Rule

Automated CI tests and documentation verifiers MUST pass before AI-assisted
or peer code reviews occur. Review is a post-gate activity, not a parallel
one. This rule applies to all Phase 2 Engineering Plans.

---

## 6. Frozen Architecture Firewall

No Engineering Plan, implementation artifact, or team decision may:
- Modify the wording of a frozen ADR invariant.
- Introduce a new capability boundary not defined in a frozen ADR.
- Bypass a frozen ADR constraint on the grounds of implementation
  convenience.

If implementation reveals a genuine deficiency in a frozen ADR, the
correct resolution is to file a new Engineering Question for architectural
review — not to silently deviate in implementation.