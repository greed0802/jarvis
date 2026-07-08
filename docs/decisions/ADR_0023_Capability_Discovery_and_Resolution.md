# ADR_0023 — Capability Discovery and Resolution

Status: Accepted

Date: 2026-07-08

---

# Context

The Jarvis Platform separates understanding, planning, execution, and capability implementation into distinct architectural responsibilities.

As the architecture evolved through the Context Engine, Planner Engine, Workflow Engine, and Skill Framework, an important architectural distinction emerged:

- How does the platform discover available capabilities?
- How does the platform decide which implementation should perform a required capability?

Early documentation referred to both a **Capability Registry** and a **Capability Resolver**, but their individual responsibilities were not formally defined.

Without this distinction, planning, execution, and implementation selection become tightly coupled, reducing modularity and limiting extensibility.

---

# Decision

The Jarvis Platform separates **Capability Discovery** from **Capability Resolution**.

These are distinct architectural responsibilities.

The **Capability Registry** is responsible for discovering and cataloging available Capabilities and their implementing Skills.

The **Capability Resolver** is responsible for selecting the most appropriate Skill implementation for a required Capability during execution.

---

# Capability Registry

The Capability Registry answers the question:

> **What capabilities exist within the platform?**

The Capability Registry maintains information about:

- Capability definitions
- Available Skill implementations
- Provider metadata
- Version compatibility
- Supported inputs and outputs
- Required permissions
- Capability metadata

The Capability Registry never selects which Skill should be executed.

---

# Capability Resolver

The Capability Resolver answers the question:

> **Which Skill implementation should fulfill this Capability for the current execution?**

The Capability Resolver evaluates runtime information including:

- Current Context
- Approved Plan
- Workflow requirements
- User preferences
- Platform policies
- Permissions
- Provider availability
- Resource availability
- Execution constraints

The Capability Resolver selects the most appropriate Skill implementation.

---

# Planning Responsibilities

The Planner Engine identifies the Capabilities required to accomplish an objective.

The Planner Engine never selects specific Skill implementations.

The Planner produces Plans containing required Capabilities rather than implementation details.

---

# Workflow Responsibilities

The Workflow Engine coordinates execution.

During execution, the Workflow Engine requests capability resolution.

The Workflow Engine:

- Requests the required Capability
- Consults the Capability Registry
- Invokes the Capability Resolver
- Coordinates execution of the selected Skill

---

# Skill Responsibilities

Skills implement one or more Capabilities.

Skills never participate in planning or capability selection.

Skills perform work only after being selected through the Capability Resolution process.

---

# Information Flow

```text
Planner Engine
        │
        ▼
Approved Plan
        │
        ▼
Workflow Engine
        │
        ▼
Required Capability
        │
        ▼
Capability Registry
        │
        ▼
Candidate Skills
        │
        ▼
Capability Resolver
        │
        ▼
Selected Skill
        │
        ▼
Execution
```

---

# Rationale

Separating discovery from resolution provides several architectural benefits.

The Planner remains independent of implementation details.

The Workflow Engine coordinates execution without maintaining a catalog of available capabilities.

The Capability Registry remains responsible for platform knowledge.

The Capability Resolver remains responsible for runtime decision making.

Skills remain modular and replaceable.

New Skill implementations may be introduced without requiring changes to the Planner Engine or existing Plans.

This ADR supersedes earlier ontology wording that assigned runtime Skill selection to the Capability Registry.

Following this decision:

- The Capability Registry is responsible for discovering and cataloging available Skill implementations.
- The Capability Resolver is responsible for selecting the appropriate implementation at runtime based on the current execution context.

---

# Consequences

## Benefits

- Clear separation of concerns
- Planner remains implementation-independent
- Runtime selection becomes flexible
- Skills remain replaceable
- Multiple Skill implementations may provide the same Capability
- Supports future AI-assisted or policy-driven capability selection
- Improves platform extensibility

## Trade-offs

- Introduces an additional runtime component
- Capability resolution becomes a distinct execution step
- Additional contracts are required between Workflow, Registry, and Resolver

---

# Related Documents

- docs/ontology/core/capability.md
- 07_Planner_Engine.md
- 08_Workflow_Engine.md
- 15_Skill_Framework.md

---

# Related ADRs

- ADR_0005 — Deterministic Planner
- ADR_0009 — Skill Architecture
- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0020 — Runtime vs Cross-Cutting Architecture
- ADR_0021 — Control Plane and Data Plane Separation
- ADR_0022 — Context Lifecycle and Ownership