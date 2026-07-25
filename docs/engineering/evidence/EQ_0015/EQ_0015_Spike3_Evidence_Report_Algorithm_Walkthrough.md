# EQ-0015 Spike 3 Evidence Report — Algorithm Walkthrough

**EQ:** EQ-0015 (Structural Containment Investigation)
**Spike:** 3 — Algorithm Walkthrough
**Date:** 2026-07-16
**Status:** Complete

---

## Purpose

Demonstrate `_detect_structural_containment()` recursive traversal step-by-step with stack state diagrams for a Head1 → Head2 → Head3 hierarchy. Show precisely why `child.level > node.level` fires for every normal parent-child pair and cannot detect inversions (`child_level <= parent_level`).

---

## Method

1. **Stack Algorithm Recap:** Re-emphasize the structural guarantee of `_reconstruct_hierarchy()` (specifically line 245) that `child.level > parent.level` always holds for parent-child relationships.
2. **Hierarchy Tree:** Present the structure of the test hierarchy.
3. **Step-by-Step Traversal:** Walk through `_detect_structural_containment()`'s recursive `traverse` function, showing:
    - Current `node` and `child`
    - The `child.level > node.level` comparison result
    - When a finding is recorded
4. **Inversion Condition Analysis:** Explain why `child_level <= parent_level` can never be true for hierarchies built by the stack algorithm.
5. **Contract Verification:** Confirm output shape matches `BOQ_Intelligence_Public_Evidence_Contract_v1.0.md`.
6. **Inconsistency Diagram:** Visual representation of the docstring vs. implementation vs. stack algorithm conditions.

---

## Results

### Stack Algorithm Recap (`_reconstruct_hierarchy`)

- The stack algorithm in `_reconstruct_hierarchy()` (line 245: `while stack and row.level <= stack[-1].level: stack.pop()`) ensures a child is always attached to an ancestor with a lower level.
- **GUARANTEE:** Every child (`child.level`) will always have a strictly greater level than its parent (`parent.level`).
- This is a **structural property** of the algorithm. It is impossible for `child.level <= parent.level` to occur in a hierarchy produced by this algorithm.

### Hierarchy Tree Structure

```
[Row 1] Level 1
  level=1 | items=1 | child_headers=1
  [Row 3] Level 2
    level=2 | items=1 | child_headers=1
    [Row 5] Level 3
      level=3 | items=1 | child_headers=0
```
Tree structure: Head1 (L1) → Head2 (L2) → Head3 (L3)

### Step-by-Step Recursive Traversal (`_detect_structural_containment`)

| Step | Node | Child | Comparison (child.level > node.level) | Finding Recorded |
|------|------|-------|---------------------------------------|------------------|
| 1 | Head1 (L1) | Head2 (L2) | `2 > 1` = True | Yes: {parent_row: 1, parent_level: 1, child_row: 3, child_level: 2} |
| 2 | Head2 (L2) | Head3 (L3) | `3 > 2` = True | Yes: {parent_row: 3, parent_level: 2, child_row: 5, child_level: 3} |
| 3 | Head3 (L3) | (None) | (Leaf node, no children) | No |

**Total findings:** 2 (for Head1→Head2 and Head2→Head3).

### Inversion Condition Analysis (`child_level <= parent_level`)

- For `child_level <= parent_level` to be true, a child would need an equal or lower level than its parent (e.g., Head2 under Head2, or Head1 under Head2).
- The `_reconstruct_hierarchy()` stack algorithm **prevents this by design**. It pops elements from the stack until `row.level > stack[-1].level` is met.
- **Conclusion:** The docstring condition (`child_level <= parent_level`) can **NEVER be true** for hierarchies produced by `_reconstruct_hierarchy()`. It would always yield zero findings.

### Contract Output Shape Verification

The output fields from `_detect_structural_containment()` are `parent_row_number`, `parent_level`, `child_row_number`, `child_level`. These match the `structural_containment` finding type defined in `BOQ_Intelligence_Public_Evidence_Contract_v1.0.md`.

### Docstring Inconsistency Diagram

```
  Docstring (lines 402-403):
    +---------------------------------------+
    | child_level <= parent_level           |
    | (detect structural INVERSIONS)        |
    +---------------------------------------+
                    |
                    | describes OPPOSITE condition
                    v
  Implementation (line 417):
    +---------------------------------------+
    | child.level > node.level              |
    | (records ALL parent-child containment)|
    +---------------------------------------+
                    |
                    | stack algorithm guarantees this is ALWAYS True
                    v
  Stack Algorithm (_reconstruct_hierarchy):
    +---------------------------------------+
    | Every child.level > parent.level      |
    | (structural property, not anomaly)    |
    +---------------------------------------+
```

---

## Conclusion

The docstring condition (`child_level <= parent_level`) describes inversion detection that is structurally impossible for hierarchies produced by `_reconstruct_hierarchy()`. The implementation condition (`child.level > node.level`) correctly records parent-child containment facts, matching the contract output shape. The docstring condition is structurally inverted relative to the actual algorithm.

---

## Artifacts

| Item | Path |
|------|------|
| Spike tool | `tools/eq0015_spike3_algorithm_walkthrough.py` |
| JSON evidence | `data/reports/eq0015_spike3_algorithm_walkthrough.json` |

## Production Impact

None. No production code was modified. This is a documentation investigation only.