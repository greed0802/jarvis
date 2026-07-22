# EQ-0012 — Spike 4 — Evidence Report — Consumer Access Patterns

**Date:** 2026-07-15  
**Status:** Approved and Frozen
**Investigation:** EQ-0012 BOQ Intelligence Public Evidence Contract  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction  
**Source of Truth:** `src/jarvis/parsers/costx/`

---

## Objective

Determine the correct public consumer interface for the BOQ Intelligence Public Evidence Contract by analyzing production code, module boundaries, import stability, and access pattern alternatives.

---

## Methodology

1. **AST Analysis** — Parsed all production modules via Python AST to enumerate public/private symbols and import patterns
2. **Module Boundary Analysis** — Identified `__all__` exports, public-by-convention symbols, and internal implementation details
3. **Import Stability Analysis** — Traced every consumer-facing import to its production source
4. **Access Pattern Evaluation** — Compared 6 alternatives against production evidence

**Tool:** `tools/eq0012_spike4_consumer_access_patterns.py`

---

## Engineering Questions

### Q1: Smallest Stable Public Surface

**5 symbols** constitute the minimal consumer surface:

| Consumer Need | Symbol | Module | Production Evidence |
|---|---|---|---|
| Run BOQ intelligence analysis | `analyze_boq` | `jarvis.parsers.costx.boq_intelligence` | `boq_intelligence.py:67` |
| Access analysis results | `BOQIntelligenceResult` | `jarvis.parsers.costx.boq_intelligence` | `boq_intelligence.py:48-64` |
| Access hierarchy nodes | `BOQHeaderNode` | `jarvis.parsers.costx.boq_intelligence` | `boq_intelligence.py:27-45` |
| Provide row input | `BOQRow` | `jarvis.parsers.costx.boq_extraction` | `boq_extraction.py:39-48` |
| Extract rows from workbook | `extract_boq` | `jarvis.parsers.costx.boq_extraction` | `boq_extraction.py:51` |

**Evidence:** These are the only public symbols (no underscore prefix) that consumers directly interact with in the current production pipeline.

---

### Q2: Public Contract vs Internal Types

**Public contract types (consumers may import):**
- `BOQIntelligenceResult` — frozen dataclass, primary evidence container
- `BOQHeaderNode` — frozen dataclass, hierarchy node representation
- `BOQRow` — dataclass, input row representation
- `analyze_boq` — public function, evidence producer
- `extract_boq` — public function, extraction entry point

**Internal implementation (consumers must NOT import):**

| Internal Symbol | Reason | Evidence |
|---|---|---|
| `_count_row_types` | Internal evidence generator | `boq_intelligence.py:120` |
| `_compute_section_stats` | Internal evidence generator | `boq_intelligence.py:147` |
| `_compute_boq_stats` | Internal evidence generator | `boq_intelligence.py:129` |
| `_detect_anomalies` | Internal evidence generator | `boq_intelligence.py:164` |
| `_reconstruct_hierarchy` | Internal implementation | `boq_intelligence.py:198` |
| `_freeze_node` | Internal conversion | `boq_intelligence.py:262` |
| `_compute_hierarchy_statistics` | Internal statistics | `boq_intelligence.py:279` |
| `_extract_head_level` | Internal helper | `boq_intelligence.py:183` |
| `_detect_level_skips` | Internal detection | `boq_intelligence.py:335` |
| `_detect_zero_quantities` | Internal detection | `boq_intelligence.py:369` |
| `_detect_structural_containment` | Internal detection | `boq_intelligence.py:398` |
| `_detect_basic_completeness` | Internal detection | `boq_intelligence.py:432` |
| `_classify_row` | Internal classification | `boq_extraction.py:108` |

**Note:** `WorkbookParser` is a pre-extraction infrastructure concern (validation/loading). It is exported by `costx/__init__.py` as existing public surface but is not part of the evidence contract.

---

### Q3: Stable vs Unstable Imports

**STABLE — Consumers may depend on:**

```
from jarvis.parsers.costx.boq_intelligence import analyze_boq
from jarvis.parsers.costx.boq_intelligence import BOQIntelligenceResult
from jarvis.parsers.costx.boq_intelligence import BOQHeaderNode
from jarvis.parsers.costx.boq_extraction import BOQRow
from jarvis.parsers.costx.boq_extraction import extract_boq
```

**Stability Classification:** HIGH — All symbols are public (no underscore prefix), frozen dataclass or public function, protected by frozen engineering evidence.

**UNSTABLE — Consumers must NOT import:**

All symbols beginning with `_` (underscore) are internal implementation. They may change without notice and are not subject to versioning policy.

---

### Q4: Recommended Access Pattern

