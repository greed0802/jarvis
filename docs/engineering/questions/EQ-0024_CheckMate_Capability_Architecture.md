# EQ-0024: CheckMate Capability Architecture

**Status:** FROZEN
**Date:** 2026-07-28
**Frozen Date:** 2026-07-29
**Authors:** Capability Workstream
**Prerequisites:** ADR-0027, ADR-0028, ADR-0029

---

## Core Architectural Invariant

**Invariant C1.1 (Evidence Primacy):** CheckMate SHALL consume BOQ Intelligence
evidence exclusively and SHALL NOT independently parse, reconstruct, or
re-evaluate underlying workbook or tabular semantics.

**Invariant C1.2 (Evidence Grounding):** Every Finding SHALL reference at least
one `EvidenceReference` locating the source evidence within parsed BOQ
Intelligence artifacts (cell, row, section, or aggregate range). The
`EvidenceReference` canonical model SHALL support:

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | string | Source BOQ Intelligence document identifier |
| `sheet` | string | Worksheet or tab name |
| `page` | integer \| null | Page number (optional, for paginated outputs) |
| `bbox` | object \| null | Bounding box coordinates (optional, for spatial sources) |
| `text_span` | object \| null | Text span within cell or paragraph (optional) |
| `evidence_id` | string | Reference to the parsed evidence record |
| `source_type` | enum | One of `cell`, `row`, `section`, `range`, `computed` |

---

## Out of Scope (Delegated to M10 Product Workbench)

The following concerns are explicitly excluded from EQ-0024 scope and
delegated to the M10 Product Workbench:

| Concern | Delegated To | Rationale |
|---------|-------------|-----------|
| UI framework selection (React, Tauri, etc.) | M10 Product Workbench | Presentation layer; zero impact on capability architecture |
| PDF rendering or document display | M10 Product Workbench | View layer; CheckMate produces structured findings, not visual output |
| Prompt engineering for AI Assistant | M10 Product Workbench | AI Assistant is a downstream consumer, not a CheckMate concern |
| LLM provider bindings or model selection | M10 Product Workbench | Infrastructure concern; CheckMate is provider-agnostic |
| Report layout or formatting | Formatter capability | Formatting is a distinct capability boundary |

---

## Evidence Granularity Hierarchy

CheckMate evidence artifacts are classified into four granularity levels:

| Level | Name | Description | Example |
|-------|------|-------------|---------|
| 1 | **ATOMIC** | A single typed cell value (numeric, string, unit) | `Sheet1!C42 = 12.5` |
| 2 | **STRUCTURAL** | A named row, section, or collection of related cells with defined schema | A BOQ item row with quantity, unit, rate |
| 3 | **AGGREGATE** | Computed summary values across STRUCTURAL records (sum, average, group) | `Total Concrete = SUM(concrete line items)` |
| 4 | **DERIVED** | Inferred measurements or computed features produced by BOQ Intelligence | `Steel ratio = steel_area / concrete_area` |

Rules SHALL declare their minimum required evidence level. Evidence resolution
MUST satisfy the declared level or produce an explicit finding.

**Invariant C1.3 (Scope Boundary):** CheckMate SHALL NOT generate summaries,
construct conversational context, render reports, or perform any function
outside rule evaluation and finding generation.

**Invariant C1.4 (Evidence Immutability):** Published BOQ Intelligence evidence
artifacts are immutable inputs to CheckMate. Once evidence for a run is
bound, it SHALL NOT be modified, extended, or reinterpreted during rule
evaluation.

**Invariant C1.5 (Deterministic Non-Evaluation):** When rule-required evidence
is missing (absent from the evidence snapshot), CheckMate SHALL produce an
explicit `UNEVALUABLE_MISSING_EVIDENCE` finding rather than run
ungrounded inference, silently skip the rule, or raise an exception.

---

## Finding Ontology (QS-Check Actionable Record)

A Finding is the public capability output. It is separate from raw rule
execution telemetry and answers six QS questions:

1. **What was checked** (rule identifier, version)
2. **What was found** (observed value vs. expected threshold)
3. **Where it was found** (one or more `EvidenceReference`)
4. **Severity & QS impact** (impact on quantity, safety, compliance)
5. **Why it matters** (risk statement)
6. **What to do** (actionable remediation guidance)

### Severity Taxonomy

| Severity | Label | Description |
|----------|-------|-------------|
| CRITICAL | Critical | Safety hazard, structural integrity compromised, cost/schedule project-level risk |
| MAJOR | Major Error | Significant quantity deviation (>5%), missing required item, standards non-conformance |
| MINOR | Minor Issue | Minor discrepancy, misspelling, formatting, non-material variance |
| INFORMATIONAL | Advisory Only | Informational note, no corrective action required |

