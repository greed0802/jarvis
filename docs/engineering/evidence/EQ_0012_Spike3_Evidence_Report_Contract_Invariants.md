# EQ-0012 — Spike 3 — Evidence Report — Contract Invariants

**Date:** 2026-07-15  
**Status:** Approved and Frozen  
**Investigation:** EQ-0012 BOQ Intelligence Public Evidence Contract  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction  
**Source of Truth:** `src/jarvis/parsers/costx/boq_intelligence.py` (lines 48-64)

---

## Objective

Document permanent invariants for all evidence fields in the BOQ Intelligence Public Evidence Contract.

This spike answers the questions:
1. **What structural invariants apply to each evidence field?**
2. **What semantic invariants apply to each evidence field?**
3. **How should invariant violations be detected?**
4. **How should invariant violations be handled?**

---

## Methodology

Systematic analysis distinguishing between:
- **Structural Invariants:** Shape, presence, type, ordering, immutability
- **Semantic Invariants:** Meaning, determinism, provenance, boundary, reproducibility

**Verification:** This report has been verified against production implementation (`src/jarvis/parsers/costx/boq_intelligence.py`). All documented types match production exactly.

Tool: `tools/eq0012_spike3_contract_invariants.py`

---

## Summary

**Evidence analyzed:** 10 fields (4 required, 6 optional)  
**Structural invariants documented:** 39  
**Semantic invariants documented:** 31  
**Total invariants:** 70

**Structural invariant categories:**
- Presence: 10
- Type: 10
- Immutability: 10
- Shape: 9

**Semantic invariant categories:**
- Determinism: 10
- Provenance: 10
- Boundary: 6
- Meaning: 4
- Reproducibility: 1

---

## Field Invariants

### Increment 1: Observation Evidence

#### 1. row_classification

**Type:** `dict[str, int]`  
**Required:** Yes  
**Production Line:** `boq_intelligence.py` line 55  
**Classification:** Observation

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-RC-01 | presence | Field must always exist and never be None | Assert field is not None | MAJOR - consumer code expects field |
| SI-RC-02 | type | Field must be dict[str, int] | Assert isinstance(field, dict) and all(isinstance(k, str) and isinstance(v, int) for k, v in field.items()) | MAJOR - type mismatch breaks consumers |
| SI-RC-03 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR - consumers depend on immutability |
| SI-RC-04 | shape | Keys are row type strings ('Head', 'Note', 'Section', 'Item', 'Other'), values are integer counts | Assert set(field.keys()) == {'Head', 'Note', 'Section', 'Item', 'Other'} | MAJOR - shape contract violated |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-RC-01 | determinism | Same worksheet produces same classifications | Run analysis twice, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-RC-02 | boundary | Classification is observation only - no decision language | Check row type keys against EQ-0011 forbidden terms | MAJOR - engineering boundary violation |
| SE-RC-03 | provenance | Classification traceable to Increment 1 engineering evidence | Assert classification logic matches EQ-0007 specification | MAJOR - untraceable evidence |
| SE-RC-04 | reproducibility | Classification reproducible from worksheet observation alone | Assert no external state dependencies | MAJOR - non-reproducible evidence |

**Cross-field dependencies:** section_statistics, boq_statistics

---

#### 2. section_statistics

**Type:** `dict[str, dict[str, int]]`  
**Required:** Yes  
**Production Line:** `boq_intelligence.py` line 56  
**Classification:** Observation

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-SS-01 | presence | Field must always exist and never be None | Assert field is not None | MAJOR - consumer code expects field |
| SI-SS-02 | type | Field must be dict[str, dict[str, int]] | Assert isinstance(field, dict) and all(isinstance(v, dict) for v in field.values()) | MAJOR - type mismatch breaks consumers |
| SI-SS-03 | shape | Outer dict: section name → section stats dict. Inner dict keys: 'negative_qty', 'positive_qty' → integer counts | For each section dict, assert set(section.keys()).issubset({'negative_qty', 'positive_qty'}) | MAJOR - shape contract violated |
| SI-SS-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-SS-01 | determinism | Same worksheet produces same section statistics | Run analysis twice, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-SS-02 | meaning | Section statistics represent structural observation only | Verify no decision semantics in keys or values | MAJOR - engineering boundary violation |
| SE-SS-03 | provenance | Statistics traceable to Increment 1 engineering evidence | Assert logic matches EQ-0007 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** row_classification, boq_statistics