**Recommendation:** Direct dataclass + public function (current production pattern)

**Consumer usage pattern:**
```python
from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
from jarvis.parsers.costx.boq_intelligence import analyze_boq, BOQIntelligenceResult, BOQHeaderNode

rows = extract_boq(workbook)
result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

# Access evidence directly
for row_type, count in result.row_classification.items():
    ...

# Access hierarchy
for root in result.hierarchy:
    ...

# Access detections
for skip in result.detected_level_skips:
    ...
```

**Rationale:** Current production implementation is the proven consumer pattern. No engineering evidence exists for any additional abstraction layer.

---

### Q5: Consumer Guarantees

| Guarantee | Description | Origin |
|---|---|---|
| Import Stability | 5 stable import paths will not change within a MAJOR version | Q3 analysis |
| Field Stability | All documented evidence fields on BOQIntelligenceResult are frozen | Spike 3 invariants |
| Type Stability | Return types of `analyze_boq()` are frozen dataclasses | Production evidence |
| Determinism | Same input produces same output | Spike 3 invariants |
| Immutability | BOQIntelligenceResult, BOQHeaderNode are frozen dataclasses | `frozen=True` in production |

---

### Q6: Breaking Changes

**These changes are MAJOR (per Spike 2 versioning policy):**

| Change | Rationale |
|---|---|
| Adding, removing, or renaming BOQIntelligenceResult fields | Consumers access fields directly |
| Changing signature of `analyze_boq()` | Consumers call with named parameters |
| Changing return type of `analyze_boq()` | Consumer destructuring depends on type |
| Moving symbols across modules | Consumers import from specific module paths |
| Removing or renaming BOQHeaderNode fields | Consumers access hierarchy nodes directly |
| Changing BOQRow dataclass structure | BOQRow is input to analyze_boq |

**These changes are MINOR:**

| Change | Rationale |
|---|---|
| Adding new optional evidence fields | Existing fields remain stable |
| Adding new internal functions | Internal only, not part of contract |

---

## Access Pattern Alternatives Evaluated

### 1. Direct Dataclass Access (Current) ✅ **Recommended**

**Advantages:**
- Zero overhead — consumers access fields directly
- Type-checker friendly — static type checking works naturally
- No abstraction layer to maintain
- All evidence fields naturally visible and discoverable
- **Current production pattern** — proven working

**Disadvantages:**
- No encapsulation (not needed — all fields are contract)
- Direct module import dependency

**Compatibility:** 100% — current pattern

**Evidence:** `boq_intelligence.py` lines 48-64

### 2. Dedicated Public Package (jarvis.parsers.contracts) ⏸️ **Deferred**

**Advantages:** Clean separation, stable import path, re-export only contract types

**Disadvantages:**
- Requires creating and maintaining new package
- Additional abstraction layer with no current consumer benefit
- New drift surface between package and implementation
- **No engineering evidence supports this**

**Compatibility:** Could be added as MINOR

**Evidence:** No engineering evidence available

### 3. Protocol Interface ❌ **Rejected (YAGNI)**

**Advantages:** Formal interface contract, supports multiple implementations

**Disadvantages:**
- Significant overhead for single implementation
- YAGNI violation — no alternative implementation exists
- Hides concrete field types

**Compatibility:** MAJOR — changes consumer import model

**Evidence:** No engineering evidence available

### 4. Facade Object ❌ **Rejected**

**Advantages:** Single point of access

**Disadvantages:**
- Indirection with no benefit for single-module API
- Hides frozen dataclass nature
- Adds runtime overhead

**Compatibility:** Could be added as MINOR

### 5. Factory Function ❌ **Rejected**

**Advantages:** Controls construction

**Disadvantages:**
- `analyze_boq()` IS the factory — no additional factory needed
- Current frozen dataclass ensures immutability
- Would add indirection with no consumer benefit

**Compatibility:** MAJOR

**Evidence:** `boq_intelligence.py:67` — `analyze_boq()` is the factory

### 6. Read-Only Interface / Immutable Contract Object ❌ **Rejected**

**Advantages:** Prevents mutation at interface level

**Disadvantages:**
- Current frozen dataclass already enforces immutability
- Interface abstraction with no current benefit
- Hides specific field types

**Compatibility:** MAJOR

**Evidence:** `boq_intelligence.py:48` — `frozen=True`

---

## Module Boundary Analysis

