# EQ-0012 — Spike 1 — Evidence Report — Current Evidence Inventory

**Date:** 2026-07-15  
**Status:** Complete  
**Investigation:** EQ-0012 BOQ Intelligence Public Evidence Contract  
**Governance:** Engineering_Governance.md v1.0  
**Principle:** Evidence Before Abstraction

---

## Objective

Systematically inventory all evidence fields produced by BOQ Intelligence (Increments 1-3), documenting their types, semantics, traceability to engineering evidence, and stability classification.

---

## Methodology

Analyzed `src/jarvis/parsers/costx/boq_intelligence.py` to enumerate:
1. All fields in `BOQIntelligenceResult` dataclass
2. Type annotations for each field
3. Required vs. optional (opt-in) fields
4. Semantic meaning from implementation and docstrings
5. Traceability to frozen EQ evidence reports
6. Stability classification

Tool: `tools/eq0012_spike1_current_evidence_inventory.py`

---

## Findings

### Evidence Field Count

**Total:** 10 evidence fields across 3 increments

**By Increment:**
- Increment 1 (Observation Evidence): 4 fields
- Increment 2 (Hierarchy Evidence): 2 fields
- Increment 3 (Detection Evidence): 4 fields

**By Required Status:**
- Required (always present): 4 fields (all Increment 1)
- Optional (opt-in): 6 fields (Increments 2-3)

### Increment 1: Observation Evidence (Required)

#### Field: row_classification
- **Type:** `dict[str, int]`
- **Semantics:** Count of rows by type (Head, Note, Section, Item, Other)
- **Traceability:** EQ-0007, EQ-0009. Row types defined in boq_extraction.py
- **Structure:** Fixed keys: `{'Head', 'Note', 'Section', 'Item', 'Other'}`
- **Invariants:** 
  - All keys present
  - Values are non-negative integers
  - Sum of values equals total row count
- **Stability:** Stable

#### Field: section_statistics
- **Type:** `dict[str, dict[str, int]]`
- **Semantics:** Per-section quantity distribution
- **Traceability:** EQ-0009 Context Discovery Report
- **Structure:** 
  - Outer key: section name (string)
  - Inner keys: `{'negative_qty', 'positive_qty'}`
- **Invariants:**
  - Sorted by section name
  - Only sections with quantities included
  - Inner dict always has both keys
  - Values are non-negative integers
- **Stability:** Stable

#### Field: boq_statistics
- **Type:** `dict[str, int | float]`
- **Semantics:** BOQ-wide field presence statistics
- **Traceability:** EQ-0007 Production Extraction Report
- **Structure:** Fixed keys: `{'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows'}`
- **Invariants:**
  - All keys present
  - All values are non-negative integers
  - Each count ≤ total_rows
- **Stability:** Stable

#### Field: known_anomalies
- **Type:** `list[dict[str, int | str | float]]`
- **Semantics:** Identity-level anomalies detected through deterministic rules
- **Traceability:** EQ-0009 Context Discovery Report (Omission/Addition domain rules)
- **Structure:** Each dict: `{'row_number': int, 'code': str | None, 'quantity': float, 'section': str}`
- **Current Rule:** OMISSION section items with positive quantity
- **Invariants:**
  - Sorted by row_number
  - All dicts have same keys
  - row_number is unique
- **Stability:** Stable

### Increment 2: Hierarchy Evidence (Optional)

#### Field: hierarchy
- **Type:** `tuple[BOQHeaderNode, ...] | None`
- **Semantics:** Reconstructed BOQ heading tree (root headers with recursive children)
- **Traceability:** EQ-0010 Spike 4 (stack-based hierarchy reconstruction algorithm)
- **Structure:** `BOQHeaderNode` frozen dataclass with fields:
  - `level: int` (1-5)
  - `row_number: int`
  - `uom: str`
  - `description: str | None`
  - `section: str | None`
  - `depth: int`
  - `parent_row_number: int | None`
  - `children_headers: tuple[BOQHeaderNode, ...]`
  - `children_items: tuple[dict, ...]`
- **Invariants:**
  - None if `include_hierarchy=False`
  - Tuple contains only root-level headers (Head1 nodes)
  - Tree structure reflects Head1-5 nesting
  - No cycles in parent-child relationships