**Invariant C1.6 (Finding Actionability & Provenance):** Every Finding SHALL
include a severity classification (CRITICAL, MAJOR, MINOR, INFORMATIONAL),
full evidence provenance (one or more `EvidenceReference`), and an
actionable remediation statement.

**Invariant C1.7 (Execution Outcome Separation):** Rule execution outcomes
(PASS, FAIL, NOT_APPLICABLE, UNEVALUABLE_MISSING_EVIDENCE) are telemetric
records distinct from actionable Findings. Only FAIL outcomes MAY generate
Findings.

---

## Rule Domain Taxonomy

QS rules are classified into six canonical domain categories based on
professional review practice:

| Domain | Category | Description | Min Evidence | Example |
|--------|----------|-------------|-------------|---------|
| MEASUREMENT | Quantity Validation | Verification of measured/calculated quantities, unit consistency, take-off accuracy | STRUCTURAL | Concrete volume vs. dimensional take-off |
| SPECIFICATION | Conformance Check | Assertion of item descriptions, material specs, execution clauses | STRUCTURAL | Steel grade matches project spec |
| COORDINATION | Cross-Reference Check | Consistency between related items, sheets, sections, or contracts | AGGREGATE | Door schedule vs. floor plan door count |
| COMPLIANCE | Standards Adherence | Compliance with building codes, industry standards, or regulatory requirements | STRUCTURAL | Stair riser height per building code |
| DOCUMENTATION_INTEGRITY | Data Quality | Completeness, correctness, and internal consistency of documentary evidence | ATOMIC | Missing unit rate on a rate item |
| PROJECT_POLICY | Client/Project Policy | Adherence to project-specific or client-defined business rules | DERIVED | Mark-up percentage exceeds client cap |

**Invariant C1.8 (Domain Rule Taxonomy):** All CheckMate rules SHALL be
classified into one of 6 canonical domain categories: MEASUREMENT,
SPECIFICATION, COORDINATION, COMPLIANCE, DOCUMENTATION_INTEGRITY,
PROJECT_POLICY.

**Invariant C1.9 (Rule Determinism):** Every CheckMate rule SHALL produce
deterministic output given the same BOQ evidence snapshot and rule version.
Rules SHALL NOT depend on external service calls, random number generators,
or mutable global state during evaluation.

---

## Rule Model & Registry Architecture

The rule architecture is governed by four core questions:

### Q1: Self-Containment
A CheckMate rule is a self-contained evaluation unit that declares its
domain category, minimum evidence level, parameter schema, version, and
contract compatibility assertions. The rule's evaluation logic operates
exclusively on its declared inputs.

### Q2: Execution Lifecycle
1. At run initiation, the registry resolves all eligible rules into an
   immutable **RuleSnapshot** bound to the run.
2. Each rule executes independently against the evidence snapshot.
3. Rule execution SHALL NOT mutate evidence, registered rules, or other
   rule results.
4. Results are collected as telemetric execution outcomes; only FAIL
   outcomes generate Findings per C1.7.

### Q3: Registry Governance Contract
The rule registry is the sole source of truth for all CheckMate rules. It
SHALL enforce:
- Unique rule identity and semantic versioning
- Domain category classification (C1.8)
- Minimum evidence level declaration
- Parameter schema validation on registration
- Immutable rule content after version publication

### Q4: Version Compatibility
A rule declares its contract compatibility boundary during
registration. When BOQ Intelligence evidence schema changes, the
compatibility check determines whether the existing rule version remains
evaluation-eligible. A rule whose declared contract no longer satisfies
the evidence schema SHALL produce UNEVALUABLE_MISSING_EVIDENCE (not
silent failure).

**Invariant C1.10 (Rule Self-Containment):** Each rule SHALL be a
self-contained evaluation unit with declared domain category, minimum
evidence threshold, parameter schema, version, and contract compatibility
assertions. Rule evaluation SHALL NOT depend on mutable global state or
the side effects of other rules.

**Invariant C1.11 (Bound RuleSnapshot Sovereignty):** At execution
initiation, the rule registry SHALL produce an immutable RuleSnapshot
containing all eligible rules bound to that run. Rules SHALL NOT
be added, removed, or modified after snapshot capture.

**Invariant C1.12 (Contract Compatibility Boundary):** Each rule SHALL
declare its contract compatibility boundary. When BOQ Intelligence
evidence schema changes result in a rule's declared contract being
unsatisfiable, the rule SHALL yield UNEVALUABLE_MISSING_EVIDENCE
rather than silently degrading or producing incorrect results.

