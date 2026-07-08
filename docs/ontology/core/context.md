# Object: Context

Category:
Core / Intelligence

---

## Purpose

Context provides Jarvis with a complete and unified understanding of everything relevant to the current objective before planning or execution begins.

Context reduces ambiguity by assembling validated references from Resources, Memory, Knowledge, Users, Organizations, Workspaces, Projects, Permissions, Environment, and Intent into a single logical view.

Every Planner, Workflow, Skill, AI, Plugin, and Engine should operate using the same Context to ensure consistent reasoning and execution.

---

## Guiding Principle

Context answers the question:

> **"What information is relevant right now to make the correct decision?"**

---

## Guiding Philosophy

Context is the temporary universe in which Jarvis reasons.

It is not permanent storage.

It does not own information.

It references information.

Context exists only to ensure Jarvis fully understands the situation before planning or executing any action.

When Context changes, Jarvis adapts its reasoning accordingly while preserving consistency and minimizing ambiguity.

---

## Definition

Context is a dynamically assembled collection of validated references representing everything relevant to the current objective at a specific point in time.

Rather than storing duplicate information, Context references the latest validated information from across the Jarvis platform.

Context is created by the Context Engine and consumed by the Planner, Workflow Engine, Skills, AI, Plugins, and other platform components.

---

## Purpose of Context

Context exists to:

- Eliminate ambiguity.
- Increase execution confidence.
- Provide consistent reasoning.
- Reduce repetitive processing.
- Share a unified understanding across all Jarvis components.
- Allow users to modify assumptions without changing permanent data.

---

## Ownership

Context has no owner.

Context is generated dynamically.

It may be shared between:

- Planner
- Workflow Engine
- Skills
- AI
- Plugins
- GUI

while respecting user permissions and security.

---

## Sources

Context may reference:

- Resources
- Memory
- Knowledge
- Workspace
- Project
- User
- Organization
- Permissions
- Environment
- Installed Capabilities
- Active Workflows
- Intent

Future modules may contribute additional Context.

---

## References

Context stores references rather than copies.

This ensures:

- Single Source of Truth
- Reduced memory usage
- Consistent updates
- Better synchronization
- Easier validation

---

## Lifetime

Context exists only while it remains relevant.

Contexts may be:

- Request Context
- Conversation Context
- Workflow Context
- Workspace Context
- Project Context

Users may save, recall, edit, duplicate, or delete Context when appropriate.

---

## Mutation

Context is dynamic.

Users may:

- Add Context
- Remove Context
- Save Context
- Recall Context
- Create alternative Contexts

AI may suggest Context modifications.

The Context Engine validates all changes before applying them.

---

## Conflict Resolution

When conflicting information exists:

1. Detect the conflict.
2. Search Memory.
3. Search Knowledge.
4. Validate available evidence.
5. Ask the user for clarification.

Jarvis should never silently resolve significant ambiguity.

The user always has the final authority.

---

## Relationships

Context references:

- Resources
- Memory
- Knowledge
- Workspace
- Project
- User
- Organization
- Intent

Context is consumed by:

- Planner
- Workflow Engine
- Skills
- AI
- Plugins
- GUI

---

## States

- Building
- Active
- Updating
- Pending Clarification
- Saved
- Recalled
- Archived
- Expired

---

## Lifecycle

Intent Received

↓

Context Engine

↓

Context Built

↓

Planner

↓

Workflow

↓

Execution

↓

Context Updated

↓

Saved, Archived, or Expired

---

## Context is NOT

Context is not permanent knowledge.

Context is not memory.

Context is not a resource.

Context is not the planner.

Context does not execute work.

Context provides the complete, validated understanding required for Jarvis to make correct decisions.

---

## Future Expansion

Future versions may support:

- Context comparison
- Context branching
- Context snapshots
- Context confidence scoring
- Context inheritance
- Multi-user collaborative Context
- AI-assisted Context enrichment
- Semantic Context search