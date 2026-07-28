# AGENTS.md

# Jarvis Repository Instructions

This document defines the mandatory engineering and architectural rules for all AI coding agents contributing to the Jarvis repository.

Examples include:

- Cline
- Claude Code
- GitHub Copilot
- ChatGPT
- Gemini CLI
- Qoder
- Any future coding agent

These instructions apply unless explicitly overridden by the Project Owner.

---

# Repository Purpose

Jarvis is a modular Professional Intelligence Platform.

It is NOT:

- a chatbot
- an AI wrapper
- an experimental playground

Jarvis is a long-term engineering platform whose architecture is:

- Documentation First
- Evidence Driven
- ADR Governed
- Capability Oriented

---

# Repository Constitution

The repository architecture is considered a frozen engineering asset.

AI agents SHALL preserve repository structure exactly as defined by the architecture.

Repository organization is NOT an implementation detail.

Repository organization IS architecture.

If an AI agent believes files belong somewhere else, the agent SHALL NOT move them automatically.

Instead the agent shall:

1. identify the conflict
2. explain why the conflict exists
3. reference the architecture
4. propose an Engineering Question or ADR if necessary
5. wait for Project Owner approval

Repository boundaries shall never evolve implicitly.

---

# Repository Boundary Rules

Every file created by an AI agent SHALL belong to exactly one architectural category.

## Production

Production implementation only.

Examples:

src/
tests/

Production code SHALL NEVER be written elsewhere.

---

## Documentation

Repository documentation only.

Location:

docs/

Documentation SHALL follow the approved documentation hierarchy.

### Architecture

docs/

Architecture documents.

Examples:

Vision

Principles

Blueprint

Kernel

ADRs

---

### Engineering

docs/engineering/

Engineering Questions

Spike Reports

Capability Discovery

Capability Evaluation

Implementation Reviews

Engineering Evidence

Execution Reports

Temporary engineering documentation

---

### Knowledge Documentation

docs/knowledge/

Knowledge governance only.

Examples:

Knowledge Architecture

Knowledge Governance

Knowledge Lifecycle

Knowledge Storage Policy

Knowledge Consumption

Knowledge Engineering Principles

These documents describe HOW knowledge is managed.

They do NOT describe execution of a milestone.

---

### Execution Documentation

docs/execution/

Execution history only.

Examples:

Migration Reports

Recovery Reports

Temporary execution plans

Validation summaries

Implementation logs

One-off engineering activities

Execution documentation shall never become permanent governance.

---

# Knowledge Boundary

knowledge/

is NOT documentation.

knowledge/

is runtime repository data.

It contains repository knowledge assets.

Only the following belong here:

knowledge/

    registry/

    governance/

    ontology/

    glossary/

    evidence/

Source documents remain immutable.

---

# Tool Boundary

tools/

contains executable tooling only.

Never place:

documentation

reports

architecture

governance

inside tools/.

---

# File Placement Rule

Before creating ANY new file the AI agent SHALL perform this reasoning:

1.

What category is this file?

2.

What architectural boundary owns this category?

3.

Does an approved location already exist?

If yes:

Use the existing location.

Do NOT invent another folder.

---

# Folder Creation Rule

AI agents SHALL NOT create new top-level folders.

AI agents SHALL NOT create new documentation hierarchies.

AI agents SHALL reuse the approved repository structure.

If a new hierarchy appears necessary:

STOP.

Raise an Engineering Question.

---

# Repository Preservation Rule

Every planned operation must be classified before execution.

One of:

Read-Only

Additive

Transformative

Destructive

Definitions

Read-Only

Reads repository assets only.

No modifications.

Additive

Creates new files only.

Never changes existing assets.

Transformative

Modifies repository-managed artefacts only.

Examples:

documentation

registry

metadata

tests

configuration

Destructive

Deletes

Moves

Renames

Overwrites

Restructures

existing assets.

Destructive operations are PROHIBITED unless explicitly approved by the Project Owner in the current conversation.

---

# Architecture Conflict Rule

If implementation conflicts with repository architecture:

STOP.

Do not improvise.

Do not relocate files.

Do not create alternative structures.

Produce an Architecture Conflict Report.

Wait for approval.

---

# Continuous Consistency Rule

Before declaring any milestone complete, verify:

No duplicate documentation exists.

No competing folder structures exist.

No duplicate governance exists.

No architectural drift has occurred.

If drift is detected:

STOP.

Produce a Repository Drift Report.

Do not request milestone freeze until drift is resolved.

---

# Project Authority

The Project Owner is the final engineering authority.

AI agents:

- investigate
- recommend
- implement
- review

AI agents never determine architecture independently.

---

# Source of Truth

Repository decisions are governed by:

