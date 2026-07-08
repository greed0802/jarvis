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

Intent serves as the bridge between human communication and Jarvis's internal architecture.

Every workflow begins with one or more Intents.

Without an Intent, no planning or execution should occur.

---

Intent Contains

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

Intent should never be interpreted using only the current sentence.

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

If required parameters are missing or ambiguous, the Planner is responsible for requesting clarification.

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

Execution should never begin if confidence is below the acceptable threshold.

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

creates

Intent

Intent

uses

Context

Planner

consumes

Intent

Planner

creates

Plan

Workflow

executes

Plan

---

Intent Never

Intent never:

• Executes work

• Chooses Skills

• Chooses AI

• Chooses Workflows

• Calls Plugins

• Reads Resources directly

Those responsibilities belong to the Planner.

---

Lifecycle

Created

↓

Parsed

↓

Context Enriched

↓

Validated

↓

Planned

↓

Completed

or

Rejected

---

Guiding Principle

Intent answers one question:

"What does the user want?"

Planning answers:

"How do we accomplish it?"

Execution answers:

"Let's do it."