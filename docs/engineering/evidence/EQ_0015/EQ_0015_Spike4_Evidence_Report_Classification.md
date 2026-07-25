# EQ-0015 Spike 4 Evidence Report — Classification

**EQ:** EQ-0015 (Structural Containment Investigation)
**Spike:** 4 — Evidence Classification
**Date:** 2026-07-16
**Status:** Complete

---

## Purpose

Synthesize evidence from Spikes 1-3 into exactly one conclusion from the amended 5-option classification.

---

## Method

Evidence from Spike 1 (Production Behavior), Spike 2 (Historical Intent), and Spike 3 (Algorithm Walkthrough) was evaluated against each of the five classification options. Each option was assigned a "verdict" and "evidence match" score.

---

## Classification Options (Amended M9 Plan)

1. **Documentation inconsistency:** Docstring is wrong, implementation is correct.
2. **Implementation inconsistency:** Implementation is wrong, docstring is correct.
3. **Contract inconsistency:** Contract conflicts with implementation and/or docstring.
4. **Historical intent inconsistent:** Design records don't match current behavior.
5. **Insufficient evidence:** Cannot determine from available evidence.

---

## Evidence Summary

### S1: Production Behavior (from `eq0015_spike1_production_behavior.json`)
- Implementation condition (`child.level > node.level`) fires for all parent-child pairs.
- Normal hierarchy: 2 findings. Inverted hierarchy: 1 finding.
- Implementation cannot distinguish normal from inverted containment.

### S2: Historical Intent (from `eq0015_spike2_historical_intent.json`)
- No EQ (0010, 0011, 0012) specified `child_level <= parent_level`.
- Contract defines output shape only (`structural_containment` finding type is neutral).
- Internal naming mismatch (containment/inversion/inversions) suggests docstring written for intent never fully implemented.

### S3: Algorithm Walkthrough (from `eq0015_spike3_algorithm_walkthrough.json`)
- Stack algorithm (`_reconstruct_hierarchy` line 245) guarantees `child.level > parent.level` always.
- Docstring condition (`child_level <= parent_level`) is structurally impossible for any stack-built hierarchy. It would produce zero findings.

---

## Classification Matrix

| Option | Name | Verdict | S1 Match | S2 Match | S3 Match | Reasoning |
|--------|------|---------|----------|----------|----------|-----------|
| 1 | Documentation inconsistency | **CONSISTENT** | True | True | True | Implementation records parent-child level facts per contract. Docstring describes inversion detection (`<=`), contradicting implementation, lacking historical spec, and is structurally impossible for stack-built hierarchies. Docstring is the outlier. |
| 2 | Implementation inconsistency | INCONSISTENT | False | False | False | Accepting docstring (`<=`) as correct would break the implementation, yielding zero findings for all hierarchies due to stack algorithm. No historical spec for `<=`. |
| 3 | Contract inconsistency | INCONSISTENT | False | False | False | Contract defines output shape (neutral `structural_containment`). Implementation produces this shape correctly. Contract does not specify detection condition. |
| 4 | Historical intent inconsistent | PARTIALLY CONSISTENT | False | True | False | Naming inconsistency suggests original intent may have been inversion detection. However, implementation and contract evolved to containment recording. No spec for `<=` condition exists. This is a contributing factor, not the root cause. |
| 5 | Insufficient evidence | INCONSISTENT | False | False | False | Convergent evidence from three spikes is sufficient for classification. |

---

## Final Classification

**EXACTLY ONE CONCLUSION:**

**OPTION 1: DOCUMENTATION INCONSISTENCY**

The docstring at `src/jarvis/parsers/costx/boq_intelligence.py:398–411` is inconsistent with the implementation (`child.level > node.level`), the BOQ Intelligence contract, the structural guarantees of the stack algorithm, and the historical design records.

**Specifically:**
1.  **Docstring claims inversion detection** (`child_level <= parent_level`).
2.  **Implementation uses containment recording** (`child.level > node.level`).
3.  **Stack algorithm guarantees `child.level > parent.level` always.**
4.  **No EQ specified the `child_level <= parent_level` condition.**
5.  **Contract defines output shape, not detection condition.**
6.  **Implementation output matches contract.**

The docstring is the single inconsistent artifact. All other artifacts (implementation, contract, stack algorithm, historical design records) are consistent with each other.

---

## Recommendation

**Docstring correction only. No production code change.**

-   Update `child_level <= parent_level` to `child.level > node.level`
-   Update `structural inversions` to `structural containment`
-   Rename local variable `inversions` to `containment_pairs`
-   Update the inline comment at line 418 to reflect actual behavior

Project Owner must authorize any fix after Gate 2 (Architecture Verification) review.

---

## Artifacts

| Item | Path |
|------|------|
| Spike tool | `tools/eq0015_spike4_evidence_classification.py` |
| JSON evidence | `data/reports/eq0015_spike4_evidence_classification.json` |

## Production Impact

None. No production code was modified. This is a documentation investigation only.