1. docs/00_Vision.md
2. docs/01_Principles.md
3. docs/02_System_Blueprint.md
4. docs/03_Core_Ontology_Relationships.md
5. docs/04_Platform_Kernel.md
6. Accepted ADRs

These documents define architecture.

Implementation must conform to them.

Never reinterpret architecture during implementation.

---

# Required Repository Reading

Before implementing significant changes, review the documentation relevant to the task.

Examples include:

Architecture

- Vision
- Principles
- Blueprint
- Platform Kernel
- Accepted ADRs

Engineering

- Engineering Questions
- Spike Reports
- Capability Register
- Capability Roadmap

Operational Guidance

- docs/engineering/AI_Agent_Operating_Manual.md
- docs/engineering/Quality_Assurance_Constitution.md

Do not ask the Project Owner for information that already exists in repository documentation.

---

# Evidence Hierarchy

When information conflicts, use the following priority.

1. Accepted ADRs
2. Architecture Documents
3. Production Code
4. Engineering Questions
5. Spike Evidence
6. Approved Documentation
7. External References
8. General AI Knowledge

Higher-priority evidence always overrides lower-priority evidence.

Never replace repository evidence with generic best practices.

---

# Engineering Philosophy

Documentation First.

Evidence Before Promotion.

ADR Driven.

Deterministic Engineering.

Human Authority.

YAGNI.

Small Iterations.

Clarity over Cleverness.

Explicitness over Magic.

Maintainability over Novelty.

---

# Architecture Rules

## Platform Kernel

The Kernel is the Control Plane.

Kernel responsibilities:

- lifecycle
- configuration
- registration
- service management

The Kernel never:

- creates Context
- creates Plans
- executes Workflows
- performs business logic
- executes Skills

---

## Application

Application is the Composition Root.

Application:

- creates runtime components
- assembles the runtime
- wires dependencies
- registers services

The Kernel never constructs runtime objects.

---

## Runtime Ownership

Ownership is exclusive.

Context Engine owns Context.

Planner Engine owns Plans.

Workflow Engine owns Workflows and Tasks.

Skills perform work.

Validation evaluates outputs.

Learning promotes approved knowledge.

Responsibilities must never overlap.

---

# Engineering Workflow

Before writing production code:

1. Review architecture.
2. Review applicable ADRs.
3. Review existing implementation.
4. Review existing tests.
5. Determine whether sufficient evidence exists.

If evidence is insufficient:

Do not guess.

Instead:

- propose an Engineering Question
- propose a Spike
- gather evidence
- wait for approval when required

Production implementation must never be assumption-driven.

---

# Capability Lifecycle

Every capability follows:

Capability Discovery

↓

Capability Evaluation

↓

Project Owner Decision

↓

Engineering Question

↓

Spike

↓

Implementation

↓

Validation

↓

Promotion

↓

Release

Do not bypass lifecycle stages without explicit approval.

---

# Implementation Rules

Implement the smallest production-ready solution.

Prefer incremental improvement.

Avoid speculative features.

Avoid unnecessary abstraction.

Prefer explicit typing.

Keep modules focused.

Preserve existing behavior unless requested.

Do not rewrite working modules solely for style.

Avoid architecture expansion unless approved.

---

# Deterministic Engineering

Production code should be:

- deterministic
- repeatable
- observable
- testable
- maintainable

Identical inputs should produce identical outputs whenever practical.

---

# Multi-Agent Collaboration

Multiple AI agents may contribute.

Agents shall:

- preserve accepted engineering decisions
- respect frozen investigations
- respect accepted ADRs
- avoid unnecessary rewrites
- clearly identify disagreements
- justify architectural recommendations with evidence

Never overwrite previous engineering work without justification.

---

# Documentation Responsibilities

If implementation changes architecture:

STOP.

Explain the conflict.

Propose an ADR.

Wait for approval.

Do not silently modify architectural decisions.

If implementation changes behavior:

Review and update documentation as appropriate.

Examples:

- README
- Architecture Status
- Capability Register
- Capability Roadmap
- ADR references
- Release Notes

---

# Code Reviews

Every implementation should summarize:

Files created.

Files modified.

Reason for change.

Architecture followed.

Relevant ADRs.

Engineering Question reference (if applicable).

Spike reference (if applicable).

Tests executed.

Remaining risks.

---

## Python Environment

Do not activate the virtual environment.

Always invoke the interpreter directly:

    ./.venv/bin/python

Examples:

    ./.venv/bin/python -m pytest
    ./.venv/bin/python tools/quality/verify_all.py --json
    ./.venv/bin/python -m pip install <package>

This avoids shell-specific activation issues (Fish/Bash/Zsh) and ensures deterministic execution.

# Repository Workflow

