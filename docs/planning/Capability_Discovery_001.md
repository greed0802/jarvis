# Capability Discovery 001

Date: 2026-07-13
Status: Complete — Pending Project Owner Decision

---

## Purpose

This document records the first formal Capability Discovery under the Capability Era governance process established in `docs/planning/Capability_Roadmap.md`.

Capability Discovery identifies candidate capabilities from three sources:
1. Production Evidence
2. Engineering Backlog
3. User Needs

---

## Discovery Sources

### 1. Production Evidence

**What does the current production pipeline produce?**

Current production types:
- `WorkbookParser` — loads and validates CostX workbooks
- `extract_boq()` — extracts structured `BOQRow` objects from validated workbooks
- `BOQRow` — dataclass with 7 fields (code, description, quantity, uom, classification, section, sign_valid)

Current production output (verified against `full_boq.xlsx`):
- 6,349 BOQRow objects
- Classification counts: Item 3,605 / Head 2,011 / Note 520 / Section 15 / Other 198
- 7 known OMISSION anomalies reproduced (positive quantities where negative expected)
- 10 committed regression tests passing

**What is missing?**

- No validation beyond extraction (sign convention is extracted but not validated as a feature)
- No summaries or statistics (counts, totals, section breakdown)
- No export functionality (CSV, JSON, human-readable reports)
- No anomaly detection or reporting (the 7 anomalies are observable but not surfaced as a feature)
- No section analysis (section boundaries are tracked but not analyzed)
- No trade breakdown or categorization
- No duplicate detection or quality checking

**Evidence sources:**
- EQ-0001 (ANSWERED) — UOM-based classification is deterministic
- EQ-0002 (ANSWERED) — Sign convention validation mechanism is proven
- EQ-0006 (ANSWERED) — 7 anomalies confirmed as data-entry errors
- EQ-0007 (ANSWERED) — Production extraction verified, regression tests passing
- EQ-0005 (EVIDENCE COMPLETE) — UOM semantics survive across 2 fixtures, structural assumptions falsified
- EQ-0009 (EVIDENCE COMPLETE) — Extraction is not Context assembly

### 2. Engineering Backlog

**What investigations have been completed or are pending?**

Completed investigations:
- EQ-0001: BOQ row identification via UOM markers (ANSWERED)
- EQ-0002: Sign convention validation mechanism (ANSWERED)
- EQ-0003: CostX export format characteristics (ANSWERED)
- EQ-0004: Observation Runtime architecture (ANSWERED — rejected by ADR-0025)
- EQ-0005: BOQ semantic generalization (EVIDENCE COMPLETE — Rule of Three not met)
- EQ-0006: Anomaly domain interpretation (ANSWERED — data-entry errors)
- EQ-0007: Minimum production extraction (ANSWERED)
- EQ-0009: Context discovery (EVIDENCE COMPLETE — extraction ≠ understanding)

Pending investigations:
- EQ-0008: Deterministic header/worksheet discovery (CANDIDATE — requires additional fixtures)

**Key findings from engineering backlog:**
- UOM-based classification is stable across 2 observed fixtures
- Structural assumptions (worksheet name, header position, first data row) are export-specific
- Rule of Three not met for parser generalization (need 3+ structurally different fixtures)
- Context Engine architecture exists but has no production evidence

### 3. User Needs

**What do professional users need that the platform cannot currently provide?**

Based on the repository's focus on Quantity Surveying and CostX integration:

- **BOQ validation and quality checking** — Detect data-entry errors, missing descriptions, invalid UOMs, duplicate codes
- **Structured summaries and statistics** — Row counts by classification, section breakdown, quantity totals, trade analysis
- **Data export in usable formats** — CSV, JSON, human-readable reports for downstream use
- **Anomaly detection and reporting** — Surface the 7 known anomalies and detect new ones
- **Section analysis** — Understand section structure, identify missing sections, analyze section boundaries
- **Trade breakdown** — Categorize BOQ items by trade (structural, architectural, mechanical, electrical)
- **Duplicate detection** — Identify duplicate item codes or descriptions
- **Missing data detection** — Flag items missing descriptions, quantities, or UOMs

---

## Candidate Capabilities

Based on the three discovery sources, the following candidate capabilities are identified:

### Candidate 1: BOQ Intelligence

**Description:** Validation, analysis, summaries, exports, and anomaly detection over `list[BOQRow]`.

**Source:** Production evidence + user need

**Preliminary Assessment:**
- User Value: High — directly addresses professional QS workflow needs
- Engineering Effort: Low — pure functions over existing production types
- Evidence Readiness: High — all rules trace to answered EQs or documented office standards
- Architectural Impact: None — no new engines, frameworks, or runtime components

**Evidence Trace:**
- Section sign validation: EQ-0002 (mechanism proven), EQ-0006 (anomalies confirmed)
- Row classification consistency: EQ-0001 (UOM-based classification verified)
- Anomaly detection: EQ-0006 (7 anomalies reproducible)
- Summaries/statistics: Observable from `list[BOQRow]` (EQ-0007 verified counts)
- Export functionality: Formatting over existing data structure
- Domain rules (duplicates, missing data): Office standards documented in `docs/reference/office_standards/`

