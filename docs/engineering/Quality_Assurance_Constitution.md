# Quality Assurance Constitution

**Document:** Quality_Assurance_Constitution.md

**Status:** Active

**Version:** 1.0

**Authority:** Project Owner

**Applies To:**

* Cline
* Claude Code
* ChatGPT
* GitHub Copilot
* Gemini
* Grok
* Qoder
* Future AI engineering assistants
* Human contributors

---

# Purpose

This document establishes the mandatory Quality Assurance framework for the Jarvis Platform.

Its purpose is to ensure that every engineering artifact reaches an objective, repeatable quality standard before being promoted to production or declared frozen.

Quality Assurance exists to:

* detect objective defects before architectural review
* preserve deterministic engineering
* maintain contract integrity
* prevent documentation drift
* ensure implementation fidelity
* preserve long-term maintainability

Quality Assurance complements:

* **AGENTS.md** — Repository governance
* **AI_Agent_Operating_Manual.md** — Operational workflow

This constitution governs **verification**.

---

# First Principle

Repository summaries are **not evidence**.

Documentation is **not implementation**.

Claims are **not verification**.

**Execution is evidence.**

Whenever an engineering claim can be objectively verified through automation, automation SHALL take precedence over opinion.

---

# Repository Must Prove Itself

No engineering claim is accepted merely because an AI, reviewer, or Project Owner states it.

Every claim must be reproducible through executable evidence generated from the repository itself.

Claims regarding:
- architecture
- determinism
- contracts
- registry integrity
- version consistency
- documentation synchronization
- traceability
- test counts
- import boundaries

must all be mechanically verifiable through the `tools/quality/` verification suite.

This principle captures the shift from opinion-driven to evidence-driven engineering. It is the foundation of the Quality Gates and the `verify_all.py` pipeline.

Evidence: M9 Repository Foundation Sprint — established permanent quality tooling and verification pipeline.

---

# Test Construction Rule

When constructing dataclass instances in tests, keyword arguments SHALL be used unless positional construction is explicitly under test.

Reason: Dataclass field ordering may change without type-enforcement failures. Positional arguments silently corrupt field assignments. Keyword arguments eliminate field-ordering ambiguity.

Evidence: EQ-0014 — 20 parser tests failed because BOQRow positional construction swapped uom/row_type fields. Production code was correct. Tests were fixed by converting to keyword arguments.

---

# Engineering Philosophy

Jarvis follows:

* Documentation First
* Evidence Before Abstraction
* Deterministic Engineering
* Verification Before Freeze
* Continuous Validation
* Explicit Engineering Debt
* Small Safe Iterations

Quality Assurance exists to preserve these principles.

---

# Verification Hierarchy

Engineering confidence is established in the following order:

Production Execution

↓

Automated Tests

↓

Verification Gates

↓

Architecture Review

↓

Project Owner Approval

↓

Freeze

No higher layer replaces a lower one.

Architecture review does not replace testing.

Testing does not replace execution.

Documentation never replaces verification.

---

# Quality Gates

Every capability shall pass all applicable Quality Gates before requesting Freeze.

---

# Quality Gate 0 — Engineering Question Admission

Purpose:

Prevent Engineering Question inflation. Ensure only genuine investigations requiring new evidence become Engineering Questions.

Decision tree:

```
Need new engineering evidence?
├── YES → Engineering Question (proceed to Gate 0 checklist)
└── NO  → Does it change production behavior?
          ├── YES → Bug Fix
          └── NO  → Documentation
                    Testing
                    Refactoring
                    Cleanup
                    Release
                    Maintenance
```

Only investigations requiring new evidence become Engineering Questions.

Before creating an EQ, verify the work is genuinely an investigation rather than a maintenance task.

---

# Quality Gate 1 — Mechanical Verification

Purpose:

Detect objective defects through executable verification.

Mandatory checks include:

## Production Tests

* committed under `tests/`
* reproducible
* automated
* deterministic

Spike tools under `tools/` are supporting evidence only.

They do not replace regression tests.

---

## Test Growth

Every implementation shall report:

Previous test count

↓

New test count

↓

Number of new tests

---

## Deterministic Verification

If deterministic behavior is claimed:

The implementation SHALL prove:

* identical input
* identical output
* repeatable execution

Deterministic equality shall include the complete public contract unless metadata is explicitly excluded.

---

## Contract Verification

Every public contract shall be verified against production implementation.

Documentation shall never become the contract.

Implementation is authoritative.

---

## Documentation Synchronization

Implementation

↓

Tests

↓

Contracts

↓

Documentation

shall remain synchronized.

Documentation drift blocks Freeze.

---

## Version Consistency

Version identifiers shall remain synchronized across:

* version module
* README
* implementation status
* release notes
* contracts
* capability register

---

## Repository Integrity

Production code shall not depend upon:

* docs/
* tools/
* data/reports/

unless explicitly approved by the Project Owner.

Spike artifacts shall never become hidden production dependencies.

---

# Quality Gate 2 — Architecture Verification

Purpose:

Verify engineering correctness beyond executable behavior.

Review includes:

* responsibility ownership
* dependency direction
* hidden coupling
* architecture consistency
* public contracts
* determinism
* consumer independence
* ADR compliance
* Engineering Boundary compliance
* YAGNI
* Rule of Three

Architecture review focuses on engineering judgment rather than mechanics.

---

# Quality Gate 3 — Consumer Readiness

Purpose:

Verify production usability.

Review includes:

Stable APIs

Public imports

Backward compatibility

Packaging

Consumer documentation

Contract maturity

Version compatibility

No consumer shall depend on unstable implementation details.

---

# Quality Gate 4 — Repository Consistency

