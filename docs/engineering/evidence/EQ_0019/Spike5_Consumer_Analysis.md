# Spike 5 — Consumer Analysis

## EQ-0019 BOQ Semantic Intelligence Increment 1

### Purpose
Evaluate value of each Production Ready capability for CheckMate, Formatter, Builder, Reporting, and future consumers. No consumer-specific implementation.

---

## 1. Consumer Profile

### 1.1 CheckMate (Planned — Primary Consumer)

**Role:** First consumer of BOQ Intelligence evidence
**Relationship:** Depends on BOQ Intelligence Evidence Contract v1.0
**Needs:** Deterministic evidence about BOQ structure, content, and quality
**Status:** Planned — not yet implemented

### 1.2 Formatter (Future Consumer)

**Role:** Output format adapter (Excel, PDF, HTML)
**Relationship:** Depends on BOQ Intelligence Evidence Contract
**Needs:** Structured data for output formatting
**Status:** Deferred

### 1.3 Builder (Future Consumer)

**Role:** Build/CI integration
**Relationship:** Depends on BOQ Intelligence + Validation Engine
**Needs:** Machine-readable evidence for automated checks
**Status:** Deferred

### 1.4 Reporting (Future Consumer)

**Role:** Summary reporting
**Relationship:** Depends on BOQ Intelligence + Validation Engine
**Needs:** Aggregated statistics for summary reports
**Status:** Deferred

---

## 2. Capability Value Assessment

### SEM-PROD-01: Vocabulary Extraction

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **High** | Vocabulary distribution helps reviewers identify dominant materials/trades. For example, "Concrete" (427), "Finish" (446), "Formwork" (300) immediately indicate a structural/finishes-heavy project. Provides quick project characterisation. |
| **Formatter** | Medium | Vocabulary can be included in report metadata |
| **Builder** | Low | Not directly useful for CI validation |
| **Reporting** | **High** | Key input for executive summaries — "Project has X concrete items, Y finishes items" |

**Consumer Value Category:** Evidence enrichment for human reviewers

---

### SEM-PROD-02: Head1 Text Categorization

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **High** | Separates administrative boilerplate from trade-specific work items. Reviewers can quickly see: "This section has [5 admin headers, 12 trade-specific headers]". |
| **Formatter** | Medium | Can render admin vs trade headers differently |
| **Builder** | Low | Not directly useful for CI validation |
| **Reporting** | **High** | Summary statistic: "X% of headers are administrative boilerplate" provides insight into BOQ template structure |

**Consumer Value Category:** Structural clarity for human consumers

---

### SEM-PROD-04: Administrative Pattern Detection

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **High** | Verifies whether standard administrative patterns (GENERALLY, REFERENCES, PRICES, GENERAL ITEMS, NOTES AND ASSUMPTIONS) are present. Missing patterns may indicate incomplete BOQ. |
| **Formatter** | Medium | Can structure output based on detected patterns |
| **Builder** | **High** | Can enforce pattern presence as validation rule |
| **Reporting** | Medium | Can report pattern completeness per section |

**Consumer Value Category:** Quality evidence for BOQ template completeness

---

### SEM-PROD-05: Section Code Enumeration

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **High** | Ordered section list (A → BI) is a fundamental navigation structure. "This BOQ has 61 sections covering structural, finishes, services, and external works." |
| **Formatter** | **High** | Primary structure for output organisation |
| **Builder** | **High** | Section enumeration is essential for item code prefix validation |
| **Reporting** | **High** | Core summary input — section count and coverage |

**Consumer Value Category:** Foundational structure evidence (already partially available via `section_statistics`)

---

### SEM-PROD-06: UOM Distribution Reporting

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **High** | UOM distribution reveals the nature of the project: m2 dominance (33.7%) suggests surface-measured trades. no-count (25.2%) suggests counted items. Provides immediate project characterisation. |
| **Formatter** | Medium | Can render UOM-specific quantities |
| **Builder** | Medium | Can validate UOM consistency |
| **Reporting** | **High** | Key summary statistic for report generation |

**Consumer Value Category:** Evidence enrichment for characterisation

---

### SEM-PROD-07: Header Level Count Distribution

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **High** | Head1 (294), Head2 (394), Head3 (627), Head4 (636) shows the hierarchy shape. Unusual distributions may indicate structural issues (e.g., too many Head1 entries relative to Head2 may mean missing hierarchy depth). |
| **Formatter** | Medium | Can display hierarchy depth statistics |
| **Builder** | Medium | Can flag unusual hierarchy distributions as warnings |
| **Reporting** | Medium | Summary statistic for hierarchy structure |