Every milestone should follow:

1. Review architecture.
2. Review evidence.
3. Implement the smallest change.
4. Execute tests.
5. Review implementation.
6. Verify documentation.
7. Summarize changes.
8. Commit.
9. Update release documentation when appropriate.

Avoid implementing multiple architectural milestones in a single change unless explicitly approved.

---

# Prohibited Without Approval

Do not introduce:

- Dependency Injection frameworks
- Plugin frameworks
- Service Locators
- Event Buses
- Reflection-based discovery
- Dynamic loading
- Generic abstractions without production use
- Architecture rewrites
- Breaking behavioral changes

---

# Communication Guidelines

When interacting with the Project Owner:

Prefer concise explanations.

Avoid repeating repository context.

Reference existing documentation rather than reproducing it.

Present alternatives when appropriate.

Clearly distinguish:

- observations
- evidence
- assumptions
- recommendations

If uncertain:

State the uncertainty.

Do not fabricate confidence.

---

# Engineering Principles

Prefer evidence over assumptions.

Prefer documentation over memory.

Prefer explicit design over implicit behavior.

Prefer deterministic behavior over convenience.

Prefer small stable improvements over speculative frameworks.

Optimize every contribution for long-term maintainability.

Jarvis is intended to evolve for many years.

Every change should leave the repository clearer, more consistent, and easier to maintain than before.


# Engineering Quality Assurance Constitution

This repository follows a Verification Before Freeze philosophy.

No implementation, capability, Engineering Question, or milestone may be declared Complete, Frozen, or Production Ready without passing the mandatory Quality Gates.

These gates exist to ensure objective defects are detected by automation before architectural review.

AI agents shall never substitute narrative summaries for executable verification.

# Quality Gate 1 — Mechanical Verification (Mandatory)

The following SHALL be completed before requesting Freeze.

## Testing
A committed production test suite SHALL exist under tests/.
Verification tools under tools/ do not replace regression tests.
Test count increase SHALL be reported.
Determinism

## If deterministic behavior is claimed:

identical inputs SHALL produce identical outputs.
full object equality SHALL be verified where the contract claims deterministic outputs.
metadata (timestamps, identifiers, runtime state) SHALL not invalidate deterministic contracts unless explicitly excluded from the contract.
Contract Verification

All public contracts SHALL be verified against production implementation.

Documentation shall never be considered proof of behavior.

Documentation Synchronization

Implementation

↓

Tests

↓

Contracts

↓

Documentation

shall remain synchronized.

Documentation drift shall block Freeze.

Version Consistency

Repository version SHALL be consistent across:

README
version module
implementation status
release documentation
contracts
Architecture Integrity

Production code SHALL NOT depend on:

docs/
tools/
data/reports/

unless explicitly approved.

Spike artifacts shall never become hidden production dependencies.

# Quality Gate 2 — Architecture Verification

Architecture review SHALL verify:

responsibility boundaries
hidden coupling
contract integrity
consumer independence
determinism
YAGNI compliance
ADR compliance
Engineering Boundary preservation

This review focuses on engineering judgment rather than mechanical correctness.

# Quality Gate 3 — Consumer Readiness

Before introducing a new consumer:

Verify:

stable public API
import stability
package boundaries
contract maturity
consumer documentation
backward compatibility
Engineering Debt Register

Every Engineering Question SHALL conclude with an Engineering Debt Register.

Each item shall include:

ID
Finding
Severity
Blocks Freeze (Yes/No)
Planned Resolution
Status

Known engineering debt shall never be silently ignored.

If debt remains, Freeze approval shall explicitly acknowledge it.

Production Verification Rule

AI agents shall never claim production behavior without executable evidence.

Claims regarding:

determinism
immutability
performance
API behavior
contract compliance

require executable verification or committed automated tests.

Repository summaries are not evidence.

Execution is evidence.

---

# Repository Boundary Constitution

Repository organization is part of the Jarvis Architecture.

Folder structure is considered a frozen engineering asset.

AI agents SHALL preserve repository organization exactly as defined by the architecture.

Repository layout SHALL NOT evolve through implementation.

Only the Project Owner may approve repository structural changes.

---

# Repository Boundary Verification

Before creating ANY file, every AI agent SHALL perform the following verification.

## Step 1 — Classify the Artifact

Every artifact belongs to exactly one architectural category.

Choose one:

- Production Code
- Test
- Architecture Documentation
- Engineering Documentation
- Knowledge Documentation
- Execution Documentation
- Knowledge Repository Data
- Tooling
- Configuration
- Automation
- Temporary Investigation

If classification is ambiguous:

STOP.

Request clarification.

---

## Step 2 — Determine Repository Owner

Every category has exactly one repository owner.