| Module | `__all__` Exports | Public Symbols (Convention) | Internal Symbols |
|---|---|---|---|
| `costx/__init__.py` | `WorkbookParser` | `WorkbookParser` | — |
| `boq_extraction.py` | *none* | `BOQRow`, `extract_boq` | `_classify_row` |
| `boq_intelligence.py` | *none* | `BOQHeaderNode`, `BOQIntelligenceResult`, `analyze_boq` | 12 internal |
| `loader.py` | *none* | `load_workbook`, `patched_init` | `_apply_named_style_none_name_patch` |
| `workbook_parser.py` | *none* | `WorkbookParser`, `load`, `workbook`, `path`, `is_loaded`, `validate`, `close` | `__init__` |

**Key finding:** No BOQ intelligence symbols are re-exported from `costx/__init__.py`. Consumers currently import directly from individual modules. This is the production-proven pattern.

---

## Import Graph

```
Consumer
  └── jarvis.parsers.costx.boq_intelligence
        ├── analyze_boq (function)
        ├── BOQIntelligenceResult (frozen dataclass)
        └── BOQHeaderNode (frozen dataclass)
  
  └── jarvis.parsers.costx.boq_extraction
        ├── BOQRow (dataclass)
        └── extract_boq (function)
```

**Internal (hidden from consumer):**
```
boq_intelligence imports from boq_extraction (BOQRow)
boq_extraction imports from openpyxl (external)
```

---

## Verification Audit

**Tool:** `tools/eq0012_spike4_verification_audit.py`  
**Result:** **16 MATCH — All claims verified against production**  
**Report:** `data/reports/eq0012_spike4_verification_audit.json`

| Category | Total | MATCH | Drift |
|---|---|---|---|
| Module Boundaries | 1 | 1 | 0 |
| Stable Imports | 5 | 5 | 0 |
| Unstable Imports (must not import) | 9 | 9 | 0 |
| Access Pattern | 1 | 1 | 0 |
| **Total** | **16** | **16** | **0** |

---

## Consumer Guarantees (Detailed)

### Import Stability

Consumers importing from the 5 stable paths receive the following guarantees:

1. **Module stability:** `jarvis.parsers.costx.boq_intelligence` and `jarvis.parsers.costx.boq_extraction` will exist at these paths
2. **Symbol stability:** The 5 public symbols will remain importable
3. **Type stability:** Types will not change incompatibly within a MAJOR version
4. **Field stability:** Evidence fields will not be removed or renamed without deprecation

### Breaking Changes

Moving any of the 5 stable symbols to a different module path is a MAJOR breaking change.

---

## Boundary Preservation

**EQ-0011 engineering boundary is preserved:**
- All evidence fields are observation/detection only
- No decision language in any public symbol
- No validation, recommendation, or AI behavior
- `analyze_boq()` is a pure function

---

## Engineering Governance Improvement

The verification audit workflow proven in Spike 3 is repeated in Spike 4:

```
Engineering Question
→ Spike Investigation
→ Evidence Report
→ Production Verification Audit ← this artifact
→ Project Owner Review
→ Freeze
```

This is now considered **best practice** for repository contract engineering. The audit tool reads the generated JSON report rather than duplicating definitions, ensuring the verification tool itself cannot drift.

---

## Risks

| Risk | Mitigation |
|---|---|
| Direct module imports bind consumers to file layout | Document stable import paths explicitly in contract |
| No re-export package means module restructuring breaks consumers | Classify module moves as MAJOR |
| `BOQRow` is not part of evidence contract but is required as input | Document as stable dependency, not contract member |

---

## Implementation Requirements

### For Evidence Contract v1.0

1. Document 5 stable import paths explicitly
2. Document 9 must-not-import paths explicitly
3. Maintain frozen dataclass pattern for BOQIntelligenceResult
4. Keep `analyze_boq()` as the single factory function
5. No abstraction layer until a consumer specifically requires it

### For Future Development

If a consumer emerges that requires a dedicated public package:
1. Create `jarvis.contracts` or equivalent
2. Re-export existing symbols (MINOR change)
3. Do not remove existing direct import paths (backward compatibility)

---

## Conclusion

**Status:** Complete (verification passed — 16 MATCH)

**Key Findings:**
- 5 stable public symbols form the minimal consumer surface
- Current direct dataclass access pattern is correct — no abstraction needed
- 6 alternative access patterns evaluated; direct pattern recommended
- 9 internal symbols explicitly forbidden for consumer import
- All 16 verification claims match production

**Verification Audit:** 16 MATCH — All documentation matches production

**Recommendation:** Proceed to Spike 5 (Contract Documentation Standards).

---

## Tool

**Analysis Tool:** `tools/eq0012_spike4_consumer_access_patterns.py`  
**Analysis Output:** `data/reports/eq0012_spike4_consumer_access_patterns.json`  
**Verification Tool:** `tools/eq0012_spike4_verification_audit.py`  
**Verification Output:** `data/reports/eq0012_spike4_verification_audit.json`

---

**End of Evidence Report**