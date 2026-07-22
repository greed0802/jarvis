# Appendix C: Domain Verification Matrix

> **Purpose**: Per-document verification status for every domain knowledge document in `docs/domain/`.
> **Generated**: 2026-07-15
> **Part of**: Jarvis Knowledge Consolidation

---

## Verification Classification

| Code | Meaning | Implication for Engineering Decisions |
|------|---------|--------------------------------------|
| `VP` | Verified by Project Owner | Safe to use as authoritative domain truth |
| `AGV` | AI-generated, subsequently verified by Project Owner | Safe to use; project owner has confirmed |
| `AG-EB` | AI-generated, backed by engineering evidence (EQ/spike confirmed) | Safe to use; evidence corroborates |
| `AG-PV` | AI-generated, partially verified — some sections confirmed, others not | Use confirmed sections only; flag unconfirmed |
| `AGP` | AI-generated, pending Project Owner verification | Requires Project Owner review before use in engineering decisions |
| `SP` | Speculative — domain assumptions not yet validated | Do not use for production implementation without verification |
| `UN` | Unknown authorship — cannot determine origin | Treat as AGP until provenance established |
| `OBS` | Obsolete — superseded by newer domain evidence | Do not use; refer to superseding document |
| `CONFLICT` | Contains statements that conflict with other verified documents | Flag for Project Owner resolution |

---

## Domain Document Verification Status

### Core/Index Documents

| Document | Lines | Verification | Notes |
|----------|-------|--------------|-------|
| `docs/domain/README.md` | ~50 | `AGP` | Index/overview. AI-generated structure. Content references domain docs 01-10 which have mixed verification. |
| `docs/domain/glossary.md` | ~100 | `AG-PV` | Terminology glossary. Some terms confirmed by EQ-0011 Spike 1 (Domain Vocabulary Discovery). Remaining terms need Project Owner confirmation. |

### Domain Knowledge Documents (01-10)

| # | Document | Lines | Verification | Key Content | Verification Notes |
|---|----------|-------|--------------|-------------|-------------------|
| 01 | `01_QS_Office_Standards.md` | ~200 | `AGP` | QS office standards and conventions | AI-generated. No EQ evidence directly validates office-specific conventions. **Needs Project Owner review.** |
| 02 | `02_BOQ_Structure.md` | ~300 | `AG-EB` | BOQ structure: rows, sections, hierarchy | **Frozen domain document.** Validated by EQ-0010 (structural intelligence) and EQ-0011 (semantic boundary). Row types, section headers, hierarchy patterns confirmed by production data. |
| 03 | `03_Trade_Schedule.md` | ~200 | `AGP` | Trade schedule definitions | AI-generated. Partially referenced by EQ-0011 for semantic classification. Trade names/schedule structure needs Project Owner confirmation. |
| 04 | `04_Omission_Addition.md` | ~200 | `AG-EB` | Omission/Addition sign conventions | Validated by EQ-0002 (sign convention) and EQ-0011. Sign conventions confirmed against production data. |
| 05 | `05_UOM_Standards.md` | ~200 | `AG-PV` | Unit of Measure standards | Partially validated by EQ-0010 Spike 2 (UOM Pattern Analysis). Common UOMs confirmed. Edge cases and non-standard UOMs need Project Owner review. |
| 06 | `06_Naming_Convention.md` | ~200 | `AGP` | Naming conventions for BOQ items | AI-generated. Naming patterns partially observed in production data but formal conventions not independently verifiable. **Needs Project Owner review.** |
| 07 | `07_Client_Conventions.md` | ~200 | `AGP` | Client-specific conventions | AI-generated. No production data available for multi-client validation. **Needs Project Owner review.** |
| 08 | `08_Checking_Workflow.md` | ~200 | `AGP` | BOQ checking/QA workflow | AI-generated. Describes human workflow process. Cannot be verified from production data alone. **Needs Project Owner review.** |
| 09 | `09_Dimension_Group_Guide.md` | ~200 | `AGP` | Dimension group guide | AI-generated. Domain-specific measurement grouping. No EQ evidence directly validates. **Needs Project Owner review.** |
| 10 | `10_Drawing_Organization.md` | ~200 | `AGP` | Drawing organization standards | AI-generated. Drawing management conventions. No EQ evidence available. **Needs Project Owner review.** |