---

#### 3. boq_statistics

**Type:** `dict[str, int | float]`  
**Required:** Yes  
**Production Line:** `boq_intelligence.py` line 57  
**Classification:** Observation

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-BS-01 | presence | Field must always exist and never be None | Assert field is not None | MAJOR - consumer code expects field |
| SI-BS-02 | type | Field must be dict[str, int \| float] | Assert isinstance(field, dict) and all(isinstance(v, (int, float)) for v in field.values()) | MAJOR - type mismatch breaks consumers |
| SI-BS-03 | shape | Required keys: 'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows' → int or float values | Assert set(field.keys()) == {'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows'} | MAJOR - shape contract violated |
| SI-BS-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-BS-01 | determinism | Same worksheet produces same BOQ statistics | Run analysis twice, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-BS-02 | meaning | BOQ statistics represent quantitative observation only | Verify no decision semantics in keys or values | MAJOR - engineering boundary violation |
| SE-BS-03 | provenance | Statistics traceable to Increment 1 engineering evidence | Assert logic matches EQ-0007 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** row_classification, section_statistics

---

#### 4. known_anomalies

**Type:** `list[dict[str, int | str | float]]`  
**Required:** Yes  
**Production Line:** `boq_intelligence.py` line 58  
**Classification:** Observation

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-KA-01 | presence | Field must always exist (may be empty list) | Assert field is not None | MAJOR - consumer code expects field |
| SI-KA-02 | type | Field must be list[dict[str, int \| str \| float]] | Assert isinstance(field, list) and all(isinstance(x, dict) for x in field) | MAJOR - type mismatch breaks consumers |
| SI-KA-03 | shape | Each anomaly dict contains keys: 'row_number' (int), 'code' (str), 'quantity' (float), 'section' (str) | For each anomaly, assert set(anomaly.keys()) == {'row_number', 'code', 'quantity', 'section'} | MAJOR - shape contract violated |
| SI-KA-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-KA-01 | determinism | Same worksheet produces same anomaly list | Run analysis twice, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-KA-02 | boundary | Anomalies describe observations only - no decision language | Check anomaly values against EQ-0011 forbidden terms | MAJOR - engineering boundary violation |
| SE-KA-03 | provenance | Anomalies traceable to Increment 1 engineering evidence | Assert logic matches EQ-0007 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** None

---

### Increment 2: Hierarchy Evidence

#### 5. hierarchy

**Type:** `tuple[BOQHeaderNode, ...] | None`  
**Required:** No (controlled by include_hierarchy parameter)  
**Production Line:** `boq_intelligence.py` line 59  
**Classification:** Hierarchy

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-H-01 | presence | Field may be None (controlled by include_hierarchy parameter) | Assert field is None or isinstance(field, tuple) | MINOR - optional field behavior |
| SI-H-02 | type | When present, must be tuple[BOQHeaderNode, ...] | If not None, assert isinstance(field, tuple) and all(isinstance(n, BOQHeaderNode) for n in field) | MAJOR - type mismatch breaks consumers |
| SI-H-03 | immutability | Evidence is immutable after creation (tuple + frozen BOQHeaderNode) | Dataclass frozen=True, tuple immutable, BOQHeaderNode frozen | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-H-01 | determinism | Same worksheet produces same hierarchy when include_hierarchy=True | Run analysis twice with same parameters, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-H-02 | meaning | Hierarchy represents structural relationships only | Verify no decision semantics in node attributes | MAJOR - engineering boundary violation |
| SE-H-03 | provenance | Hierarchy traceable to Increment 2 engineering evidence | Assert logic matches increment 2 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** hierarchy_statistics

---

#### 6. hierarchy_statistics