**Features (incremental):**
1. Section sign validation (engineering-derived)
2. Row classification consistency (engineering-derived)
3. Anomaly detection (engineering-derived)
4. Deterministic summaries and statistics (engineering-derived)
5. Section analysis (engineering-derived)
6. Trade breakdown (domain rule)
7. Duplicate code detection (domain rule)
8. Missing description / UOM checks (domain rule)
9. CSV / JSON export (engineering)
10. Human-readable summary report (engineering)

**Constraints:**
- No architectural expansion
- Pure functions over `list[BOQRow]`
- No modification to parser
- No runtime registration

---

### Candidate 2: Formatter

**Description:** Structured output formatting for BOQ data.

**Source:** User need

**Preliminary Assessment:**
- User Value: Medium — useful but dependent on BOQ Intelligence for validation
- Engineering Effort: Low — formatting over existing data
- Evidence Readiness: Medium — depends on BOQ Intelligence being complete
- Architectural Impact: None

**Evidence Trace:**
- Formatting is a presentation concern over existing data
- No engineering questions required — formatting is straightforward

**Features:**
- CSV export
- JSON export
- Human-readable report

**Dependencies:**
- BOQ Intelligence (validation should precede export)

---

### Candidate 3: CheckMate

**Description:** QA checking against domain rules.

**Source:** User need

**Preliminary Assessment:**
- User Value: High — professional QA is critical for QS work
- Engineering Effort: Medium — requires domain rule catalog
- Evidence Readiness: Medium — domain rules exist but need formal cataloging
- Architectural Impact: None

**Evidence Trace:**
- Domain rules from office standards (e.g., `12_Units of Measurements.docx`)
- Duplicate detection, missing data checks are standard QA practices
- Requires Project Owner or QS authority to define rule catalog

**Features:**
- Duplicate item code detection
- Missing description detection
- Missing UOM detection
- Invalid UOM detection
- Custom rule definitions

**Dependencies:**
- Domain rule catalog (requires QS authority)

---

### Candidate 4: Cubit Parser

**Description:** Deterministic extraction from Cubit exports.

**Source:** Engineering backlog

**Preliminary Assessment:**
- User Value: Medium — expands platform to second estimating platform
- Engineering Effort: Medium — similar to CostX parser but different format
- Evidence Readiness: Low — no fixtures, no engineering evidence
- Architectural Impact: None (yet)

**Evidence Trace:**
- No Cubit fixtures available
- No engineering investigation completed
- Requires Project Owner to provide fixtures

**Prerequisites:**
- Cubit export fixtures
- Engineering Question to investigate Cubit export structure

---

### Candidate 5: PDF Parser

**Description:** Extraction from PDF documents.

**Source:** Engineering backlog

**Preliminary Assessment:**
- User Value: Low — PDF extraction is complex and error-prone
- Engineering Effort: High — PDF parsing requires significant engineering
- Evidence Readiness: Very Low — no fixtures, no evidence
- Architectural Impact: None (yet)

**Evidence Trace:**
- No PDF fixtures available
- No engineering investigation completed
- PDF extraction is fundamentally different from structured workbook extraction

**Prerequisites:**
- PDF fixtures
- Engineering Question to investigate PDF structure
- Evaluation of PDF parsing libraries

---

### Candidate 6: AI-Assisted Estimation

**Description:** AI-supported cost estimation.

**Source:** User need

**Preliminary Assessment:**
- User Value: High — AI-assisted estimation is a strategic capability
- Engineering Effort: High — requires AI integration, training data, validation
- Evidence Readiness: Very Low — no foundation, no training data
- Architectural Impact: Potentially significant — may require Context Engine, Knowledge Framework

**Evidence Trace:**
- No AI integration exists
- No training data available
- Context Engine architecture exists but has no production evidence (EQ-0009)
- Requires significant architectural work

**Prerequisites:**
- BOQ Intelligence (structured data foundation)
- Context Engine (for AI context assembly)
- Training data
- AI integration framework

**Dependencies:**
- Multiple foundational capabilities must exist first

---

## Capability Discovery Output

The output of Capability Discovery is a list of candidate capabilities with preliminary assessments.

| Candidate | Lifecycle State | Evidence Ready | Implementation Ready | User Value | Effort | Evidence Readiness | Arch. Impact | Source |
|-----------|:---------------:|:--------------:|:--------------------:|:----------:|:------:|:------------------:|:------------:|--------|
| **BOQ Intelligence** | Proposed | Yes | No | High | Low | High | None | Production evidence + user need |
| **Formatter** | Proposed | Partial | No | Medium | Low | Medium | None | User need |
| **CheckMate** | Proposed | Partial | No | High | Medium | Medium | None | User need |
| **Cubit parser** | Proposed | No | No | Medium | Medium | Low | None | Engineering backlog |
| **PDF parser** | Proposed | No | No | Low | High | Very Low | None | Engineering backlog |
| **AI-assisted estimation** | Proposed | No | No | High | High | Very Low | Potentially significant | User need |

---

## Next Step

Capability Discovery is complete. The next step is **Capability Evaluation**, where each candidate is evaluated against the four criteria and a ranked recommendation is produced for Project Owner Decision.

See `docs/planning/Capability_Evaluation_001.md` for the formal evaluation.

---

## Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-07-13 | Initial Capability Discovery. Six candidates identified. |