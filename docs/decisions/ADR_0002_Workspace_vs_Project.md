---
adr: 0002
title: Workspace vs Project
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Ontology
tags:
- Workspace
- Project
related:
- 03_Core_Ontology_Relationships.md
supersedes: null
superseded_by: null
---

# ADR_0002_Workspace_vs_Project

## Context

Clarify ownership of data and working context.

## Decision

Projects own data. Workspaces own context.

## Rationale

Separating persistent data from active context simplifies collaboration and synchronization.

## Alternatives Considered

- Alternative approaches were discussed during architecture design.
- The selected approach best supports Jarvis's long-term modular architecture.

## Consequences

- Projects become source of truth
- Workspaces remain lightweight.

## Future Considerations

This decision may be revisited if future platform requirements fundamentally change, but it should remain stable unless superseded by a new ADR.

## Related Documents

03_Core_Ontology_Relationships.md
