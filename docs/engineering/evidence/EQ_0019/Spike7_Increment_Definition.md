# Spike 7 — Increment Definition

## EQ-0019 BOQ Semantic Intelligence Increment 1

### Purpose
Define the minimum production increment: included capabilities, deferred capabilities, required tests, required evidence, acceptance criteria, and freeze criteria.

---

## 1. Increment Name

**BOQ Intelligence Increment 4 — Semantic Intelligence**

### Naming Rationale
- Increment 1: Row classification + section stats + anomalies
- Increment 2: Hierarchy reconstruction (EQ-0010)
- Increment 3: Structural detection evidence (EQ-0011)
- **Increment 4: Semantic intelligence evidence (EQ-0019)** — this increment

---

## 2. Included Capabilities (8 Production Ready)

| ID | Capability | Priority | Spike 2 Classification |
|---|---|---|---|
| SEM-PROD-01 | Vocabulary extraction (term frequency) | P1 — High Value | Production Ready |
| SEM-PROD-02 | Head1 text categorization | P1 — High Value | Production Ready |
| SEM-PROD-04 | Administrative pattern detection | P2 — Quality Evidence | Production Ready |
| SEM-PROD-05 | Section code enumeration | P0 — Essential | Production Ready |
| SEM-PROD-06 | UOM distribution reporting | P1 — High Value | Production Ready |
| SEM-PROD-07 | Header level count distribution | P2 — Quality Evidence | Production Ready |
| SEM-PROD-09 | "Items Always Quantify" enforcement | P3 — Safety Net | Production Ready |
| SEM-PROD-12 | Head1 admin sub-template recognition | P2 — Quality Evidence | Production Ready |

---

## 3. Deferred Capabilities (Not in this Increment)

| ID | Capability | Reason | Possible Future Action |
|---|---|---|---|
| SEM-PROD-03 | Description tag extraction | Needs Additional Evidence — insufficient tag pattern analysis | New spike on tag pattern analysis |
| SEM-PROD-08 | Cross-trade pattern verification | Needs Additional Evidence — only 16/61 sections verified | Fixture expansion + pattern verification spike |
| SEM-PROD-10 | Items-per-section distribution | Needs Additional Evidence — no consumer request, YAGNI | Implement when consumer needs it |
| SEM-PROD-11 | Note frequency distribution by section | Consumer Feature — better implemented as part of CheckMate | Implement with CheckMate consumer design |

---

## 4. Contract Changes

| Aspect | Detail |
|---|---|
| **Version** | 1.0.0 → 1.1.0 (MINOR) |
| **Backward Compatible** | Yes — all existing fields and invariants preserved |
| **New Fields** | 9 new optional fields + 2 enhanced existing fields |
| **New Invariants** | 28 (4 per new capability) |
| **New Parameter** | `include_semantic: bool = False` on `analyze_boq()` |
| **Consumer Impact** | None — optional opt-in pattern |

---

## 5. Required Tests

### 5.1 Unit Tests (18 test cases)

| # | Test | Capability |
|---|---|---|
| 1 | Vocabulary extraction counts terms correctly | SEM-PROD-01 |
| 2 | Vocabulary handles empty descriptions | SEM-PROD-01 |
| 3 | Vocabulary respects max_terms limit | SEM-PROD-01 |
| 4 | Head1 categorization labels admin patterns correctly | SEM-PROD-02 |
| 5 | Head1 categorization labels trade entries correctly | SEM-PROD-02 |
| 6 | Admin pattern detection finds present patterns | SEM-PROD-04 |
| 7 | Admin pattern detection finds missing patterns | SEM-PROD-04 |
| 8 | Section enumeration preserves worksheet order | SEM-PROD-05 |
| 9 | Section enumeration includes code + name | SEM-PROD-05 |
| 10 | UOM distribution counts match expected | SEM-PROD-06 |
| 11 | UOM percentages sum to 100% | SEM-PROD-06 |
| 12 | Header distribution counts by level | SEM-PROD-07 |
| 13 | Header distribution consistency (sum = Head total) | SEM-PROD-07 |
| 14 | Header quantity invariant passes with clean data | SEM-PROD-09 |
| 15 | Header quantity invariant catches violations | SEM-PROD-09 |
| 16 | Admin template recognition detects standard pattern | SEM-PROD-12 |
| 17 | Admin template recognition handles missing entries | SEM-PROD-12 |
| 18 | `include_semantic=False` preserves backward compatibility | ALL |

### 5.2 Integration Tests

| # | Test | Capability |
|---|---|---|
| 19 | Production fixture: all semantic capabilities return expected values | ALL |
| 20 | Production fixture: existing capabilities unchanged when `include_semantic=False` | ALL (regression) |

---

## 6. Required Evidence

### 6.1 Evidence Must Demonstrate

| Evidence | Source |
|---|---|
| Every new function is pure (no side effects) | Spike 3 Rule Definition + code review |
| Every new function is deterministic (same input → same output) | Spike 3 Rule Definition + test verification |
| Every new function preserves Evidence/Assessment boundary | Spike 6 Architecture Verification |
| Every new field returns `None` when `include_semantic=False` | Spike 4 Contract Impact + Backward compat test |
| All existing tests pass without modification | Regression test run |
| All 18 new test cases pass | Test execution |
| Production fixture verification | Integration test against full_boq.xlsx |

