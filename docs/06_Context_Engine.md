# Context Engine

Version: 1.0

---

## Definition

The Context Engine is the first Core Runtime Engine of the Jarvis Data Plane.

It constructs, maintains, and refreshes the Context required for understanding the current objective.

The Context Engine assembles relevant information from across the platform into a coherent, temporary understanding that enables planning, workflow coordination, reasoning, and skill execution.

The Context Engine does not perform planning, workflow orchestration, skill execution, validation, learning, or result generation.


---

## Purpose

The Context Engine exists to provide an accurate, relevant, and continuously maintained understanding of the current objective.

It enables downstream runtime components to make informed and explainable decisions by supplying Context and interpreted Intent.

The Context Engine publishes the current Context and interpreted Intent through defined runtime interfaces for consumption by downstream Runtime Engines and Skills.

---

## Scope

The Context Engine manages understanding.

It does not:

- Create Plans
- Coordinate Workflows
- Execute Tasks
- Invoke Skills
- Produce Results
- Validate Results
- Promote Knowledge

Those responsibilities belong to the appropriate Runtime Engines and Frameworks.

---

## Context Philosophy

Context is not persistent information.

Context is the temporary understanding of the information relevant to the current objective.

Context references information whenever possible rather than duplicating it.

Context evolves as understanding changes throughout execution.

---

## Responsibilities

### Context Assembly

- Assemble Context
- Select relevant information
- Resolve references
- Interpret user requests into Intent

### Context Maintenance

- Maintain Context consistency
- Remove obsolete references
- Track contextual changes
- Refresh Context when requested

### Context Coordination

- Provide Context to the Planner Engine
- Provide Context to the Workflow Engine
- Provide Context to Skills during execution

---

## Ownership

The Context Engine exclusively owns:

- Context
- Intent

No other Runtime Engine or Framework may directly modify Context or Intent.

---

## Lifetime

Context exists only for the lifetime of the current objective.

It is created when understanding begins, evolves throughout execution, and is disposed of when the objective is completed or abandoned.

Persistent information remains within the appropriate Frameworks.

---

## Communication

The Context Engine communicates through well-defined runtime interfaces.

It provides:

- Context
- Intent

to downstream runtime components.

The Context Engine accepts Context refresh requests from the Workflow Engine.

It does not autonomously initiate Context refresh during active task execution.

---

## Extensibility

The Context Engine remains independent of specific Resource implementations.

New information sources may contribute to Context through the appropriate Frameworks and interfaces without requiring modifications to the Context Engine itself.

---

## Context Lifecycle

```text
User Request
      │
      ▼
Initial Intent
      │
      ▼
Context Assembly
      │
      ▼
Context Evaluation
      │
      ▼
Context Available
      │
      ▼
Planner Engine
      │
      ▼
Workflow Engine
      │
      ▼
Context Refresh (when requested)
      │
      ▼
Updated Context
```

---

## Context Composition

Context may reference information from:

- Resources
- Memory
- Knowledge
- Workspace
- Project
- User
- Organization
- Environment
- Runtime metadata exposed through Platform interfaces

Context should reference information whenever possible rather than duplicate it.

---

## Context Refresh

The Context Engine performs Context refreshes.

The Workflow Engine determines when Context should be refreshed in accordance with ADR_0022.

Typical refresh points include:

- Task completion
- User clarification
- Workflow checkpoints
- Explicit replanning
- Validation feedback

Context is never refreshed autonomously during active task execution.

---

## Relationships

The Context Engine collaborates with:

- Planner Engine
- Workflow Engine
- Memory Framework
- Knowledge Framework
- Resource Framework
- Skills

The Context Engine does not directly interact with the Platform Kernel beyond consuming runtime metadata exposed through defined interfaces.

---

## Information Boundaries

### Information entering the Context Engine

- User Requests
- Resources
- Memory
- Knowledge
- Workspace
- Project
- Runtime metadata exposed by the Platform Kernel

### Information produced

- Context
- Intent

### Information that never belongs to the Context Engine

- Plans
- Workflows
- Tasks
- Results
- Knowledge
- Persistent Memory

---

## Failure Management

The Context Engine detects incomplete, inconsistent, or insufficient understanding.

When Context cannot be established with sufficient confidence, it requests clarification rather than allowing downstream runtime components to proceed with incomplete understanding.

Failures in Context formation must be isolated and explained without compromising platform stability.

---

## Golden Rule

The Context Engine understands the current situation.

It never decides what should be done.

---

## Guiding Principle

> **What information is relevant right now to understand the current objective accurately, safely, and explainably?**

---

## Related Documents

- 02_System_Blueprint.md
- 03_Core_Ontology_Relationships.md
- 04_Platform_Kernel.md
- 05_Data_Flow.md
- 07_Planner_Engine.md
- 08_Workflow_Engine.md

---

## Related ADRs

- ADR_0008 — Context
- ADR_0010 — Human Control
- ADR_0013 — Workflow Ownership
- ADR_0021 — Control Plane and Data Plane Separation
- ADR_0022 — Context Lifecycle and Ownership