# Planner Engine

Version: 1.0

---

## Definition

The Planner Engine is the second Core Runtime Engine of the Jarvis Data Plane.

It transforms validated Context and interpreted Intent into one or more executable Plans.

The Planner Engine determines **what should be done** to achieve the current objective.

It does not coordinate execution, invoke Skills, perform work, or generate Results.

---

## Purpose

The Planner Engine exists to produce safe, deterministic, explainable, and effective Plans for accomplishing the current objective.

It evaluates Context, Intent, constraints, risks, and available platform capabilities before proposing one or more Plans.

The Planner Engine provides strategy.

Execution belongs to the Workflow Engine.

---

## Scope

The Planner Engine owns planning.

It does not:

- Own Context
- Own Intent
- Coordinate Workflows
- Create Tasks
- Select Skill implementations
- Execute Skills
- Produce Results
- Validate Results
- Promote Knowledge

Those responsibilities belong to the appropriate Runtime Engines and Frameworks.

---

## Planning Philosophy

Planning determines the strategy.

Execution performs the strategy.

The Planner Engine proposes what should happen without performing any work itself.

Planning should remain deterministic, explainable, and auditable.

AI may assist planning but never replace deterministic decision making.

---

## Responsibilities

### Plan Construction

- Analyze Context
- Evaluate Intent
- Generate Plans
- Evaluate constraints
- Assess risks
- Generate alternative Plans
- Identify required Capabilities

### Plan Evaluation

- Compare alternative Plans
- Estimate planning confidence
- Validate planning assumptions
- Recommend the preferred Plan

### Clarification

- Detect ambiguity
- Detect missing information
- Request clarification when required
- Prevent planning with insufficient understanding

### Plan Coordination

- Publish approved Plans
- Submit approved Plans to the Workflow Engine

---

## Ownership

The Planner Engine exclusively owns:

- Plans

No other Runtime Engine or Framework may directly modify an approved Plan.

Plan revisions remain the responsibility of the Planner Engine.

---

## Lifetime

The Planner Engine is invoked for each planning cycle.

It consumes Context and Intent, produces one or more Plans, and completes its work.

If replanning is required, a new planning cycle begins.

---

## Communication

The Planner Engine consumes:

- Context
- Intent

The Planner Engine produces:

- Plan

Approved Plans are provided to the Workflow Engine through defined runtime interfaces.

The Planner Engine may receive replanning requests from the Workflow Engine.

---

## Extensibility

The Planner Engine remains independent of specific Skills, Providers, and implementation technologies.

New planning strategies, optimization methods, and decision policies may be introduced without changing the Planner Engine's fundamental responsibilities.

---

## Planning Lifecycle

```text
Context
      │
      ▼
Intent
      │
      ▼
Plan Construction
      │
      ▼
Alternative Evaluation
      │
      ▼
Risk Assessment
      │
      ▼
Planning Confidence
      │
      ▼
Approved Plan
      │
      ▼
Workflow Engine
```

---

## Planning Confidence

The Planner Engine evaluates whether sufficient understanding exists before producing an approved Plan.

Planning confidence is based on explainable planning conditions rather than arbitrary numerical scores.

Planning states may include:

- Sufficient Understanding
- Context Gap
- Knowledge Gap
- Capability Ambiguity
- User Clarification Required

The Planner Engine never proceeds with unresolved ambiguity.

---

## Planning Modes

The Planner Engine may generate multiple Plans, including:

- Preferred Plan
- Alternative Plan
- Fallback Plan
- User-Constrained Plan

Alternative Plans provide explainable options without altering the user's objective.

---

## Capability Identification

The Planner Engine identifies the Capabilities required to accomplish an objective.

The Planner Engine does not select Skill implementations.

Capability discovery and runtime implementation selection are defined by ADR_0023.

---

## Relationships

The Planner Engine collaborates with:

- Context Engine
- Workflow Engine
- AI Framework
- Validation Framework

The Planner Engine does not directly coordinate execution or communicate with Skills.

---

## Information Boundaries

### Information entering the Planner Engine

- Context
- Intent

### Information produced

- Plan

### Information that never belongs to the Planner Engine

- Workflow
- Tasks
- Skill Implementations
- Results
- Knowledge
- Persistent Memory

---

## Failure Management

The Planner Engine must never guess.

When planning cannot be completed with sufficient confidence, the Planner Engine follows this escalation sequence:

1. Re-evaluate Context.
2. Consult Memory and Knowledge.
3. Request AI assistance when appropriate.
4. Request user clarification.

Planning stops until sufficient understanding has been established.

---

## Determinism

The Planner Engine is deterministic by default.

AI may assist by proposing alternatives, identifying constraints, or suggesting strategies.

All AI recommendations must be evaluated and approved by the Planner Engine before becoming part of an approved Plan.

Execution never proceeds based solely on AI-generated recommendations.

---

## Golden Rule

The Planner Engine determines what should be done.

It never performs the work.

---

## Guiding Principle

> **Given the current Context and Intent, what is the safest, most explainable, and most effective way to achieve the objective?**

---

## Related Documents

- 05_Data_Flow.md
- 06_Context_Engine.md
- 08_Workflow_Engine.md
- 15_Skill_Framework.md

---

## Related ADRs

- ADR_0005 — Deterministic Planner
- ADR_0008 — Context
- ADR_0009 — Skill Architecture
- ADR_0010 — Human Control
- ADR_0013 — Workflow Ownership
- ADR_0014 — Workflow Determinism
- ADR_0020 — Runtime vs. Cross-Cutting Architecture
- ADR_0021 — Control Plane and Data Plane Separation
- ADR_0022 — Context Lifecycle and Ownership
- ADR_0023 — Capability Discovery and Resolution