Purpose:

Verify repository-wide consistency across all engineering artifacts.

Review includes:

## Documentation Synchronization

Documentation SHALL match implementation.

Every public API, contract, and behavior described in documentation SHALL be verifiable against production code.

## Version Consistency

All version references SHALL be synchronized across:

- README
- version module
- implementation status
- release documentation
- contracts
- capability register
- knowledge base

## Contract Alignment

Contracts SHALL match the public API.

No contract SHALL describe behavior that does not exist in implementation.

No implementation SHALL expose behavior not covered by a contract.

## Test Coverage

All committed contracts SHALL have corresponding tests.

Tests SHALL verify contract invariants, not just happy paths.

## Knowledge Base Alignment

Knowledge base documents SHALL reflect the current frozen state of contracts and implementation.

Stale knowledge base entries SHALL block Freeze.

## Capability Register Consistency

The Capability Register SHALL match Implementation Status.

No capability SHALL be listed as "Implemented" without a frozen contract and committed tests.

## Artifact Synchronization

Every engineering claim SHALL trace to exactly one authoritative artifact.

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

Artifact Synchronization asks: **"Is every downstream artifact saying the same thing?"**

This is distinct from traceability (which asks "Where did this come from?").

---

# Quality Gate 5 — Release Readiness

Purpose:

Determine whether the repository is eligible for tagging, publishing, and consumer adoption.

Checklist:

□ All previous gates PASS (G0–G4)

□ Engineering Debt Register reviewed

□ No Critical Debt

□ Capability Register synchronized

□ Implementation Status synchronized

□ Contracts synchronized

□ Version synchronized across README, module, contracts, release notes

□ Release Notes prepared

□ `verify_all.py` PASS

Authority: Project Owner

---

# Definition of Done

No capability may be declared:

Complete

Frozen

Production Ready

unless all applicable Quality Gates pass.

Minimum completion requirements:

✓ Production implementation complete

✓ Regression tests committed

✓ Test count increased

✓ Contracts verified

✓ Documentation synchronized

✓ Version synchronized

✓ Engineering Debt reviewed

✓ Architecture reviewed

✓ Project Owner approval received

---

# Engineering Debt Register

Every Engineering Question shall conclude with an Engineering Debt Register.

Each entry shall include:

* Debt ID
* Description
* Severity
* Root Cause
* Impact
* Blocks Freeze (Yes/No)
* Planned Resolution
* Target Milestone
* Current Status

Known engineering debt shall never be silently ignored.

Freeze approval must explicitly acknowledge unresolved debt.

---

# Verification Classification

Every verification result shall be classified as:

PASS

All required criteria satisfied.

PASS WITH ENGINEERING DEBT

Implementation acceptable.

Known debt documented.

Does not invalidate current milestone.

FAIL

Quality Gate not satisfied.

Implementation cannot proceed to Freeze.

---

# Artifact Verification

Every production artifact shall identify:

Purpose

Authority

Evidence Source

Verification Method

Current Status

Dependencies

Verification Date

Applicable Engineering Question

Applicable Contracts

Applicable ADRs

---

# Evidence Classification

Every engineering statement shall be classified as:

Evidence

Observation

Assumption

Recommendation

Only Evidence may justify production implementation.

Assumptions require investigation.

Recommendations require Project Owner approval.

---

# Anti-Drift Policy

Every implementation shall verify alignment between:

Production Code

↓

Tests

↓

Contracts

↓

Documentation

↓

Knowledge Base

Drift shall be corrected before Freeze whenever practical.

---

# Multi-Model Review Policy

Multiple AI systems may participate.

Recommended responsibilities:

Implementation

↓

Mechanical Verification

↓

Architecture Review

↓

Adversarial Review

↓

Project Owner

Example reviewers:

Cline

Implementation

Automation

Testing

ChatGPT

Engineering methodology

Architecture

Planning

Claude

Architecture

Governance

Boundary verification

GitHub Copilot

Repository audit

Implementation consistency

Documentation drift

Grok

Independent adversarial review

Consistency validation

No AI reviewer is authoritative.

Repository evidence remains authoritative.

---

# Automated Quality Assurance

Whenever possible, Quality Gates shall be executable.

Examples include:

pytest

Contract verification

Deterministic replay

Schema validation

Coverage analysis

Documentation link checking

Version consistency

Import verification

Consumer compatibility

Automation should detect objective defects before AI review.

---

# Continuous Improvement

Every Retrospective shall consider:

Defects discovered

Missed Quality Gates

New verification opportunities

Automation improvements

Engineering process improvements

Quality Assurance evolves with repository maturity.

---

# Responsibilities

## AI Agents

Shall:

* execute verification
* report evidence
* identify risks
* document engineering debt
* distinguish evidence from opinion

Shall not:

* fabricate verification
* infer successful execution
* hide failed checks
* declare Freeze without evidence

---

## Project Owner

Responsible for:

* approving Quality Assurance policy
* accepting engineering debt
* authorizing Freeze
* determining acceptable risk

---

# Constitutional Amendments

This constitution is expected to evolve.

Changes require:

1. Engineering rationale
2. Project Owner approval
3. Repository documentation updates

Historical changes shall remain traceable.

---

# Success Criteria

Quality Assurance is successful when:

* objective defects are detected before release
* documentation reflects implementation
* contracts remain trustworthy
* deterministic behavior is preserved
* engineering debt is visible
* architecture remains stable
* future contributors can reproduce engineering confidence without relying on institutional memory

The goal of Jarvis is not simply to produce software.

The goal is to produce a professional engineering platform whose correctness, maintainability, and evolution are continuously supported by objective evidence and disciplined quality assurance.
