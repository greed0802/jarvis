# Object: Capability

Category:
Core / Platform

---

# Definition

A Capability represents a standardized function that the Jarvis Platform can perform.

Capabilities define **what** can be accomplished.

They never define **how** it is accomplished.

The implementation is provided by one or more Skills.

Capabilities act as architectural contracts between the Planner Engine, Workflow Engine, and Skill Framework.

---

# Purpose

Capabilities decouple planning from implementation.

The Planner Engine identifies the Capabilities required to accomplish an objective without knowing how they will be implemented.

The Workflow Engine requests those Capabilities during execution.

The Capability Registry discovers available Skill implementations.

The Capability Resolver selects the most appropriate implementation at runtime.

---

# Capability Answers

> **What can be accomplished?**

Not

> **How is it accomplished?**

---

# Examples

## Engineering

- Build BOQ
- Generate Formula
- Validate Formula
- Compare BOQs
- Generate Description
- QA Check

---

## Documents

- Read Excel
- Write Excel
- Read PDF
- OCR Image
- Generate Report

---

## Development

- Execute Python
- Execute SQL
- Read Git Repository
- Run Tests

---

## Artificial Intelligence

- Summarize
- Translate
- Reason
- Plan
- Explain
- Research

---

## Automation

- Send Email
- Schedule Task
- Notify User
- Synchronize Resources

---

# Capability Does NOT

A Capability never:

- Execute work
- Store data
- Own Resources
- Plan execution
- Coordinate Workflows
- Select Skill implementations
- Maintain Context
- Produce Results

Capabilities describe platform functionality.

Execution belongs to Skills coordinated by the Workflow Engine.

---

# Skill Implementations

Each Capability may be implemented by one or more Skills.

Example

Capability

```
Read Excel
```

Available Skill Implementations

- OpenPyXL Skill
- LibreOffice Skill
- Microsoft Excel Skill

The Workflow Engine requests the Capability.

The Capability Registry identifies all compatible Skill implementations.

The Capability Resolver selects the most appropriate implementation based on runtime conditions.

---

# Capability Registry

The Capability Registry is responsible for Capability discovery.

Capabilities are registered when Skills become available.

The Registry maintains:

- Capability name
- Description
- Version
- Available Skill implementations
- Provider metadata
- Requirements
- Dependencies
- Permissions
- Availability
- Compatibility information

The Capability Registry never selects which Skill implementation will execute.

---

# Capability Resolver

The Capability Resolver is responsible for runtime implementation selection.

It evaluates:

- Approved Plan
- Current Context
- Workflow requirements
- User preferences
- Platform policies
- Permissions
- Provider availability
- Resource availability
- Execution constraints

The Capability Resolver selects the most appropriate Skill implementation for the requested Capability.

---

# Capability Requirements

A Capability may require:

- Resources
- Context
- User approval
- Permissions
- Installed Skills
- Available Providers

Execution cannot begin until all mandatory requirements have been satisfied.

---

# Capability Lifecycle

```text
Registered
      │
      ▼
Discovered
      │
      ▼
Requested
      │
      ▼
Resolved
      │
      ▼
Executing
      │
      ▼
Completed

or

Unavailable

or

Failed
```

---

# Relationships

Planner Engine

identifies

Capability

↓

Workflow Engine

requests

Capability

↓

Capability Registry

discovers

Candidate Skill Implementations

↓

Capability Resolver

selects

Skill

↓

Skill

implements

Capability

---

# Information Boundaries

Capability defines platform functionality.

It never owns:

- Plans
- Workflows
- Tasks
- Results
- Resources
- Knowledge
- Context

Capabilities remain implementation-independent throughout their lifecycle.

---

# Guiding Principle

Capabilities define **what** the platform can do.

Skills define **how** work is performed.

The Planner Engine determines **what Capabilities are required**.

The Workflow Engine determines **when they are used**.

The Capability Registry determines **what implementations are available**.

The Capability Resolver determines **which implementation should execute**.

---

# Related Documents

- 07_Planner_Engine.md
- 08_Workflow_Engine.md
- 15_Skill_Framework.md

---

# Related ADRs

- ADR_0009 — Skill Architecture
- ADR_0023 — Capability Discovery and Resolution