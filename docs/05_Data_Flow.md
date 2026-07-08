# Data Flow

Version: 1.1

---

# Purpose

This document defines the architectural flow of information and execution within the Jarvis Platform.

It describes how requests become understanding, how understanding becomes strategy, how strategy becomes execution, and how execution becomes validated knowledge.

This document defines **information flow**, not implementation.

---

# Core Flow

Jarvis follows a deterministic lifecycle of understanding, planning, execution, validation, and learning.

```text
User Request
      │
      ▼
Intent
      │
      ▼
Context
      │
      ▼
Planner
      │
      ▼
Approved Plan
      │
      ▼
Workflow
      │
      ▼
Task
      │
      ▼
Capability
      │
      ▼
Capability Registry
      │
      ▼
Capability Resolver
      │
      ▼
Skill
      │
      ▼
Result
      │
      ▼
Validation
      │
      ▼
Memory
      │
      ▼
Learning
      │
      ▼
Knowledge
```

---

# 1. Understanding Flow

Understanding establishes the current working reality before any planning occurs.

```text
User Request
      │
      ▼
Intent
      │
      ▼
Context
```

The Context Engine assembles the relevant Context by referencing:

- Resources
- Memory
- Knowledge
- Workspace
- Project
- User
- Runtime metadata

Context references information rather than duplicating it.

---

# 2. Planning Flow

Planning transforms understanding into an executable strategy.

```text
Intent
      │
      ▼
Context
      │
      ▼
Planner Engine
      │
      ▼
Approved Plan
```

The Planner Engine evaluates:

- Intent
- Context
- Constraints
- Risks
- Available Capabilities

Planning is deterministic by default.

AI may assist planning but never replaces deterministic decision making.

---

# 3. Execution Flow

The Workflow Engine transforms an approved Plan into coordinated execution.

```text
Approved Plan
      │
      ▼
Workflow
      │
      ▼
Task
      │
      ▼
Capability
      │
      ▼
Capability Registry
      │
      ▼
Capability Resolver
      │
      ▼
Skill
      │
      ▼
Result
```

Workflow coordinates execution.

Tasks define executable work.

Capabilities define required operations.

Skills perform the work.

---

# 4. Validation and Replanning

Validation is a cross-cutting concern throughout execution.

```text
Result
      │
      ▼
Validation Framework
      │
      ▼
Workflow Engine
      ├──────── Continue
      ├──────── Retry
      ├──────── Refresh Context
      └──────── Request Replanning
                     │
                     ▼
               Planner Engine
```

The Validation Framework never communicates directly with the Planner Engine.

The Workflow Engine determines whether execution should:

- Continue
- Retry
- Refresh Context
- Request replanning

---

# 5. Learning Flow

Validated execution contributes to long-term platform knowledge.

```text
Validated Result
      │
      ▼
Memory
      │
      ▼
Learning
      │
      ▼
Knowledge
```

Memory preserves experience.

Learning evaluates experience.

Knowledge stores validated understanding.

Knowledge promotion requires validation and, where appropriate, explicit human approval.

---

# Ownership

| Information | Primary Owner |
|-------------|---------------|
| Resource | Resource Framework |
| Memory | Memory Framework |
| Knowledge | Knowledge Framework |
| Context | Context Engine |
| Intent | Context Engine |
| Plan | Planner Engine |
| Workflow | Workflow Engine |
| Task | Workflow Engine |
| Capability | Capability Registry & Resolver |
| Skill | Skill Framework |
| Result | Workflow Execution |

---

# Architectural Invariants

The following rules apply throughout the platform:

- Context is owned exclusively by the Context Engine.
- Plans are owned exclusively by the Planner Engine.
- Workflows and Tasks are owned exclusively by the Workflow Engine.
- Capability discovery is performed by the Capability Registry.
- Runtime Skill selection is performed by the Capability Resolver.
- Skills perform work but never coordinate execution.
- Validation evaluates execution but never requests replanning directly.
- The Workflow Engine mediates retries, Context refresh, and replanning.
- Knowledge promotion requires validation.
- Human approval is required whenever platform policy demands it.

---

# Governance Principles

The Data Flow follows the architectural principles of the Jarvis Platform.

- Humans remain in control.
- AI provides assistance rather than authority.
- Deterministic systems take precedence over probabilistic recommendations.
- Context references information rather than duplicating it.
- Execution remains explainable and traceable.
- Failures are contained and recoverable.

---

# Architectural Summary

Jarvis understands before it plans.

Jarvis plans before it executes.

The Workflow Engine coordinates execution.

Tasks define executable work.

Capabilities define required operations.

The Capability Registry discovers available implementations.

The Capability Resolver selects the appropriate implementation.

Skills perform work.

Validation evaluates execution.

Learning preserves validated experience.

The user remains in control throughout the lifecycle.

---

# Related Documents

- 06_Context_Engine.md
- 07_Planner_Engine.md
- 08_Workflow_Engine.md
- 10_Memory_Framework.md
- 11_Knowledge_Framework.md
- 12_Resource_Framework.md
- 14_Validation_Framework.md
- 15_Skill_Framework.md

---

# Related ADRs

- ADR_0005 — Deterministic Planner
- ADR_0007 — Knowledge Promotion
- ADR_0008 — Context
- ADR_0009 — Skill Architecture
- ADR_0010 — Human Control
- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0020 — Runtime vs. Cross-Cutting Architecture
- ADR_0021 — Control Plane and Data Plane Separation
- ADR_0022 — Context Lifecycle and Ownership
- ADR_0023 — Capability Discovery and Resolution