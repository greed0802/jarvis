# Object: Intent

Category:
Core / Intelligence

Definition

An Intent is Jarvis's structured understanding of what the user wants to achieve.

An Intent is independent of how the request was written.

Whether the request comes from text, voice, an API, or another system, it is converted into one or more Intents before any planning or execution begins.

An Intent never performs work.

It only describes the desired outcome.

---

Purpose

Intent represents Jarvis's structured understanding of the user's objective.

It provides the Planner Engine with a clear description of what should be achieved while remaining independent of how that objective will be accomplished.

Every workflow begins with one or more Intents.

Without an Intent, no planning or execution should occur.

---

Intent References

Intent references the Context against which it was interpreted.

Context remains owned by the Context Engine throughout its lifecycle.

• Goal

• Context

• Parameters

• Constraints

• Priority

• Required Inputs

• Expected Outputs

• Dependencies

• Confidence

• Ambiguities

• Attachments

• Approval Requirements

---

Goal

Defines what the user ultimately wants to achieve.

Examples:

• Build BOQ

• Compare Drawings

• Generate Report

• Export Workbook

• Search Knowledge

---

Context

The Context Engine interprets user requests using the current Context.

The resulting Intent maintains a reference to the Context against which it was interpreted.

This allows downstream Runtime Engines to understand both the objective and the supporting evidence.

Jarvis should evaluate:

• Workspace

• Project

• Memory

• Knowledge

• Resources

• Previous conversation

• Current task

The complete context always takes priority over isolated words.

---

Parameters

Intent should identify all available parameters.

Examples:

Trade

Zone

Level

Revision

Date

Template

Output Format

If required parameters are missing or ambiguous, the Context Engine should attempt to resolve them using available Context.

If ambiguity remains, the Planner Engine requests clarification before planning proceeds.

---

Attachments

An Intent may reference:

• Drawings

• Excel files

• PDFs

• Images

• Reports

• APIs

If required attachments are missing, the Planner should search available Resources and Memory before asking the user.

---

Confidence

Intent should include a confidence score representing how well Jarvis understands the user's objective.

Planning should not proceed until the Intent has sufficient confidence.

When confidence is insufficient, the Context Engine should expand understanding through additional Context, Memory, Knowledge, or user clarification.

Instead:

• Search Context

• Search Memory

• Search Knowledge

• Search Resources

• Ask Clarifying Questions

Jarvis should maximize confidence before planning.

---

Dependencies

One Intent may depend on another.

Example:

Intent 1

Build BOQ

↓

Intent 2

Compare BOQ

↓

Intent 3

Email Report

Dependent Intents should execute only after prerequisite Intents complete successfully.

---

Multiple Intents

One user request may contain multiple Intents.

Example:

"Build the BOQ, compare it to Revision B, then email the report."

Intent 1

Build BOQ

↓

Intent 2

Compare Revision

↓

Intent 3

Email Report

Each Intent may generate one or more Tasks during planning.

---

Relationships

User
      │
      ▼
User Request
      │
      ▼
Context Engine
      │
      ▼
Intent
      │
      ▼
Planner Engine
      │
      ▼
Plan
      │
      ▼
Workflow Engine

---

Intent Never

Intent never:

• Executes work

• Chooses Skills

• Chooses AI

• Chooses Workflows

• Calls Plugins

• Reads Resources directly

• Intent never owns Context

Those responsibilities belong to the Planner.

---

Lifecycle

User Request
      │
      ▼
Initial Intent
      │
      ▼
Context Assembly
      │
      ▼
Intent Interpretation
      │
      ▼
Intent Validation
      │
      ▼
Planner
      │
      ▼
Plan

---

Guiding Principle

Intent answers one question:

"What does the user want?"

Planning answers:

"How do we accomplish it?"

Execution answers:

"Let's do it."


# Related Documents

05_Data_Flow.md

06_Context_Engine.md

07_Planner_Engine.md

# Related ADR

ADR_0008 — Context

ADR_0005 — Deterministic Planner

ADR_0010 — Human Control

ADR_0021 — Control Plane and Data Plane Separation

ADR_0022 — Context Lifecycle and Ownership