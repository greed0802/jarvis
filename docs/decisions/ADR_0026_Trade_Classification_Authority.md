---
adr: 0026
title: Trade Classification Authority
status: proposed
date: 2026-07-23
author: Cline
category: Domain
tags:
- Domain
- Classification
- BOQ
related:
- docs/domain/Trade_Taxonomy.md
- data/reports/eq0016_trade_classification_evidence.md
supersedes: null
superseded_by: null
---

# ADR_0026_Trade_Classification_Authority

## Context

CB-0005 implemented deterministic trade classification using Item Code prefixes discovered from CostX fixture analysis (EQ-0016). The implementation correctly classifies trades for BOQs with recognizable Item Code patterns (A-Z, AA-AZ, BA-BH).

During architectural review, an important observation was made: Item Codes are not universally present across all BOQ formats. Many BOQs use different identification systems that vary by client, consultant, office, or project. This observation indicates that while the current implementation is correct and production-ready for its designed scope, its applicability may be limited to specific BOQ formats.

## Decision

Preserve the current Item-Code-based trade classification implementation (CB-0005) as it is correct and valuable for supported formats. Launch EQ-0016 to investigate alternative evidence sources for universal trade classification across arbitrary BOQ formats.

## Rationale

The current evidence supports Item-Code-based classification for the analyzed CostX fixture. The applicability to arbitrary BOQs has not yet been established and requires further engineering investigation. This decision preserves working functionality while following an evidence-first approach to determine universal classification authority.

## Alternatives Considered

- **Remove current implementation**: Rejected as it would lose valuable functionality for supported formats
- **Force universal solution immediately**: Rejected due to insufficient evidence for alternative authorities
- **Mark as experimental**: Rejected as the implementation is production-ready for its scope

## Consequences

### Positive

- Preserves working functionality for CostX and similar formats
- No disruption to existing consumers
- Follows evidence-first engineering principles
- Maintains architectural integrity

### Negative

- Limited applicability to BOQs without recognizable Item Codes
- Universal solution requires additional engineering investigation
- Consumers must handle "UNKNOWN" classifications appropriately

## Review Trigger

Completion of EQ-0016 engineering investigation into alternative evidence sources for trade classification.

## Related Documents

- docs/domain/Trade_Taxonomy.md
- data/reports/eq0016_trade_classification_evidence.md
- docs/decisions/ADR_0005_Deterministic_Planner.md

## Related ADRs

- ADR_0005 — Deterministic Planner