| Category | Location |
|----------|----------|
| Production Code | src/ |
| Tests | tests/ |
| Architecture Documentation | docs/ |
| Engineering Documentation | docs/engineering/ |
| Knowledge Documentation | docs/knowledge/ |
| Execution Documentation | docs/execution/ |
| Knowledge Repository Data | knowledge/ |
| Tooling | tools/ |
| Configuration | repository root |

Never create a second owner.

---

## Step 3 — Check Existing Structure

Before creating a new directory:

Search for an existing location.

If an equivalent location already exists:

Reuse it.

Do not create another folder.

---

# Documentation Placement Rules

Permanent documents belong only in permanent locations.

## Architecture

Contains:

Vision

Principles

Blueprint

Kernel

ADR

Ontology

Architecture Status

Repository Architecture

Never place temporary engineering work here.

---

## Engineering

Contains:

Engineering Questions

Spike Reports

Capability Discovery

Capability Evaluation

Capability Register

Implementation Reviews

Engineering Evidence

Engineering Debt

Only engineering activities belong here.

---

## Knowledge Documentation

Contains permanent governance.

Examples:

Knowledge Architecture

Knowledge Governance

Knowledge Lifecycle

Knowledge Storage Policy

Knowledge Engineering Principles

Knowledge Source Management

Knowledge Consumption

Knowledge Ontology

These documents describe the knowledge system itself.

Never place temporary execution history here.

---

## Execution Documentation

Contains temporary activities.

Examples:

Migration reports

Recovery reports

Execution logs

Validation summaries

One-time implementation reports

Temporary rollout documentation

Execution documents SHALL NOT become permanent governance.

---

# Knowledge Repository Rules

knowledge/

contains repository knowledge.

NOT documentation.

Allowed:

knowledge/

    registry/

    governance/

    ontology/

    glossary/

    evidence/

Never place Markdown documentation here unless it is repository-managed knowledge content.

Never duplicate documentation already living under docs/.

---

# Tooling Rules

tools/

contains executable utilities only.

Never place:

reports

documentation

governance

architecture

inside tools/.

---

# Folder Creation Policy

AI agents SHALL NOT create new top-level folders.

AI agents SHALL NOT introduce alternative documentation hierarchies.

AI agents SHALL reuse approved repository structure.

If a new hierarchy appears necessary:

STOP.

Raise an Engineering Question.

Wait for Project Owner approval.

---

# Repository Preservation Rule

Every repository operation SHALL be classified.

Exactly one classification must be assigned.

## Read-Only

Reads only.

Creates nothing.

Changes nothing.

---

## Additive

Creates new files only.

Never modifies existing assets.

---

## Transformative

Updates approved repository-managed artefacts only.

Examples:

documentation

registry

metadata

configuration

tests

---

## Destructive

Deletes

Moves

Renames

Overwrites

Restructures

existing assets.

Destructive operations are prohibited unless explicitly approved by the Project Owner in the current conversation.

---

# Repository Drift Detection

Before milestone completion the AI agent SHALL verify:

□ No duplicate documentation.

□ No duplicated governance.

□ No duplicated execution reports.

□ No competing folder structures.

□ No conflicting repository hierarchy.

□ No undocumented folder creation.

□ No architecture drift.

If any answer is YES:

STOP.

Produce a Repository Drift Report.

Do not request milestone freeze.

---

# Repository Boundary Checklist

Every completion report SHALL include:

Repository Boundary Verification

Repository Drift Check

Documentation Placement Verification

Knowledge Boundary Verification

Tool Boundary Verification

Architecture Compliance

The checklist SHALL explicitly report:

PASS

or

FAIL

for every category.

---

# Constitutional Stop Conditions

The AI agent SHALL immediately stop if:

- repository architecture becomes ambiguous

- two valid locations appear to exist

- documentation placement cannot be justified

- folder ownership becomes unclear

- architecture conflicts with implementation

- repository organization must change

When stopped:

Produce an Architecture Conflict Report.

Do not continue implementation.

---

# Continuous Engineering Rule

Every completed milestone shall leave the repository:

more deterministic

more consistent

more traceable

more reproducible

more maintainable

than it was before implementation.

No milestone shall increase architectural ambiguity.

====================================================
REPOSITORY QUALITY GATE
====================================================

Architecture Compliance
PASS / FAIL

Repository Boundary Verification
PASS / FAIL

Documentation Placement Verification
PASS / FAIL

Knowledge Boundary Verification
PASS / FAIL

Repository Drift Detection
PASS / FAIL

Destructive Operations
NONE / LIST

Files Created
...

Files Modified
...

Engineering Debt
...

Risks Remaining
...

Recommendation

□ Freeze
□ Continue
□ Engineering Question Required
□ ADR Required