---

## Public Capability Contract

The FindingReport is the public contract boundary of the CheckMate
capability. It decouples internal execution mechanics from public
consumption and presents a stable, technology-agnostic interface
for downstream consumers (Project Understanding, AI Assistant,
Formatter).

### FindingReport Schema Anatomy

| Section | Content | Purpose |
|---------|---------|---------|
| **Provenance** | Execution ID, evidence snapshot fingerprint, RuleSnapshot hash, execution timestamp, capability version | Full audit trail linking report to execution context |
| **Telemetry Summary** | Rule count (total, executed, unevaluable), execution duration, coverage percentage | Operational transparency without exposing internal mechanics |
| **Actionable Findings** | Sorted collection of Finding records (C1.6), each with severity, evidence provenance, risk statement, remediation | Consumer-ready violation intelligence |
| **Domain Coverage** | Rule count per domain category (C1.8), domain-level pass/fail/unavailable breakdown | QS domain-level compliance snapshot |

**Invariant C1.13 (Public Contract Decoupling):** The FindingReport SHALL
present a stable, technology-agnostic interface for external consumption.
Internal rule engine mechanics, execution state machine transitions, and
registry-implementation details SHALL NOT propagate into the public
contract.

**Invariant C1.14 (FindingReport Version Provenance):** Every FindingReport
SHALL contain a provenance block with execution ID, evidence snapshot
fingerprint, RuleSnapshot hash, and capability version. This entire
metadata block is embedded into the FindingReport for full
reproducibility verification.

**Invariant C1.15 (Report Completeness & Integrity):** A FindingReport
SHALL represent the complete, deterministic result of a single execution
run. Reports SHALL NOT be incrementally composed, partially updated, or
retroactively modified after publication.

---

## Vertical Slice Specification (M10 Readiness)

The vertical slice exercises all 15 prior invariants through a single
end-to-end execution: frozen BOQ evidence → deterministic CHECK
evaluation → Complete FindingReport publication.

### 5-Step Execution Pipeline

| Step | Action | Invariant Coverage |
|------|--------|-------------------|
| 1. **Evidence Binding** | Frozen BOQ Intelligence evidence snapshot bound to execution context | C1.1, C1.2, C1.4 |
| 2. **Rule Resolution** | RuleSnapshot with all eligible rules captured at run initiation | C1.8, C1.10, C1.11 |
| 3. **Evaluation** | Each rule executes independently against the evidence snapshot | C1.3, C1.5, C1.9, C1.12 |
| 4. **Finding Assembly** | FAIL outcomes repackaged as actionable Findings with severity, provenance, remediation | C1.6, C1.7 |
| 5. **Report Publication** | FindingReport assembled with Provenance, Telemetry Summary, Actionable Findings, Domain Coverage | C1.13, C1.14, C1.15 |

### Representative Rules

| Rule ID | Domain | Category | Expected Outcome |
|---------|----------------|-------------|-----------------|
| CHK-MEAS-001 | MEASUREMENT | Quantity Validation | PASS |
| CHK-COMP-001 | COMPLIANCE | Standards Adherence | FAIL → Finding (MAJOR) |
| CHK-SPEC-001 | SPECIFICATION | Conformance Check | FAIL → Finding (MAJOR) |
| CHK-COORD-001 | COORDINATION | Cross-Reference Check | FAIL → Finding (MINOR) |
| CHK-DOC-001 | DOCUMENTATION_INTEGRITY | Data Quality | UNEVALUABLE_MISSING_EVIDENCE |

### Telemetry Outcomes

| Outcome | Count | Rules |
|---------|-------|-------|
| PASS | 1 | CHK-MEAS-001 |
| FAIL (generates Findings) | 3 | CHK-COMP-001 (MAJOR), CHK-SPEC-001 (MAJOR), CHK-COORD-001 (MINOR) |
| UNEVALUABLE_MISSING_EVIDENCE | 1 | CHK-DOC-001 |

### Sample FindingReport Structure

```
FindingReport
├── Provenance (C1.14)
│   ├── execution_id
│   ├── evidence_fingerprint
│   ├── rule_snapshot_hash
│   └── capability_version
├── Telemetry Summary
│   ├── rule_count: 5
│   ├── executed: 4
│   ├── unavailable: 1
│   ├── duration_ms
│   └── coverage_pct
├── Actionable Findings (C1.6, C1.7)
│   ├── CHK-COMP-001 [MAJOR]
│   │   ├── evidence_reference
│   │   ├── risk_statement
│   │   └── remediation
│   ├── CHK-SPEC-001 [MAJOR]
│   │   ├── evidence_reference
│   │   ├── risk_statement
│   │   └── remediation
│   └── CHK-COORD-001 [MINOR]
│       ├── evidence_reference
│       ├── risk_statement
│       └── remediation
└── Domain Coverage (C1.8)
    ├── MEASUREMENT: 1/1
    ├── SPECIFICATION: 1/1
    ├── COORDINATION: 1/1
    ├── COMPLIANCE: 1/1
    └── DOCUMENTATION_INTEGRITY: 0/1
```

