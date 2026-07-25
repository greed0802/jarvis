# EQ-0015 Spike 1 Evidence Report — Production Behavior

**EQ:** EQ-0015 (Structural Containment Investigation)
**Spike:** 1 — Production Behavior
**Date:** 2026-07-16
**Status:** Complete

---

## Purpose

Execute `_detect_structural_containment()` on normal and inverted hierarchies to document actual production behavior vs. docstring claims.

---

## Method

Two test hierarchies constructed:
1. **Normal:** Head1 → Head2 → Head3 (standard stack-built tree)
2. **Inverted:** Head1 → Head3 (skip Head2, level gap)

Both hierarchies executed through `_reconstruct_hierarchy()` then `_detect_structural_containment()`. Every `child.level > node.level` comparison traced.

---

## Results

### Normal Hierarchy (Head1 → Head2 → Head3)

**Tree structure:**
```
Row 1: Level 1 (level=1, children=1)
  Row 3: Level 2 (level=2, children=1)
    Row 5: Level 3 (level=3, children=0)
```

**Findings: 2**

| # | parent_row | parent_level | child_row | child_level |
|---|------------|--------------|-----------|-------------|
| 1 | 1 | 1 | 3 | 2 |
| 2 | 3 | 2 | 5 | 3 |

**Condition walkthrough:**
- `child.level(2) > node.level(1)` = True → FIRES
- `child.level(3) > node.level(2)` = True → FIRES

### Inverted Hierarchy (Head1 → Head3, skip Head2)

**Tree structure:**
```
Row 1: Level 1 (level=1, children=1)
  Row 2: Level 3 SKIP (level=3, children=0)
```

**Findings: 1**

| # | parent_row | parent_level | child_row | child_level |
|---|------------|--------------|-----------|-------------|
| 1 | 1 | 1 | 2 | 3 |

**Condition walkthrough:**
- `child.level(3) > node.level(1)` = True → FIRES

### Docstring Condition Simulation

The docstring condition `child_level <= parent_level` would produce:
- Normal hierarchy: **0 findings** (2 > 1 is false, 3 > 2 is false)
- Inverted hierarchy: **0 findings** (3 <= 1 is false)

The docstring condition would produce **ZERO findings for any stack-built hierarchy.**

---

## Analysis

1. Implementation condition (`>`) fires for **EVERY** parent-child pair — it records normal structural containment, not inversions.

2. Implementation **cannot distinguish** normal containment from structural inversion. Both scenarios produce findings for every parent-child pair.

3. Docstring condition (`<=`) would produce **zero findings** for any hierarchy produced by `_reconstruct_hierarchy()` — the stack algorithm guarantees `child.level > parent.level` always.

4. The inline comment at line 418 ("This should never occur given stack algorithm, but check anyway") suggests the developer expected `>` to detect anomalies, when it actually fires for every normal parent-child pair.

5. The local variable name `inversions` matches the docstring intent, not the implementation behavior.

---

## Conclusion

The implementation condition (`child.level > node.level`) is structurally inverted relative to the docstring (`child_level <= parent_level`). The implementation records normal containment facts per the contract output shape. The docstring describes inversion detection that is structurally impossible for stack-built hierarchies.

---

## Artifacts

| Item | Path |
|------|------|
| Spike tool | `tools/eq0015_spike1_production_behavior.py` |
| JSON evidence | `data/reports/eq0015_spike1_production_behavior.json` |

## Production Impact

None. No production code was modified. This is a documentation investigation only.