**Type:** `dict[str, int | float] | None`  
**Required:** No (controlled by include_hierarchy parameter)  
**Production Line:** `boq_intelligence.py` line 60  
**Classification:** Hierarchy

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-HS-01 | presence | Field may be None (controlled by include_hierarchy parameter) | Assert field is None or isinstance(field, dict) | MINOR - optional field behavior |
| SI-HS-02 | type | When present, must be dict[str, int \| float] | If not None, assert isinstance(field, dict) and all(isinstance(v, (int, float)) for v in field.values()) | MAJOR - type mismatch breaks consumers |
| SI-HS-03 | shape | Required keys: 'total_headers', 'root_headers', 'depth_distribution', 'items_per_header_by_uom' → int or float values | If not None, assert set(field.keys()) == {'total_headers', 'root_headers', 'depth_distribution', 'items_per_header_by_uom'} | MAJOR - shape contract violated |
| SI-HS-04 | immutability | Evidence is immutable after creation | Dataclass frozen=True | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-HS-01 | determinism | Same worksheet produces same hierarchy statistics when include_hierarchy=True | Run analysis twice with same parameters, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-HS-02 | meaning | Statistics represent quantitative hierarchy observation only | Verify no decision semantics in keys or values | MAJOR - engineering boundary violation |
| SE-HS-03 | provenance | Statistics traceable to Increment 2 engineering evidence | Assert logic matches increment 2 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** hierarchy

---

### Increment 3: Detection Evidence

#### 7. detected_level_skips

