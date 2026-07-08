---
adr: 0021
title: Control Plane and Data Plane Separation
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Architecture
related:
  - 02_System_Blueprint.md
  - 04_Platform_Kernel.md
  - 05_Data_Flow.md
---

# ADR_0021_Control_Plane_and_Data_Plane_Separation

## Status

Accepted

---

## Context

As the Jarvis architecture evolved, the responsibilities of the Platform Kernel became clearer.

Originally, the Platform Kernel appeared to coordinate runtime execution alongside platform management. Further architectural refinement showed that these are separate concerns.

The Platform Kernel should manage the platform itself, while user requests and business execution should be handled by the Runtime Engines and Frameworks operating within the platform.

This distinction establishes a clear boundary between platform management and domain execution.

---

## Decision

The Jarvis Platform is divided into two architectural planes:

### Control Plane

The Control Plane is implemented by the **Platform Kernel**.

It is responsible for:

- Platform lifecycle
- Component registration
- Service registration
- Dependency resolution
- Configuration management
- Platform policy enforcement
- Health monitoring
- Platform service provisioning
- Security initialization
- Storage initialization

The Control Plane never performs business logic.

### Data Plane

The Data Plane is responsible for processing user work.

It includes:

- Context Engine
- Planner Engine
- Workflow Engine
- Cross-Cutting Frameworks
- Skills
- Plugins
- Resources
- Results

The Data Plane transforms user intent into validated results.

---

## Information Boundary

Only platform control information enters the Control Plane, including:

- Registration
- Configuration
- Lifecycle events
- Dependency resolution
- Health information
- Platform policies

Business information remains within the Data Plane, including:

- User queries
- Intent
- Context
- Plans
- Workflows
- Tasks
- Resources
- Knowledge
- Results

---

## Rationale

Separating platform management from business execution:

- Reduces coupling.
- Prevents platform infrastructure from depending on domain logic.
- Improves maintainability.
- Simplifies testing.
- Enables independent evolution of runtime engines and platform services.
- Aligns Jarvis with proven platform architectures used in operating systems and cloud orchestration platforms.

---

## Consequences

### Positive

- Clear separation of responsibilities.
- Stable Platform Kernel.
- Modular runtime architecture.
- Easier extension through Engines, Frameworks, Skills, and Plugins.
- Improved long-term scalability.

### Trade-offs

- Requires well-defined interfaces between the Platform Kernel and Runtime Engines.
- Architectural boundaries must be enforced consistently.

---

## Guiding Principle

> The Platform Kernel manages the platform.

> The Runtime Engines perform the work.

The Control Plane provides the environment.

The Data Plane delivers the value.
