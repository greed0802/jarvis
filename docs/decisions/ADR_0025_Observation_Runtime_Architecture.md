---
adr: 0025
title: Observation Runtime Architecture
status: rejected
date: 2026-07-11
author: Dhanrick Eviota
category: Architecture
tags:
- Observation
- Parser
- Runtime
related:
- 05_Data_Flow.md
- design/M6_Observation_Model.md
- ontology/observation/
supersedes: null
superseded_by: null
---

# ADR_0025_Observation_Runtime_Architecture

## Context

The M6 implementation introduced the Observation Runtime as an architectural concept without an accompanying ADR. This ADR evaluates whether the Observation Runtime should be adopted as-proposed, revised, or rejected.

## Decision

Reject adoption of the Observation Runtime as the active production architecture for the current CostX acquisition scope.

## Evidence

Engineering Spike #1 (BOQ Row Analysis) demonstrated:

### Implementation Requirements
- **Runtime**: < 1 second for 6,350 rows
- **Lines of Code**: ~80 lines for complete BOQ row classification and sign validation
- **Classes/Abstractions**: None required; a flat script sufficed

### Row Classification Rules (observed from fixture)
- Column D matches `Head\d+` → Section headers (2,011 rows)
- Column D = `'Note'` → Note rows (520 rows)
- Column D = `'noidc'` + Column B = 'OMISSION/ADDITION' → Section boundaries (15 rows)
- Column A contains '/' and length > 2 → Item rows (3,615 rows)

### Sign Convention Validation
- Section state (single variable) was sufficient for tracking
- OMISSION section: 169 negative, 7 positive (anomalies)
- ADDITION section: 0 negative, 3 positive (correct)
- No font/style/border data was needed for classification

### Unexpected Findings
- Column D contains both semantic markers and legitimate UOM values (m2, m3, no)

## Rationale

The engineering spike did not naturally produce a need for runtime abstractions.

- **No consumer currently requires** Provenance tracking, font/style data, or ObservationSet
- **Column positions and marker conventions are format-specific** and not yet validated against additional fixtures
- **~80 lines of flat script** achieved the engineering goal without architectural overhead

The proposed Observation Runtime introduces complexity that is not justified by current evidence. A simpler acquisition mechanism without runtime abstractions better aligns with the YAGNI principle and the existing architecture preference for minimal, focused modules.

## Consequences

### Positive
- Avoids premature architectural commitment
- Simpler implementation path for CostX parsing
- Reduces coupling between acquisition and runtime concepts

### Negative
- Future multi-format or multi-source validation will require re-evaluation
- Domain rules discovered in this spike are not yet generalized

## Disposition

The Observation Runtime is not adopted as part of the active Jarvis architecture.

The supported production interface of `WorkbookParser` remains the M6.2 scope
(load → validate). The `observe()` method is not part of the supported production
parser interface and shall not be relied upon as a dependency for future
production milestones.

Future production implementation shall follow the accepted architecture in effect
after this decision.

The existing Observation implementation and documentation are retained as
historical engineering artifacts until a separate repository cleanup decision
is made.

## Engineering Backlog

- Repository Cleanup: retire Observation implementation (archived as separate item)

## Related Documents

- docs/reference/BOQ_Row_Analysis.md
- docs/design/M6_Observation_Model.md
- docs/ontology/observation/