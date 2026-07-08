---
adr: 0015
title: Result Persistence
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Result
tags:
  - Result
  - Persistence
related:
  - 03_Core_Ontology_Relationships.md
  - 10_Memory_Framework.md
supersedes: null
superseded_by: null
---

# ADR_0015_Result_Persistence

## Context

Jarvis requires a consistent lifecycle for Results to preserve valuable work and project history.

## Decision

Results are permanent records by default.

Results should be archived rather than permanently deleted under normal operating conditions.

Storage policies determine whether Results remain active or archived. Temporary Results may expire when storage limits require it.

## Rationale

User work is valuable and should remain recoverable whenever possible.

## Consequences

### Positive

- Preserves project history.
- Improves traceability.
- Supports audits and future reuse.

### Negative

- Requires storage management and archiving policies.

## Related Documents

- 03_Core_Ontology_Relationships.md
- 10_Memory_Framework.md