### Review Document

| Document | Lines | Verification | Notes |
|----------|-------|--------------|-------|
| `DOMAIN_LAYER_V1_1_REVIEW.md` | ~300 | `EB` | Domain layer v1.1 review — reconciliation of AI-generated domain docs with EQ evidence. Evidence-backed review process. References specific EQ findings. |

---

## Verification Summary

| Status | Count | Documents |
|--------|-------|-----------|
| `AG-EB` (Evidence-backed) | 2 | 02_BOQ_Structure, 04_Omission_Addition |
| `AG-PV` (Partially verified) | 2 | glossary, 05_UOM_Standards |
| `AGP` (Pending verification) | 9 | README, 01, 03, 06, 07, 08, 09, 10 |
| `EB` (Evidence-backed review) | 1 | DOMAIN_LAYER_V1_1_REVIEW |

**Critical Finding**: 9 of 13 domain documents (69%) are AI-generated with **no Project Owner verification**. Only 2 documents (BOQ Structure, Omission/Addition) have been validated through engineering evidence (EQ-0010, EQ-0011).

---

## Domain Knowledge Verification by EQ Coverage

| EQ | Domain Docs Validated | Validation Type |
|----|----------------------|-----------------|
| EQ-0007 (Production Extraction) | 02_BOQ_Structure | Confirmed row types, field structure |
| EQ-0010 (Structural Intelligence) | 02_BOQ_Structure, 05_UOM_Standards | Confirmed structural properties, UOM patterns |
| EQ-0011 (Semantic Boundary) | 02_BOQ_Structure, 03_Trade_Schedule (partial), 04_Omission_Addition, glossary | Confirmed evidence/assessment boundary, sign conventions, vocabulary |
| EQ-0012 (Evidence Contract) | 02_BOQ_Structure (via contract fields) | Confirmed evidence fields trace to domain structure |

---

## Recommendations for Project Owner

1. **HIGH PRIORITY**: Review and verify domain docs that directly impact current capabilities:
   - `03_Trade_Schedule.md` — needed for BOQ semantic classification
   - `05_UOM_Standards.md` — needed for validation rule completeness
   - `06_Naming_Convention.md` — needed for description parsing

2. **MEDIUM PRIORITY**: Review domain docs needed for future capabilities:
   - `08_Checking_Workflow.md` — needed for QA capability
   - `09_Dimension_Group_Guide.md` — needed for measurement intelligence

3. **LOW PRIORITY**: Review office/client-specific docs:
   - `01_QS_Office_Standards.md`
   - `07_Client_Conventions.md`
   - `10_Drawing_Organization.md`

4. **PROCESS**: Consider instituting a "Domain Knowledge Freeze" process similar to the EQ Freeze process — where domain documents are formally verified and frozen before dependent capabilities are implemented.

---

## Flagged Statements Requiring Confirmation

The following domain statements appear in AI-generated documents and require Project Owner confirmation before use in engineering:

1. **Trade schedule classifications** (03_Trade_Schedule.md): Are the trade groupings and hierarchies accurate for the user's QS practice?
2. **Client-specific conventions** (07_Client_Conventions.md): Which clients have which conventions? Are these conventions stable?
3. **Checking workflow steps** (08_Checking_Workflow.md): Does the described workflow match actual practice?
4. **Dimension group categories** (09_Dimension_Group_Guide.md): Are these dimension groupings standard or office-specific?
5. **UOM edge cases** (05_UOM_Standards.md): Are there non-standard UOMs used that aren't captured?
6. **Drawing organization** (10_Drawing_Organization.md): Does the described organization match actual project drawing structures?

---

**Source Documents**:
- All 13 files under `docs/domain/`
- EQ-0010 evidence reports (Spikes 1-5)
- EQ-0011 evidence reports (Spikes 1-5)
- `docs/domain/DOMAIN_LAYER_V1_1_REVIEW.md`