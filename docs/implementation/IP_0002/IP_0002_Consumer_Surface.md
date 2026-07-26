# IP-0002 - BOQ Consumer Contract Surface

**Status:** Complete
**Date:** 2026-07-25
**Authority:** EQ-0020
**Implementation Package:** IP-0002

---

## 1. Approved Import Paths

Consumers must only import from these 5 stable symbols:

| Symbol | Module | Type | Stability |
|--------|--------|------|-----------|
| analyze_boq | jarvis.parsers.costx.boq_intelligence | Function | HIGH |
| BOQIntelligenceResult | jarvis.parsers.costx.boq_intelligence | Frozen dataclass | HIGH |
| BOQHeaderNode | jarvis.parsers.costx.boq_intelligence | Frozen dataclass | HIGH |
| BOQRow | jarvis.parsers.costx.boq_extraction | Dataclass | HIGH |
| extract_boq | jarvis.parsers.costx.boq_extraction | Function | HIGH |

---

## 2. Unsupported Imports (Prohibited)

### Internal Functions
All _-prefixed functions in boq_intelligence.py (20 internal functions)

### Pre-Extraction Infrastructure
- jarvis.parsers.costx.WorkbookParser - workbook loading/validation
- jarvis.parsers.costx.loader - internal loading logic
- jarvis.parsers.costx.boq_extraction._classify_row - internal extraction helper

### Documented Finding
boq_extraction currently imports loader as a side effect. This is pre-extraction infrastructure coupling.

---

## 3. Consumer Obligations

### Must Do
1. Import only stable symbols from the approved list
2. Access fields defensively: Optional fields return None when flag is False
3. Use keyword arguments for analyze_boq flags
4. Treat results as immutable: Frozen dataclasses raise FrozenInstanceError on mutation

### Must NOT Do
1. Do not import _-prefixed symbols
2. Do not import WorkbookParser for evidence consumption
3. Do not import the loader module
4. Do not mutate result dataclasses

---

## 4. Extension Rules

### Adding New Evidence Fields
1. Add field to BOQIntelligenceResult with default None
2. Add corresponding flag to analyze_boq() with default False
3. Update contract document (v1.2+)
4. Update contract verification tests

### Adding New Internal Functions
1. Prefix with _
2. Do NOT export in __all__

### Removing Fields
- Never remove fields from a frozen contract version
- Deprecate by setting to None and documenting in next contract version

---

## 5. Test Coverage

Enforced by tests/parser/test_consumer_contract.py (31 tests):

| Test Class | Tests | Purpose |
|------------|-------|---------|
| TestStableImports | 7 | All 5 stable symbols importable and public |
| TestNoPrivateLeakage | 4 | No _-prefixed in __all__ or stable imports |
| TestWorkbookParserIsolation | 2 | Consumers do not need WorkbookParser |
| TestFrozenDataclassImmutability | 4 | Results frozen, mutation raises error |
| TestOptionalFieldBehavior | 4 | Fields return None when flags False |
| TestFieldExistence | 1 | All 19 contract fields exist |
| TestBackwardCompatibility | 4 | v1.0 consumers work with v1.1.0 |
| TestConsumerAccessPatterns | 2 | Recommended patterns work |
| TestNoInternalDependencyLeakage | 3 | No internal leakage |

---

## 6. Document Control

| Property | Value |
|----------|-------|
| Document ID | IP-0002-SURFACE |
| Implementation Package | IP-0002 |
| Status | Complete |
| Date | 2026-07-25 |
| Authority | EQ-0020 |
