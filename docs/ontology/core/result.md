# Result

## Definition

A Result is the validated product of Jarvis. It is the final outcome produced to satisfy a user's Intent after planning, execution, verification, and quality assurance.

A Result represents the successful completion of one or more Workflows and serves as the tangible evidence that Jarvis has fulfilled the user's objective.

A Result is not merely an answer; it is the product of the entire platform.

---

## Purpose

The Result exists to deliver value to the user.

It represents the culmination of planning, workflow execution, skill execution, validation, and quality assurance into a concrete, usable product.

Every process inside Jarvis ultimately exists to produce Results.

---

## Ownership

Result ownership follows the platform hierarchy.

- **User** owns personal Results.
- **Workspace** manages active Results within a session.
- **Project** stores project Results as permanent records.
- **Organization** may own shared Results.
- **Platform** defines the Result architecture but does not own user data.

During creation:

- Skills produce intermediate Results.
- Workflows validate and combine Results.
- The Planner performs quality review before delivery.
- Jarvis delivers the final Result to the user.

---

## Lifetime

Results are permanent records unless explicitly archived.

Results should not be permanently deleted under normal circumstances.

Storage policies determine whether Results remain active or archived.

If storage limits are exceeded:

- Final Results may be archived.
- Temporary Results may expire.
- Results remain recoverable where storage policies allow.

---

## Types

Examples include:

- Intermediate Result
- Draft Result
- Validation Result
- Error Result
- Comparison Result
- Report Result
- Final Result

Intermediate Results exist for execution.

Final Results exist for users.

---

## Confidence

Every Result contains a confidence assessment.

Only Results meeting the required confidence threshold should be delivered as Final Results.

The confidence calculation should remain transparent and explainable.

Users may choose to accept lower-confidence Results when appropriate.

---

## Relationships

Results may be chained.

Example:

Raw Data
↓

Processed Data
↓

Analysis
↓

BOQ
↓

QA Report
↓

Final Report

Each Result may become the input Resource for another Workflow.

---

## History

Every Result should preserve traceability, including:

- Intent
- Context
- Workflow
- Planner
- Skills
- Resources
- Validation history
- Confidence
- Timestamp

Results should be reproducible whenever possible.

---

## Guiding Principle

A Result answers the question:

> **"What was produced, and how can it be trusted?"**