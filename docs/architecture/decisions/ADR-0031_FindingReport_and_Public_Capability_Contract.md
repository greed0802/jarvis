# ADR-0031: FindingReport & Public Capability Contract

**Status:** FROZEN
**Date:** 2026-07-29
**Frozen Date:** 2026-07-29
**Authors:** Capability Workstream
**Prerequisites:** ADR-0030, EQ-0024 (FROZEN)
**Source Review:** `docs/architecture/reviews/EQ-0024_Project_Owner_Review.md`

---

## Context

EQ-0024 defined CheckMate's output model: actionable Findings separated
from raw execution telemetry, delivered through a stable, technology-agnostic
FindingReport. This ADR codifies the evidence grounding, Finding ontology,
and public capability contract from the frozen EQ-0024 discovery.

---

## Decision

### Invariant 1 — Evidence Grounding (C1.2)

Every Finding SHALL reference at least one `EvidenceReference` locating the
source evidence within parsed BOQ Intelligence artifacts. The canonical
`EvidenceReference` model SHALL support:

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | string | Source BOQ Intelligence document identifier |
| `sheet` | string | Worksheet or tab name |
| `page` | integer \| null | Page number (optional) |
| `bbox` | object \| null | Bounding box coordinates (optional) |
| `text_span` | object \| null | Text span within cell or paragraph (optional) |
| `evidence_id` | string | Reference to the parsed evidence record |
| `source_type` | enum | `cell`, `row`, `section`, `range`, `computed` |

**Rationale:** Every Finding must be traceable back to its source evidence
for auditability and downstream consumer trust. The flexible optional
fields accommodate different evidence source types without mandating
spatial coordinates for non-spatial evidence.

### Invariant 2 — Finding Actionability & Provenance (C1.6)

Every Finding SHALL include a severity classification (CRITICAL, MAJOR,
MINOR, INFORMATIONAL), full evidence provenance (one or more
`EvidenceReference`), and an actionable remediation statement.

**Rationale:** Findings that lack remediation guidance or provenance are
not actionable for QS professionals. The 6 QS questions (What was checked,
What was found, Where, Severity & Impact, Why it matters, What to do)
ensure every Finding is complete and self-contained.

### Invariant 3 — Execution Outcome Separation (C1.7)

Rule execution outcomes (PASS, FAIL, NOT_APPLICABLE,
UNEVALUABLE_MISSING_EVIDENCE) are telemetric records distinct from
actionable Findings. Only FAIL outcomes MAY generate Findings.

**Rationale:** PASS and NOT_APPLICABLE outcomes are not violations and
should not pollute the actionable Finding stream. UNEVALUABLE_MISSING_EVIDENCE
indicates insufficient input, not a rule violation. Only FAIL outcomes
represent confirmed issues requiring QS attention.

### Severity Taxonomy

| Severity | Label | Description |
|----------|-------|-------------|
| CRITICAL | Critical | Safety hazard, structural integrity compromised, cost/schedule project-level risk |
| MAJOR | Major Error | Significant quantity deviation (>5%), missing required item, standards non-conformance |
| MINOR | Minor Issue | Minor discrepancy, misspelling, formatting, non-material variance |
| INFORMATIONAL | Advisory Only | Informational note, no corrective action required |

### Invariant 4 — Public Contract Decoupling (C1.13)

The FindingReport SHALL present a stable, technology-agnostic interface for
external consumption. Internal rule engine mechanics, execution state machine
transitions, and registry-implementation details SHALL NOT propagate into
the public contract.

**Rationale:** Downstream consumers (Project Understanding, AI Assistant,
Formatter) must not couple to CheckMate's internal execution model. The
FindingReport is a capability contract, not a debug log.

### Invariant 5 — FindingReport Version Provenance (C1.14)

Every FindingReport SHALL contain a provenance block with execution ID,
evidence snapshot fingerprint, RuleSnapshot hash, and capability version.
This metadata block is embedded into the FindingReport for full
reproducibility verification.

**Rationale:** Reproducibility is a core CheckMate requirement. Any
FindingReport must be traceable back to the exact evidence, rules, and
capability version that produced it.

### Invariant 6 — Report Completeness & Integrity (C1.15)

A FindingReport SHALL represent the complete, deterministic result of a
single execution run. Reports SHALL NOT be incrementally composed,
partially updated, or retroactively modified after publication.

**Rationale:** Incremental or partial reports create ambiguity about what
was and was not checked. A complete, atomic FindingReport eliminates the
need for consumers to track partial state.

### FindingReport Schema Anatomy

| Section | Content | Purpose |
|---------|---------|---------|
| **Provenance** | Execution ID, evidence fingerprint, RuleSnapshot hash, timestamp, capability version | Full audit trail |
| **Telemetry Summary** | Rule count (total, executed, unevaluable), execution duration, coverage % | Operational transparency |
| **Actionable Findings** | Sorted Finding records with severity, evidence provenance, risk, remediation | Consumer-ready violation intelligence |
| **Domain Coverage** | Rule count per domain category, domain-level pass/fail/unavailable | QS domain-level compliance snapshot |

---

## Consequences

- FindingReport is the sole public output of the CheckMate capability.
- Internal execution telemetry is never exposed to downstream consumers.
- Every FindingReport is independently reproducible from its provenance block.
- Partial or incremental reports are prohibited; each report is atomic.
- Downstream consumers (Project Understanding, AI Assistant, Formatter)
  integrate against the FindingReport contract, not CheckMate internals.

---

## Related Capability ADRs

- **ADR-0030**: Defines CheckMate capability boundaries and domain taxonomy.
- **ADR-0032**: Defines the `RuleSnapshot`, rule model, and evidence contract.

---

## Freeze Record

| Field | Value |
|-------|-------|
| **Frozen Date** | 2026-07-29 |
| **PO-DEC Reference** | `docs/architecture/reviews/EQ-0024_Project_Owner_Review.md` |