- **Stability:** Stable

#### Field: hierarchy_statistics
- **Type:** `dict[str, int | float] | None`
- **Semantics:** Statistics derived from reconstructed hierarchy
- **Traceability:** EQ-0010 Spike 4 (hierarchy reconstruction statistics)
- **Structure:** Fixed keys: `{'total_headers', 'root_headers', 'depth_distribution', 'items_per_header_by_uom'}`
- **Invariants:**
  - None if `include_hierarchy=False`
  - All keys present when not None
  - `depth_distribution` is dict[int, int] (depth → count)
  - `items_per_header_by_uom` is dict[str, float] (UOM → average items)
  - All counts are non-negative
- **Stability:** Stable

### Increment 3: Detection Evidence (Optional)

#### Field: detected_level_skips
- **Type:** `tuple[dict[str, int], ...] | None`
- **Semantics:** Level progression skips (e.g., Head1→Head3)
- **Traceability:** EQ-0010 Spike 3, EQ-0011 Spike 2 (detection only, not legitimacy assessment)
- **Structure:** Each dict: `{'parent_row': int, 'child_row': int, 'parent_level': int, 'child_level': int, 'skip': int}`
- **Invariants:**
  - None if `include_detection=False` or `hierarchy=None`
  - `skip = child_level - parent_level > 1`
  - No assessment of legitimacy
- **Stability:** Stable

#### Field: zero_quantity_items
- **Type:** `tuple[dict[str, int | str | float | None], ...] | None`
- **Semantics:** Items with quantity exactly 0.0
- **Traceability:** EQ-0010 Spike 1, EQ-0011 Spike 2 (detection only, not acceptability assessment)
- **Structure:** Each dict: `{'row_number': int, 'code': str | None, 'description': str | None, 'quantity': float, 'uom': str | None, 'section': str | None}`
- **Invariants:**
  - None if `include_detection=False`
  - quantity == 0.0 exactly
  - No assessment of acceptability
- **Stability:** Stable

#### Field: structural_containment_findings
- **Type:** `tuple[dict[str, int], ...] | None`
- **Semantics:** Structural parent-child level consistency violations
- **Traceability:** EQ-0010 Spike 4, EQ-0011 Spike 3 (structural only, not semantic)
- **Structure:** Each dict: `{'parent_row': int, 'child_row': int, 'parent_level': int, 'child_level': int}`
- **Invariants:**
  - None if `include_detection=False` or `hierarchy=None`
  - Reports cases where child_level > parent_level (structural inversion)
  - Structural containment only (not semantic scope)
- **Stability:** Stable

#### Field: completeness_findings
- **Type:** `tuple[dict[str, int | str], ...] | None`
- **Semantics:** Sections lacking measurable items
- **Traceability:** EQ-0010 Spike 3, EQ-0011 Spike 3 (basic structural, not project scope)
- **Structure:** Each dict: `{'section': str, 'total_rows': int, 'item_count': int}`
- **Invariants:**
  - None if `include_detection=False`
  - `item_count` is count of rows with non-None quantity
  - No assessment of whether absence is acceptable
- **Stability:** Stable

---

## Stability Analysis

### Stability Classification

**All 10 fields classified as Stable.**

**Rationale:**
1. All fields trace to frozen engineering evidence (EQ-0007, EQ-0009, EQ-0010, EQ-0011)
2. All fields implement approved capabilities through formal gate approval
3. All fields have passed production validation (66 tests, 100% pass rate)
4. No speculative or experimental fields exist
5. No known defects or design issues

### Required vs. Optional Fields

**Required Fields (4):** Increment 1 observation evidence
- Always present in `BOQIntelligenceResult`
- No opt-in parameter required
- Consumers can depend unconditionally

**Optional Fields (6):** Increments 2-3 hierarchy and detection evidence
- Present only when requested via parameters
- `include_hierarchy=True` → hierarchy, hierarchy_statistics
- `include_detection=True` → detected_level_skips, zero_quantity_items, structural_containment_findings, completeness_findings
- Consumers must check for None before use

**Input to Spike 2:** The Required vs. Optional distinction must inform the versioning policy. Required fields carry stricter stability guarantees and should only change via major version bumps. Optional fields provide more flexibility — new optional fields are non-breaking additions. Versioning policy must differentiate between changes to required vs. optional fields.

