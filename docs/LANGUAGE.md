# LANGUAGE

Version: 1.0

---

# Purpose

This document defines the canonical architectural vocabulary of the Jarvis Platform.

Its purpose is to ensure that every document, ADR, implementation, and discussion uses consistent terminology.

When terminology conflicts arise, this document serves as the authoritative reference unless superseded by an accepted Architecture Decision Record (ADR).

---

# Core Concepts

| Term | Meaning |
|------|---------|
| **Resource** | Anything Jarvis can access. |
| **Knowledge** | Validated understanding Jarvis can reason from. |
| **Memory** | Experience and observations Jarvis remembers. |
| **Context** | The temporary understanding relevant to the current objective. |
| **Intent** | What the user wants to achieve. |
| **Plan** | The proposed approach for achieving an Intent. |
| **Workflow** | The coordination of execution for an approved Plan. |
| **Task** | The smallest executable unit of work. |
| **Capability** | A contract describing an operation that can be performed. |
| **Skill** | An implementation that provides one or more Capabilities. |
| **Planner** | Produces a Plan from Context and Intent. |
| **Project** | Owns project-specific data and resources. |
| **Workspace** | Owns the user's working environment and organizational context. |
| **Result** | The validated outcome of execution. |

---

# Runtime Concepts

| Term | Meaning |
|------|---------|
| **Platform Kernel** | The Control Plane responsible for coordinating and protecting the platform runtime. |
| **Context Engine** | The Runtime Engine responsible for understanding the current objective. |
| **Planner Engine** | The Runtime Engine responsible for producing Plans. |
| **Workflow Engine** | The Runtime Engine responsible for coordinating execution. |
| **Framework** | A reusable subsystem providing shared capabilities across the platform. |
| **Service** | Shared runtime functionality provided to multiple platform components. |
| **Plugin** | An extension that adds functionality without modifying the platform core. |
| **Provider** | An external implementation supplying capabilities or services to the platform. |

---

# Architectural Relationships

Use the following verbs consistently throughout the architecture.

| Relationship | Meaning |
|-------------|---------|
| **Owns** | Responsible for the complete lifecycle of an object. |
| **Produces** | Creates an object as output. |
| **Consumes** | Uses an object as input without owning it. |
| **References** | Maintains a relationship without owning the referenced object. |
| **Coordinates** | Orchestrates interactions between multiple components. |
| **Implements** | Provides the behavior defined by a Capability. |
| **Provides** | Makes functionality available to other components. |
| **Requests** | Asks another component to perform a responsibility it owns. |
| **Validates** | Confirms correctness without taking ownership. |
| **Promotes** | Converts information into a higher level of trust or permanence. |

---

# Information Lifecycle

The canonical information lifecycle of the Jarvis Platform is:

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
Plan
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
Skill
      │
      ▼
Result
      │
      ▼
Memory
      │
      ▼
Knowledge
```

---

# Architectural Principles

The following principles guide the use of terminology throughout the platform.

- Every architectural object has a single primary responsibility.
- Ownership implies lifecycle responsibility.
- Referencing does not imply ownership.
- Runtime Engines coordinate understanding, planning, and execution.
- Frameworks provide shared capabilities.
- Skills perform work through Capabilities.
- Plans describe what should be done.
- Workflows coordinate how approved Plans are executed.
- Results are validated before becoming trusted knowledge.

---

# Terminology Rules

To maintain consistency across the architecture:

- Prefer **Plan** over "Execution Plan."
- Prefer **Workflow** over "Process" or "Pipeline."
- Prefer **Capability** over "Function."
- Prefer **Skill** over "Tool."
- Prefer **Resource** over "Asset."
- Prefer **Knowledge** over "Facts."
- Prefer **Memory** over "History."
- Prefer **Context** over "State" when describing operational understanding.
- Prefer **Platform Kernel** over "Core" when referring to the Control Plane.

---

# Related Documents

- 03_Core_Ontology_Relationships.md
- 04_Platform_Kernel.md
- 05_Data_Flow.md

---

# Related ADRs

- ADR_0001 — Core Ontology
- ADR_0005 — Deterministic Planner
- ADR_0008 — Context
- ADR_0009 — Skill Architecture
- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0020 — Runtime vs Cross-Cutting Architecture
- ADR_0021 — Control Plane and Data Plane Separation
- ADR_0022 — Context Lifecycle and Ownership