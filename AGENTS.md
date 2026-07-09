# AGENTS.md

# Jarvis Repository Instructions

This document defines the mandatory engineering and architectural rules for
all AI coding agents contributing to the Jarvis repository.

Examples include:

- Cline
- Claude Code
- GitHub Copilot
- ChatGPT
- Any future coding agent

These instructions apply unless explicitly overridden by the repository owner.

---

# Repository Purpose

Jarvis is a modular Professional Intelligence Platform.

It is **not** a chatbot.

It is **not** an AI wrapper.

It is a long-term engineering platform whose architecture is Documentation-First and ADR-driven.

---

# Source of Truth

The architecture is defined by:

1. docs/00_Vision.md
2. docs/01_Principles.md
3. docs/02_System_Blueprint.md
4. docs/03_Core_Ontology_Relationships.md
5. docs/04_Platform_Kernel.md
6. Accepted ADRs

Implementation must follow these documents.

Never redefine architecture during implementation.

---

# Development Philosophy

Documentation First.

ADR Driven.

Small Iterations.

Deterministic Engineering.

Human Authority.

YAGNI.

---

# Architecture Rules

## The Platform Kernel

The Kernel is the Control Plane.

It manages:

- lifecycle
- configuration
- component registration
- service registration

The Kernel never:

- creates Context
- builds Plans
- executes Workflows
- executes Skills
- performs business logic

---

## Application

The Application is the Composition Root.

Application:

- creates platform components
- assembles the runtime
- registers components

The Kernel never constructs runtime components.

---

## Runtime Ownership

Context Engine owns Context.

Planner Engine owns Plans.

Workflow Engine owns Workflows and Tasks.

Skills perform work.

Validation evaluates outputs.

Learning promotes approved knowledge.

Responsibilities must never overlap.

---

# Implementation Rules

- Implement the smallest production-ready solution.
- Do not add speculative features.
- Avoid unnecessary abstractions.
- Prefer explicit typing.
- Keep modules focused.
- Preserve existing behavior unless requested otherwise.

---

# Prohibited Without Approval

Do not introduce:

- Dependency Injection frameworks
- Plugin frameworks
- Service Locators
- Event Buses
- Reflection-based discovery
- Dynamic loading
- Generic abstractions with no current use

---

# Documentation

If implementation changes architecture:

Stop.

Explain the conflict.

Propose an ADR.

Wait for approval.

Do not silently change architectural decisions.

---

# Code Reviews

Every implementation should explain:

- Files created
- Files modified
- Why the change was necessary
- Which architectural documents were followed

---

# Engineering Principle

Prefer clarity over cleverness.

Prefer explicitness over magic.

Prefer small stable improvements over large speculative frameworks.

Jarvis is intended to evolve for many years.

Optimize for maintainability rather than novelty.

# Repository Workflow

For every milestone:

1. Review architecture.
2. Implement the smallest change.
3. Review implementation.
4. Test implementation.
5. Commit.
6. Update documentation if behavior changed.

Do not implement multiple architectural milestones in a single change.