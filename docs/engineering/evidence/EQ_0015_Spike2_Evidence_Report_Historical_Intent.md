# EQ-0015 Spike 2 Evidence Report — Historical Intent

**EQ:** EQ-0015 (Structural Containment Investigation)
**Spike:** 2 — Historical Engineering Intent
**Date:** 2026-07-16
**Status:** Complete

---

## Purpose

Trace the design intent for `_detect_structural_containment()` through EQ-0010, EQ-0011, EQ-0012, and the BOQ Intelligence contract. Determine whether the `child_level <= parent_level` condition has any supporting historical specification.

---

## Sources Analyzed

| Source | Path |
|--------|------|
| EQ-0010 | `docs/engineering/questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md` |
| EQ-0011 | `docs/engineering/questions/EQ_0011_BOQ_Semantic_Intelligence_Boundary.md` |
| EQ-0012 | `docs/engineering/questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md` |
| Contract | `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` |
| Production code | `src/jarvis/parsers/costx/boq_intelligence.py` lines 398–430 |

---

## Evidence Items

### E1: EQ-0010 — Foundation (Deterministic BOQ Structural Intelligence)

**Status:** Not frozen (investigation phase)

EQ-0010 defined hierarchy reconstruction (stack algorithm) and level progression patterns in Spike 4. It did NOT define:
- Structural inversion detection
- Containment checking
- A `child_level <= parent_level` condition

Capability V-004 ("Scope Containment") was classified as Domain Dependent and described semantic scope ("children fit within parent scope"), not structural level comparison.

**Finding:** EQ-0010 did not specify a structural containment detector. The docstring reference "Evidence: EQ-0010 Spike 4" traces to hierarchy reconstruction, not to the `<=` condition.

---

### E2: EQ-0011 — Engineering Boundary (BOQ Semantic Intelligence Boundary)

**Status:** Investigation approved, not started

EQ-0011 established the Detection vs. Decision boundary:
- Detection = observable structural facts (no professional judgment)
- Decision = semantic interpretation (professional QS judgment)

Spike 3 (Boundary Validation) validated what constitutes a structural fact vs. professional judgment. It did NOT define `child_level <= parent_level` as a boundary condition or detection algorithm.

**Finding:** EQ-0011 defined the boundary philosophy but did not specify the specific condition for structural containment detection.

---

### E3: EQ-0012 + BOQ Intelligence Contract

**Status:** Frozen (contract v1.0)

The contract defines the `structural_containment` finding type with fields:
- `parent_row_number`
- `parent_level`
- `child_row_number`
- `child_level`

The finding type description is neutral: "Records structural hierarchy relationships." It does NOT mention:
- Inversions as the purpose
- `child_level <= parent_level` as a detection condition

The finding type name `structural_containment` is neutral — it records containment facts, not necessarily inversion facts.

**Finding:** The contract defines the output shape, not the detection condition. Implementation produces the correct output shape per contract.

---

### E4: Internal Naming Mismatch

Three different names for the same concept within the function:

| Artifact | Name Used |
|----------|-----------|
| Function name | `_detect_structural_containment` |
| Docstring (line 403) | "structural inversions" |
| Local variable (line 413) | `inversions` |
| Contract finding type | `structural_containment` |

This naming drift suggests evolution of intent during development:
- Original intent may have been inversion detection (variable name `inversions`)
- Docstring was written for inversion detection (`<=` condition)
- Implementation was written for containment recording (`>` condition)
- Contract adopted the neutral name `structural_containment`
- Naming was never reconciled across artifacts

---

### E5: Production Code Docstring vs. Implementation

The docstring at line 402: `"Verifies structural hierarchy relationships only (child_level <= parent_level)."`

The implementation at line 417: `if child.level > node.level:`

These describe **opposite conditions**. The docstring describes detection of INVERSIONS (`<=`). The implementation records ALL parent-child relationships (`>`).

---

## Conclusion

**No EQ (0010, 0011, 0012) specified `child_level <= parent_level` as the detection condition for structural containment.**

The contract defines the output shape, not the detection condition.

The docstring's inversion detection intent (`<=`) has no supporting evidence in any historical design specification. The internal naming mismatch (containment vs. inversion vs. inversions) suggests the docstring was written for an intent that was never implemented — or was changed during development without updating the docstring.

**Classification:** Documentation Inconsistency. The docstring is the inconsistent artifact. Implementation, contract, and historical records are consistent.

---

## Artifacts

| Item | Path |
|------|------|
| Spike tool | `tools/eq0015_spike2_historical_intent.py` |
| JSON evidence | `data/reports/eq0015_spike2_historical_intent.json` |

## Production Impact

None. No production code was modified. This is a documentation investigation only.