**Type:** `tuple[dict[str, int], ...] | None`  
**Required:** No (controlled by include_detection parameter)  
**Production Line:** `boq_intelligence.py` line 61  
**Classification:** Detection

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-DLS-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR - optional field behavior |
| SI-DLS-02 | type | When present, must be tuple[dict[str, int], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR - type mismatch breaks consumers |
| SI-DLS-03 | shape | Each skip dict contains keys: 'parent_row_number', 'parent_level', 'child_row_number', 'child_level', 'skip_magnitude' → int values | For each skip, verify all keys present and all values are int | MAJOR - shape contract violated |
| SI-DLS-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-DLS-01 | determinism | Same worksheet produces same level skips when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-DLS-02 | boundary | Detections describe patterns only - no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR - engineering boundary violation |
| SE-DLS-03 | provenance | Detections traceable to Increment 3 engineering evidence | Assert logic matches increment 3 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** hierarchy

---

#### 8. zero_quantity_items

**Type:** `tuple[dict[str, int | str | float | None], ...] | None`  
**Required:** No (controlled by include_detection parameter)  
**Production Line:** `boq_intelligence.py` line 62  
**Classification:** Detection

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-ZQI-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR - optional field behavior |
| SI-ZQI-02 | type | When present, must be tuple[dict[str, int \| str \| float \| None], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR - type mismatch breaks consumers |
| SI-ZQI-03 | shape | Each item dict contains keys: 'row_number', 'code', 'description', 'section', 'quantity', 'uom' | For each item, verify all keys present | MAJOR - shape contract violated |
| SI-ZQI-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-ZQI-01 | determinism | Same worksheet produces same zero quantity items when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-ZQI-02 | boundary | Detections describe patterns only - no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR - engineering boundary violation |
| SE-ZQI-03 | provenance | Detections traceable to Increment 3 engineering evidence | Assert logic matches increment 3 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** row_classification

---

#### 9. structural_containment_findings

**Type:** `tuple[dict[str, int], ...] | None`  
**Required:** No (controlled by include_detection parameter)  
**Production Line:** `boq_intelligence.py` line 63  
**Classification:** Detection

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-SCF-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR - optional field behavior |
| SI-SCF-02 | type | When present, must be tuple[dict[str, int], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR - type mismatch breaks consumers |
| SI-SCF-03 | shape | Each finding dict contains keys: 'parent_row_number', 'parent_level', 'child_row_number', 'child_level' → int values | For each finding, verify all keys present and all values are int | MAJOR - shape contract violated |
| SI-SCF-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-SCF-01 | determinism | Same worksheet produces same structural findings when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-SCF-02 | boundary | Findings describe patterns only - no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR - engineering boundary violation |
| SE-SCF-03 | provenance | Findings traceable to Increment 3 engineering evidence | Assert logic matches increment 3 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** hierarchy, row_classification

---

#### 10. completeness_findings

**Type:** `tuple[dict[str, int | str], ...] | None`  
**Required:** No (controlled by include_detection parameter)  
**Production Line:** `boq_intelligence.py` line 64  
**Classification:** Detection

**Structural Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SI-CF-01 | presence | Field may be None (controlled by include_detection parameter) | Assert field is None or isinstance(field, tuple) | MINOR - optional field behavior |
| SI-CF-02 | type | When present, must be tuple[dict[str, int \| str], ...] | If not None, assert isinstance(field, tuple) and all(isinstance(x, dict) for x in field) | MAJOR - type mismatch breaks consumers |
| SI-CF-03 | shape | Each finding dict contains keys: 'section' (str), 'item_count' (int) | For each finding, assert set(finding.keys()) == {'section', 'item_count'} | MAJOR - shape contract violated |
| SI-CF-04 | immutability | Evidence is immutable after creation (tuple immutability) | Dataclass frozen=True, tuple immutable | MAJOR - consumers depend on immutability |

**Semantic Invariants:**

| ID | Category | Description | Verification | Violation Impact |
|----|----------|-------------|--------------|------------------|
| SE-CF-01 | determinism | Same worksheet produces same completeness findings when include_detection=True | Run analysis twice with same parameters, compare results | MAJOR - non-determinism breaks consumer trust |
| SE-CF-02 | boundary | Findings describe patterns only - no decision language | Check field keys/values against EQ-0011 forbidden terms | MAJOR - engineering boundary violation |
| SE-CF-03 | provenance | Findings traceable to Increment 3 engineering evidence | Assert logic matches increment 3 specification | MAJOR - untraceable evidence |

**Cross-field dependencies:** row_classification, section_statistics

---

## Verification Approach

### Verification Strategy

**Structural Verification:**
- **Approach:** Static type checking + runtime assertions
- **Tools:** mypy, pytest assertions, dataclass validation
- **Frequency:** Every test run
- **Scope:** All fields, all tests

**Semantic Verification:**
- **Approach:** Determinism tests + boundary tests + provenance tests
- **Tools:** pytest, frozen engineering evidence, EQ-0011 term checker
- **Frequency:** Every test run + regression suite
- **Scope:** All fields, comprehensive test matrix

### Verification Phases

**Phase 1 — Development:**
- Type checker (mypy) on every file save
- Unit tests on every commit
- Determinism tests in CI pipeline

**Phase 2 — Integration:**
- Full test suite execution
- Historical fixture regression tests
- Cross-field dependency validation

**Phase 3 — Release:**
- Complete evidence inventory validation
- Provenance traceability check
- Boundary compliance audit

---

## Violation Handling

### Detection and Handling

**Structural Violations:**
- **Detection:** Immediate - fail fast at analysis time
- **Handling:** Raise InvariantViolationError with diagnostic details
- **Recovery:** None - structural violations are fatal
- **Consumer Impact:** Analysis fails, no evidence produced

**Semantic Violations:**
- **Detection:** Test-time detection via assertions
- **Handling:** Raise InvariantViolationError with evidence trace
- **Recovery:** None - semantic violations indicate implementation defect
- **Consumer Impact:** No impact (caught in testing before release)

### Error Reporting

**Required diagnostic details:**
1. Invariant ID violated
2. Field name
3. Expected behavior
4. Actual behavior
5. Input that triggered violation
6. Engineering evidence reference

**Format:** Structured error with full diagnostic context  
**Logging:** Error logged with full trace for debugging

### Governance on Violation Discovery

**When an invariant violation is discovered:**

1. Create Engineering Question to investigate
2. Classify as defect or specification gap
3. **If defect:** Fix implementation
4. **If specification gap:** Update engineering evidence and contract
5. Add regression test
6. Update contract documentation if needed

**Version Impact:**
- **Structural fix:** PATCH if no behavior change, MAJOR if behavior change
- **Semantic fix:** PATCH if clarification, MAJOR if meaning change

---

## Key Findings

### Universal Invariants

**All fields share these invariants:**
1. **Immutability** (SI-*-03): Evidence is immutable after creation
2. **Determinism** (SE-*-01): Same input produces same output
3. **Provenance** (SE-*-03): Traceable to frozen engineering evidence

### Required vs. Optional Distinction

**Required fields (4):**
- Always present (never None)
- Presence violations are MAJOR

**Optional fields (6):**
- May be None (controlled by parameters: `include_hierarchy`, `include_detection`)
- Presence of None is valid, not a violation

### Tuple Immutability

Production implementation uses tuples for hierarchy and all detection evidence. This enforces immutability at the type level:
- `tuple[BOQHeaderNode, ...]` — Frozen dataclass within immutable tuple
- `tuple[dict[str, ...], ...]` — Immutable sequence of dictionaries
- Consistent with Spike 2 versioning policy (tuples are frozen structures)

### Boundary Preservation

**6 fields explicitly preserve engineering boundary:**
- row_classification (observation)
- known_anomalies (observation)
- detected_level_skips (detection)
- zero_quantity_items (detection)
- structural_containment_findings (detection)
- completeness_findings (detection)

**Verification:** EQ-0011 forbidden term checker

### Cross-field Dependencies

**9 of 10 fields have dependencies:**
- Required fields depend on each other (observation triangle)
- Optional fields depend on required fields
- Detection fields depend on observation and/or hierarchy

**Implication:** Consumers must understand dependency graph

---

## Contract Implications

### Invariant-Driven Verification

The contract will specify:
1. **How to verify** each invariant (per verification column)
2. **When to verify** (per verification phases)
3. **What to do on violation** (per violation handling policy)

### Consumer Guarantees

From Spike 2, consumers have 16 guarantees. This spike adds:
- **G-17:** All invariants documented here are permanent
- **G-18:** Invariant violations will fail fast with diagnostic details
- **G-19:** New invariants can only be added via MAJOR version

### Implementation Requirements

For v1.0 contract:
1. BOQIntelligenceResult must be frozen dataclass — ✅ verified
2. All required fields must be non-optional in type signature — ✅ verified
3. All optional fields must be Optional[T] in type signature — ✅ verified
4. Analysis functions must be pure (no external state) — ✅ verified
5. Test suite must verify all 70 invariants — recommended

---

## Verification Audit Log

This report has been verified against production implementation.

**Verification Tool:** `tools/eq0012_spike3_verification_audit.py`  
**Production Source:** `src/jarvis/parsers/costx/boq_intelligence.py` (lines 48-64)  
**Result:** 10 MATCH, 0 DOCUMENTATION_DRIFT, 0 IMPLEMENTATION_DRIFT  
**Class A (Documentation Error):** 0  
**Class B (Implementation Error):** 0

**Verification Report:** `data/reports/eq0012_spike3_verification_audit.json`

---

## Next Steps

1. **Spike 4:** Consumer Access Patterns
   - Design consumer import model
   - Design internal detail hiding strategy
   - Define public API surface

2. **Spike 5:** Contract Documentation Standards
   - Define evidence field documentation requirements
   - Design semantics specification format
   - Define invariant documentation format

3. **Spike 6:** Evidence Contract v1.0 Specification
   - Synthesize all findings
   - Author Public Evidence Contract v1.0
   - Integrate all spikes into unified contract

---

## Conclusion

**Status:** Approved and Frozen

**Key Findings:**
- 70 total invariants documented (39 structural, 31 semantic)
- All field types verified against production implementation
- Universal invariants: immutability, determinism, provenance
- 6 fields explicitly preserve EQ-0011 engineering boundary
- All invariants are MAJOR version-locked
- Verification approach defined (3 phases, 2 strategies)
- Violation handling policy defined (fail-fast, diagnostic reporting)

**Verification Audit:** 10 MATCH — All documentation matches production

**Recommendation:** Proceed to Spike 4 (Consumer Access Patterns).

---

## Tool

**Spike Implementation:** `tools/eq0012_spike3_contract_invariants.py`  
**Analysis Output:** `data/reports/eq0012_spike3_contract_invariants.json`  
**Verification Tool:** `tools/eq0012_spike3_verification_audit.py`  
**Verification Output:** `data/reports/eq0012_spike3_verification_audit.json`

---

**End of Evidence Report**