**Consumer Value Category:** Hierarchy shape evidence

---

### SEM-PROD-09: "Items Always Quantify" Enforcement

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **Medium** | Violation detection is valuable — header rows with quantities would be anomalous. However, production data shows 0 violations, so this is a safety net rather than active review tool. |
| **Formatter** | Low | Rare edge case handling |
| **Builder** | **High** | Enforceable invariant — build pipeline can fail if header rows carry quantities |
| **Reporting** | Low | Edge case reporting |

**Consumer Value Category:** Invariant enforcement (pipeline)

---

### SEM-PROD-12: Head1 Administrative Sub-Template Recognition

| Consumer | Value | Rationale |
|---|---|---|
| **CheckMate** | **High** | Identifies the standard sub-template pattern within trade sections. Missing or reordered templates may indicate data quality issues. |
| **Formatter** | Medium | Can highlight template structure in reports |
| **Builder** | **High** | Enforceable pattern — pipeline can verify template presence |
| **Reporting** | Medium | Pattern completeness reporting per section |

**Consumer Value Category:** Template completeness evidence

---

## 3. Value Matrix

| Capability | CheckMate | Formatter | Builder | Reporting | Overall |
|---|---|---|---|---|---|
| SEM-PROD-01 (Vocabulary) | **High** | Medium | Low | **High** | **High** |
| SEM-PROD-02 (Head1 Categorization) | **High** | Medium | Low | **High** | **High** |
| SEM-PROD-04 (Admin Patterns) | **High** | Medium | **High** | Medium | **High** |
| SEM-PROD-05 (Section Enumeration) | **High** | **High** | **High** | **High** | **High** |
| SEM-PROD-06 (UOM Distribution) | **High** | Medium | Medium | **High** | **High** |
| SEM-PROD-07 (Header Count Distribution) | **High** | Medium | Medium | Medium | **High** |
| SEM-PROD-09 (Items Always Quantify) | Medium | Low | **High** | Low | **Medium-High** |
| SEM-PROD-12 (Admin Template Recognition) | **High** | Medium | **High** | Medium | **High** |

---

## 4. Consumer Implementation Priority

| Priority | Capabilities | Rationale |
|---|---|---|
| **P0 — Essential** | SEM-PROD-05 (Section Enumeration) | Foundational structure — all consumers need this |
| **P1 — High Value** | SEM-PROD-01 (Vocabulary), SEM-PROD-02 (Categorization), SEM-PROD-06 (UOM Distribution) | Enrich human reviewers and reports |
| **P2 — Quality Evidence** | SEM-PROD-04 (Admin Patterns), SEM-PROD-07 (Header Count), SEM-PROD-12 (Template Recognition) | Quality checks for CheckMate + pipeline |
| **P3 — Safety Net** | SEM-PROD-09 (Items Always Quantify) | Rare but important invariant |

---

## 5. Consumer Independence Assessment

| Concern | Assessment |
|---|---|
| Do any capabilities leak consumer-specific assumptions? | No — all capabilities produce pure evidence without consumer context |
| Do any capabilities require consumer-specific configuration? | No — all capabilities operate over BOQRow only |
| Can consumers ignore new evidence fields? | Yes — optional + opt-in pattern ensures backward compatibility |
| Does CheckMate need to change its data model? | No — new fields are additive, not transformative |
| Can Formatter render new fields without changes? | Initially no — but this is consumer-specific implementation, not contract change |

**Conclusion:** All 8 Production Ready capabilities preserve consumer independence. No capability introduces consumer-specific coupling.

---

## 6. Key Recommendation

**Include all 8 Production Ready capabilities in the next BOQ Intelligence Increment.**

Rationale:
- All 8 have High or Medium-High consumer value across at least two consumer types
- All 8 preserve consumer independence
- All 8 are backward compatible (MINOR contract change)
- CheckMate benefits most (6 High-value capabilities)

The only question is implementation priority, which Spike 7 addresses.

---

## Document Control

**Version:** 1.0
**Spike:** 5 of 7
**EQ:** EQ-0019
**Status:** Complete
**Last Updated:** 2026-07-25
**Owner:** Project Owner