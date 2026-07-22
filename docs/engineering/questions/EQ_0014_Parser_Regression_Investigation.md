# EQ-0014: Parser Regression Investigation

**Status:** Spike 1 Active  
**Date:** 2026-07-16  
**Authority:** Project Owner directive (Repository Hardening Sprint close)  
**Reference:** EQ-0013 Final Freeze Report (identified 20 parser test failures outside scope)

---

## Purpose

Investigate 20 failing parser tests in `tests/parser/test_boq_intelligence_increment3.py` to determine root cause and recommended disposition before M8 consumer expansion.

---

## Motivation

The Repository Hardening Sprint identified 20 failing parser regression tests outside the Validation Engine scope. These failures must be classified before proceeding to M8 consumer architecture work.

Project Owner directive: "Evidence first. No implementation assumptions. No fixes until evidence exists."

---

## Scope

- All 20 failing tests in `tests/parser/test_boq_intelligence_increment3.py`
- All 103 tests in `tests/parser/` (75 passing, 20 failing, 8 skipped)
- Production implementation: `src/jarvis/parsers/costx/boq_intelligence.py`, `boq_extraction.py`
- Frozen engineering evidence: EQ-0010, EQ-0011, EQ-0012

**Out of scope:**
- Modifying production code (unless evidence supports it)
- Fixing tests (until Project Owner approves disposition)
- M8 consumer architecture work

---

## Spike Plan

### Spike 1: Failure Classification

For every failing parser test, identify:
- Failing assertion
- Implementation path
- Original engineering intent
- Expected behavior vs current behavior
- Root cause classification

Classify every failure:
- Implementation Bug — Code does not match design intent
- Regression — Was passing, now broken by implementation change
- Outdated Test — Test uses data/fixtures production no longer produces
- Intentional Change — Intentional change not reflected in tests
- Specification Drift — Test asserts behavior different from frozen evidence
- Unknown — Cannot classify without further investigation

Produce:
- Parser Regression Matrix
- Failure Classification Matrix
- Root Cause Report
- Recommended disposition

---

## Success Criteria

- [x] Every failing parser test classified (20/20)
- [x] Every failure has evidence (production code references)
- [x] Every failure has recommended disposition
- [x] No failure remains unexplained
- [ ] Project Owner approves disposition
- [ ] Disposition executed (if authorized)

---

## Evidence References

- `tests/parser/test_boq_intelligence_increment3.py` — 20 failing tests
- `src/jarvis/parsers/costx/boq_intelligence.py` — Production: `_VALID_ROW_TYPES`, `_count_row_types`
- `src/jarvis/parsers/costx/boq_extraction.py` — Production: `BOQRow`, `_classify_row`, `_ITEM_UOMS`
- `docs/engineering/evidence/EQ_0010_Spike5_Evidence_Report_Domain_Reconciliation.md`
- `docs/engineering/evidence/EQ_0011_Spike5_Evidence_Report_Semantic_Capability_Disposition.md`
- `docs/implementation/BOQ_Intelligence_Increment_3_Implementation_Design.md`

---

## Engineering Debt Register Entry

| ID | Finding | Severity | Blocks | Status |
|----|---------|----------|--------|--------|
| EQ-0014-01 | 20 parser tests fail due to BOQRow field-ordering bug in test construction | High | Yes (Gate 1) | Classified |