### Traceability Map

All fields trace to frozen engineering evidence:

**EQ-0007 Production Extraction Report:**
- boq_statistics

**EQ-0009 Context Discovery Report:**
- row_classification (with EQ-0007)
- section_statistics
- known_anomalies

**EQ-0010 Deterministic BOQ Structural Intelligence:**
- Spike 1: zero_quantity_items
- Spike 3: detected_level_skips, completeness_findings
- Spike 4: hierarchy, hierarchy_statistics, structural_containment_findings

**EQ-0011 BOQ Semantic Intelligence Boundary:**
- Spike 2: Detection vs. Decision separation (applied to all Increment 3 fields)
- Spike 3: Boundary validation (structural only, not semantic)

---

## Contract Implications

### Version Baseline

**Recommendation:** **Candidate v1.0 baseline**

**Justification:**
- All fields are production-validated
- All fields trace to frozen evidence
- High stability confidence
- No experimental features
- Ready for consumer dependence

**Final Version Decision:** To be determined upon completion of EQ-0012 (all spikes). Spike 2 will establish formal versioning policy.

### Breaking vs. Non-Breaking Changes

**Breaking Changes (require major version bump):**
- Removing a field
- Changing a field type
- Changing invariants consumers depend on
- Renaming a field

**Non-Breaking Changes (minor/patch version bump):**
- Adding new optional fields
- Adding new dict keys to existing structures (if consumers iterate dynamically)
- Extending tuple contents (if consumers use indexing, this is breaking)

**Key Insight:** Most evidence uses flexible structures (dicts, tuples) which allow extension. However, consumers may have expectations about structure stability.

### Field Stability Guarantee

**Proposal for Evidence Contract:**
- All 10 current fields are **frozen** in v1.0
- Types will not change
- Invariants will not change
- Semantics will not change
- Optional fields will remain optional
- Required fields will remain required

**Future Extension:**
- New evidence fields may be added as optional
- New fields require new Engineering Question investigation
- Breaking changes require formal deprecation period

---

## Observations

### Engineering Boundary Preservation

All Increment 3 detection fields correctly observe EQ-0011 engineering boundary:
- Field names describe observations, not assessments
- No "violation", "error", "invalid" terminology
- No severity scoring
- No recommendations
- Pure structural evidence only

**Example:** `detected_level_skips` (observation) not `level_skip_violations` (assessment)

### Deterministic Evidence

All evidence is deterministic:
- Pure functions with no side effects
- Frozen dataclasses (immutable results)
- No timestamps (observation, not temporal)
- Sorted outputs where order matters
- No randomness or heuristics

### Consumer Independence

Evidence structure does not expose implementation details:
- No internal function names
- No algorithm specifics
- No performance characteristics
- Only observable facts

---

## Next Steps

1. **Spike 2:** Contract Structure & Versioning Policy
   - Define versioning scheme (semantic versioning recommended)
   - Define breaking vs. non-breaking change criteria
   - Define deprecation policy
   - Define backward compatibility guarantees

2. **Spike 3:** Contract Invariants
   - Document invariants for each evidence field
   - Define invariant verification approach
   - Define invariant violation handling

3. **Spike 4:** Consumer Access Patterns
   - Design consumer import model
   - Design internal detail hiding strategy
   - Evaluate evidence module separation

4. **Spike 5:** Contract Documentation Standards
   - Define evidence field documentation requirements
   - Design semantics specification format

5. **Spike 6:** Evidence Contract v1.0 Specification
   - Synthesize all findings
   - Author Public Evidence Contract v1.0

---

## Conclusion

**Status:** Spike 1 Complete

**Key Finding:** All 10 evidence fields are stable, production-validated, and traceable to frozen engineering evidence. High confidence for candidate v1.0 baseline.

**Recommendation:** Proceed to Spike 2 (Contract Structure & Versioning Policy). Spike 2 will establish formal versioning policy and determine final contract version number.

---

## Tool

**Spike Implementation:** `tools/eq0012_spike1_current_evidence_inventory.py`  
**Results:** `data/reports/eq0012_spike1_evidence_inventory.json`

---

**End of Evidence Report**