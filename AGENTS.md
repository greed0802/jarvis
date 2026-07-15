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