### 6.2 Evidence NOT Required

- New fixture data (existing fixture sufficient)
- Performance benchmarks (expected <10ms total)
- Consumer implementation (CheckMate, Formatter — deferred)
- Domain knowledge validation (capabilities are observation-only)

---

## 7. Acceptance Criteria

The increment is accepted only if:

1. ✅ **All 18 new unit tests pass**
2. ✅ **All 2 integration tests pass**
3. ✅ **All existing regression tests pass** (no behavioral changes)
4. ✅ **`include_semantic=False` returns identical output to current implementation** (backward compatibility verified)
5. ✅ **All 9 new fields are `None` when `include_semantic=False`**
6. ✅ **All 9 new fields are populated when `include_semantic=True`**
7. ✅ **8 new Production Ready capabilities produce correct data against production fixture**
8. ✅ **No parser modifications**
9. ✅ **No runtime modifications**
10. ✅ **No architecture changes**
11. ✅ **Evidence/Assessment boundary preserved** — no capability crosses into assessment
12. ✅ **All new invariants documented and tested**

---

## 8. Freeze Criteria

The increment may be frozen (Gate 3 approval for Production) only when:

1. All acceptance criteria met (above)
2. Gate 1 — Mechanical Verification:
   - Test suite passes (20+ tests)
   - Determinism verified (repeatability demonstrated)
   - Contract invariants verified (28 new + 19 existing)
   - Documentation synchronized
   - Version consistent
3. Gate 2 — Architecture Verification:
   - Responsibility boundaries preserved
   - Hidden coupling assessed
   - Consumer independence verified
   - Determinism confirmed
   - YAGNI compliance verified
   - Evidence/Assessment boundary confirmed
4. Gate 3 — Consumer Readiness:
   - Stable public API (`analyze_boq` with new parameter)
   - Import stability (same module, same entry point)
   - Contract maturity assessed (MINOR version — stable)
   - Consumer documentation updated
   - Backward compatibility confirmed

---

## 9. Implementation Estimate

| Phase | Effort | Description |
|---|---|---|
| BOQIntelligenceResult extension | 15 min | Add 9 new fields to dataclass |
| 8 new functions | 2-3 hours | Pure functions with test coverage |
| `include_semantic` wiring | 30 min | Parameter + conditional logic |
| 20 tests | 2-3 hours | Unit + integration tests |
| Verification and documentation | 1 hour | Test suite + spike doc update |
| **Total** | **6-8 hours** | One developer day |

---

## 10. Capability Matrix Update

### New Capability Matrix Section

#### EQ-0019: 12 Semantic Capabilities (8 Production Ready + 4 Deferred)

| ID | Capability | EQ-0019 Classification |
|---|---|---|
| SEM-PROD-01 | Vocabulary extraction | **Implementation Ready** |
| SEM-PROD-02 | Head1 text categorization | **Implementation Ready** |
| SEM-PROD-03 | Description tag extraction | Needs Additional Evidence |
| SEM-PROD-04 | Admin pattern detection | **Implementation Ready** |
| SEM-PROD-05 | Section code enumeration | **Implementation Ready** |
| SEM-PROD-06 | UOM distribution reporting | **Implementation Ready** |
| SEM-PROD-07 | Header level count distribution | **Implementation Ready** |
| SEM-PROD-08 | Cross-trade pattern verification | Needs Additional Evidence |
| SEM-PROD-09 | "Items Always Quantify" enforcement | **Implementation Ready** |
| SEM-PROD-10 | Items-per-section distribution | Needs Additional Evidence |
| SEM-PROD-11 | Note frequency by section | Consumer Feature |
| SEM-PROD-12 | Admin sub-template recognition | **Implementation Ready** |

### Updated Capability Relationship Diagram

```
EQ-0018 (Semantic Investigation — COMPLETE)
    ↓
EQ-0019 (Semantic Promotion — THIS INCREMENT)
    ↓
8 Production Ready → BOQ Intelligence Increment 4 (Implementation)
4 Deferred → Future spikes/EQs
```

---

## 11. Risk Assessment for Increment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| New capabilities break existing consumers | Very Low | High | `include_semantic=False` default + backward compat tests |
| Terminology extraction produces unexpected results | Low | Medium | Terms split by whitespace — deterministic, no AI |
| Template pattern matching too strict | Low | Low | Patterns are exact match — can be extended via EQ |
| Consumer requests different format | Medium | Low | All outputs are standard Python types (dict, tuple) |

---

## 12. Final Recommendation

**Implement BOQ Intelligence Increment 4 as defined.**

The increment contains:
- 8 deterministic semantic capabilities
- All Production Ready (Spike 2)
- All with defined deterministic rules (Spike 3)
- All backward compatible (Spike 4)
- All with confirmed consumer value (Spike 5)
- All with documented architecture (Spike 6)
- All testable with existing fixtures

**Estimated effort: 6-8 hours (one developer day)**

---

## Document Control

**Version:** 1.0
**Spike:** 7 of 7
**EQ:** EQ-0019
**Status:** Complete
**Last Updated:** 2026-07-25
**Owner:** Project Owner