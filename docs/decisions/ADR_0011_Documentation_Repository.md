---
adr: 0011
title: Decision Repository
status: accepted
date: 2026-07-08
author: Dhanrick Eviota
category: Documentation
tags:
  - Documentation
  - Decisions
  - ADR
related:
  - 01_Principles.md
  - 24_Development_Guide.md
supersedes: null
superseded_by: null
---

# ADR_0011_Decision_Repository

## Context

The project requires a permanent location for Architecture Decision Records (ADRs). The original proposal used `docs/adr/`, but a clearer directory structure was preferred.

## Decision

All Architecture Decision Records shall be stored under:

```
docs/
└── decisions/
```

The files will continue to use the ADR naming convention:

```
ADR_0001_Core_Ontology.md
ADR_0002_Workspace_vs_Project.md
...
```

A `README.md` inside `docs/decisions/` will serve as the index of all accepted architectural decisions and will eventually be generated automatically.

## Rationale

Using `docs/decisions/` is more descriptive and approachable than `docs/adr/` while still following the Architecture Decision Record methodology.

## Consequences

### Positive

- Easier for new contributors to understand.
- Clear separation between documentation and architectural decisions.
- Supports automatic documentation generation in the future.

### Negative

- Slightly departs from the common ADR folder naming convention, but retains ADR filenames for compatibility and clarity.

## Future Considerations

Documentation generation tools should automatically update `docs/decisions/README.md` whenever a new ADR is added.

## Related Documents

- 01_Principles.md
- 24_Development_Guide.md