**Invariant C1.16 (Vertical Slice Specification Completeness):** The vertical
slice SHALL exercise all 16 prior invariants through at minimum 5
representative rules across at least 4 domain categories, demonstrating
PASS, FAIL, and UNEVALUABLE_MISSING_EVIDENCE outcomes in a single
FindingReport. This specification validates capability readiness for
Project Owner review before M10 implementation begins.

---






## Success Criteria (Definition of Done)

1. CheckMate capability responsibility matrix and non-goals are formally defined.
2. Input evidence contract and versioning expectations are frozen.
3. Canonical Finding ontology is frozen.
4. Rule taxonomy classes are established.
5. Deterministic rule model and registry architecture are determined.
6. Public capability contract (Finding Report) is frozen.
7. A minimal deterministic vertical slice (M10 readiness) is specified
   for PO review.

---

## Discovery Constraints

1. **Domain Consumer Boundary**: CheckMate is a consumer layer above BOQ
   Intelligence. It MUST NOT modify, extend, or re-run parser or BOQ
   Intelligence logic.
2. **Runtime Architectural Firewall**: EQ-0024 SHALL NOT introduce new execution
   runtime architecture or modify frozen runtime ADRs (ADR-0027, ADR-0028,
   ADR-0029). If investigation finds defects in runtime ADRs, they
   SHALL be recorded as architecture feedback, not resolved within
   EQ-0024.
3. **Exploratory Discipline**: Investigation spikes MUST state inquiry
   objectives rather than predetermining architectural outcomes or
   implementation schemas.
4. **Decoupled Implementation**: EQ-0024 governs architectural discovery only.
   Implementation work (M10 Milestone) is out of scope for closing
   this Engineering Question and must follow PO Review and Capability ADR
   authoring.

---

## Exploration Roadmap

### Spike 1 — Capability Boundary
Investigate CheckMate domain responsibilities, non-goals, and capability
boundaries relative to BOQ Intelligence, Formatter, and future AI Assistant
layers.
- **Objective:** Define CheckMate domain responsibilities, non-goals, and
  capability boundaries relative to sibling capabilities (Project
  Understanding, AI Assistant, Formatter).
- **Hypothesis:** CheckMate is strictly a compliance/validation engine that
  evaluates evidence against rules to yield structured findings; it does not
  generate summaries, construct conversational context, or render reports.
- **Disposition:** Approved. CheckMate's domain boundary is strictly
  limited to rule evaluation and finding generation. Summarization belongs
  to Project Understanding, draft synthesis to AI Assistant, and layout
  rendering to Formatter.
- **Candidate Invariants:** Approved Invariant C1.3 (Scope Boundary).
- **ADR Mapping:**

### Spike 2 — Evidence Contract
Inventory BOQ Intelligence artifacts and determine mandatory/optional evidence
schemas and versioning support for CheckMate consumption.
- **Objective:** Determine the minimal evidence requirements, granularity
  hierarchy, and immutability guarantees needed for deterministic
  CheckMate rule evaluation over BOQ Intelligence evidence.
- **Hypothesis:** CheckMate requires a 4-tier evidence hierarchy where
  published evidence artifacts are strictly immutable inputs, allowing rules
  to declare precise minimum evidence dependencies and fail gracefully when
  evidence is missing.
- **Disposition:** Approved with Refinements. Rules must declare their
  minimum required evidence level. Missing evidence results in an explicit
  `UNEVALUABLE_MISSING_EVIDENCE` finding rather than ungrounded inference
  or exceptions.
- **Candidate Invariants:** Approved Invariant C1.4 (Evidence Immutability),
  Invariant C1.5 (Deterministic Non-Evaluation).
- **ADR Mapping:**

### Spike 3 — Finding Ontology
Determine the canonical Finding model, violation models, severity
classifications, evidence links, and provenance structures.
- **Objective:** Determine the canonical Finding ontology, violation models,
  severity classifications, evidence links, and provenance structures.
- **Hypothesis:** Findings must be cleanly separated from raw rule execution
  outcomes (PASS, FAIL, NOT_APPLICABLE, UNEVALUABLE_MISSING_EVIDENCE) and
  encapsulate complete proof, QS impact, and actionable remediation guidance.
