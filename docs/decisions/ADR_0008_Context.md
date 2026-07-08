---
adr: 0008
title: Context
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Context
tags:
- Context
related:
- 06_Context_Engine.md
supersedes: null
superseded_by: null
---

# ADR_0008_Context

## Context

Define how context is formed.

## Decision

Context is dynamically assembled and stores references instead of copies.

## Rationale

Context should remain lightweight and current.

## Alternatives Considered

- Alternative approaches were discussed during architecture design.
- The selected approach best supports Jarvis's long-term modular architecture.

## Consequences

- Reduced duplication.

## Future Considerations

This decision may be revisited if future platform requirements fundamentally change, but it should remain stable unless superseded by a new ADR.

## Related Documents

06_Context_Engine.md