- **Disposition:** Approved with Refinements. Rule execution telemetry is
  separated from actionable Findings. Findings answer 6 QS questions and
  carry explicit severity levels (CRITICAL, MAJOR, MINOR, INFORMATIONAL).
- **Candidate Invariants:** Approved Invariant C1.6 (Finding Actionability &
  Provenance), Invariant C1.7 (Execution Outcome Separation).
- **ADR Mapping:**

### Spike 4 — Rule Taxonomy
Classify the categories of rules CheckMate must support in deterministic QS
compliance evaluation over structural evidence.
- **Objective:** Classify the categories of professional Quantity Surveying
  rules CheckMate must evaluate deterministically over QS Intelligence
  evidence payloads.
- **Hypothesis:** QS rules fall into 6 domain categories based on
  professional review practice rather than software mechanics.
- **Disposition:** Approved. Established the 6 canonical QS domain
  categories (MEASUREMENT, SPECIFICATION, COORDINATION, COMPLIANCE,
  DOCUMENTATION_INTEGRITY, PROJECT_POLICY).
- **Candidate Invariants:** Approved Invariant C1.8 (Domain Rule Taxonomy),
  Invariant C1.9 (Rule Determinism).
- **ADR Mapping:**

### Spike 5 — Rule Model & Registry Architecture
Investigate deterministic rule execution and determine the appropriate
self-describing rule specification, parameterization model, contract
compatibility rules, and registry, governance architecture.
- **Objective:** Investigate deterministic rule execution and determine the
  appropriate self-describing rule specification, parameterization model,
  contract compatibility rules, and registry governance.
- **Hypothesis:** Rules must be self-contained, semantically versioned,
  and evaluated against an immutable RuleSnapshot captured at run
  initiation, with explicit evidence contract compatibility checks.
- **Disposition:** Approved. Established the 4-part Rule Architecture
  (Self-Containment, Execution Lifecycle, Registry Governance Contract,
  Version Compatibility) and RuleSnapshot pattern.
- **Candidate Invariants:** Approved Invariant C1.10 (Rule Self-
  Containment), Invariant C1.11 (Bound RuleSnapshot Sovereignty),
  Invariant C1.12 (Contract Compatibility Boundary).
- **ADR Mapping:**

### Spike 6 — Public Capability Contract
Determine the public interface of the capability (FindingReport, summary
statistics, rule coverage metadata, version provenance).
- **Objective:** Determine the public interface of the CheckMate
  capability (FindingReport, summary statistics, rule coverage metadata,
  version provenance).
- **Hypothesis:** Downstream consumers require a stable, technology-
  agnostic FindingReport contract that isolates internal rule engine
  mechanics from public consumption.
- **Disposition:** Approved. Established the 4-tier FindingReport schema
  (Provenance, Telemetry Summary, Actionable Findings, Domain Coverage)
  and decoupled internal execution mechanics from public reporting.
- **Candidate Invariants:** Approved Invariant C1.13 (Public Contract
  Decoupling), Invariant C1.14 (FindingReport Version Provenance),
  Invariant C1.15 (Report Completeness & Integrity).
- **ADR Mapping:**

### Spike 7 — Vertical Slice Specification (M10 Readiness)
Specify the minimal end-to-end execution scenario (frozen BOQ evidence → ~5
deterministic rules → FindingReport) to validate capability specification
readiness for Project Owner review.
- **Objective:** Specify the minimal end-to-end execution scenario (frozen
  BOQ evidence → ~5 deterministic rules → FindingReport) to validate
  capability specification readiness for Project Owner review.
- **Hypothesis:** An end-to-end scenario exercising all 16 prior
  invariants across representative rule categories and outcomes proves
  capability readiness for PO Review and M10 implementation.
- **Disposition:** Approved. Established the Vertical Slice
  Specification with 5 representative rules (CHK-MEAS-001 to CHK-DOC-001),
  executing the full 5-step pipeline and producing PASS, FAIL, and
  UNEVALUABLE_MISSING_EVIDENCE outcomes in a valid FindingReport.
- **Candidate Invariants:** Approved Invariant C1.16 (Vertical Slice
  Specification Completeness).
- **ADR Mapping:**

---

## Freeze Record

| Field | Value |
|-------|-------|
| **Frozen Date** | 2026-07-29 |
| **ADR Mapping** | ADR-0030, ADR-0031, ADR-0032 |
| **PO-DEC References** | `docs/architecture/reviews/EQ-0024_Project_Owner_Review.md` |
