# EQ-0015: Structural Containment Investigation

**Status:** Investigation Complete — Awaiting Project Owner Gate 2 Review

**Filed:** 2026-07-16

**Authority:** Project Owner Approved (M9 WP-A)

---

## Core Question

Is the discrepancy between `_detect_structural_containment()` docstring (`child_level <= parent_level`) and implementation (`child.level > node.level`) a:

1. Documentation inconsistency (docstring wrong, implementation correct)
2. Implementation inconsistency (implementation wrong, docstring correct)
3. Contract inconsistency (contract conflicts)
4. Historical intent inconsistent (design records don't match)
5. Insufficient evidence (cannot determine)

---

## Context

Discovered during EQ-0014 Spike 2 (Test Correction). While examining `_detect_structural_containment()` at `boq_intelligence.py:398–430`, the condition at line 417 (`child.level > node.level`) appeared structurally inverted relative to the docstring at line 402 (`child_level <= parent_level`).

The stack algorithm in `_reconstruct_hierarchy()` guarantees `child.level > parent.level` for every parent-child pair in any tree it produces. This means the docstring condition (`<=`) would never be true for any stack-built hierarchy.

EQ-0014-02 flagged this for separate investigation. EQ-0015 was authorized as a pure investigation — no production code modifications.

---

## Evidence References

The docstring at line 399 cites "Evidence: EQ-0010 Spike 4, EQ-0011 Spike 3." These spikes established hierarchy reconstruction (EQ-0010) and the Detection vs. Decision boundary (EQ-0011), but neither specified `child_level <= parent_level` as a detection condition.

---

## Spike Plan

| Spike | Purpose | Status |
|-------|---------|--------|
| Spike 1 | Production behavior — execute on normal and inverted hierarchies | Complete |
| Spike 2 | Historical intent — trace EQ-0010, EQ-0011, EQ-0012 design records | Complete |
| Spike 3 | Algorithm walkthrough — step-by-step traversal with stack diagrams | Complete |
| Spike 4 | Evidence classification — 5-option matrix, exactly one conclusion | Complete |

---

## Evidence Artifacts

| Artifact | Path |
|----------|------|
| Spike 1 tool | `tools/eq0015_spike1_production_behavior.py` |
| Spike 1 JSON | `data/reports/eq0015_spike1_production_behavior.json` |
| Spike 1 report | `docs/engineering/evidence/EQ_0015_Spike1_Evidence_Report_Production_Behavior.md` |
| Spike 2 tool | `tools/eq0015_spike2_historical_intent.py` |
| Spike 2 JSON | `data/reports/eq0015_spike2_historical_intent.json` |
| Spike 2 report | `docs/engineering/evidence/EQ_0015_Spike2_Evidence_Report_Historical_Intent.md` |
| Spike 3 tool | `tools/eq0015_spike3_algorithm_walkthrough.py` |
| Spike 3 JSON | `data/reports/eq0015_spike3_algorithm_walkthrough.json` |
| Spike 3 report | `docs/engineering/evidence/EQ_0015_Spike3_Evidence_Report_Algorithm_Walkthrough.md` |
| Spike 4 tool | `tools/eq0015_spike4_evidence_classification.py` |
| Spike 4 JSON | `data/reports/eq0015_spike4_evidence_classification.json` |
| Spike 4 report | `docs/engineering/evidence/EQ_0015_Spike4_Evidence_Report_Classification.md` |

---

## Key Findings Summary

### Spike 1 — Production Behavior
- Normal hierarchy (Head1→Head2→Head3): Implementation produces 2 findings (every parent-child pair)
- Inverted hierarchy (Head1→Head3, skip Head2): Implementation produces 1 finding
- Implementation cannot distinguish normal containment from structural inversion
- Docstring condition (`<=`) would produce ZERO findings for either hierarchy

### Spike 2 — Historical Intent
- EQ-0010: Defined hierarchy reconstruction, NOT inversion/containment detection
- EQ-0011: Defined Detection vs. Decision boundary, NOT `child_level <= parent_level`
- EQ-0012/Contract: Defines output shape (`structural_containment` finding type), NOT detection condition
- Internal naming mismatch: function=`structural_containment`, docstring=`structural inversions`, variable=`inversions`

### Spike 3 — Algorithm Walkthrough
- Stack algorithm (`_reconstruct_hierarchy` line 245: `while row.level <= stack[-1].level: stack.pop()`) guarantees `child.level > parent.level` always
- Docstring condition (`child_level <= parent_level`) is structurally impossible for any stack-built hierarchy
- Contract output shape verified — implementation produces correct fields

### Spike 4 — Evidence Classification
- **Selected: Option 1 — Documentation Inconsistency** (3/3 evidence match)
- Options 2–5 all inconsistent with evidence (0/3 or 1/3)
- Only option 1 is consistent with all three evidence sources

---

## Conclusion

**Classification: Documentation Inconsistency**

The docstring at `boq_intelligence.py:398–411` is the single inconsistent artifact. The implementation (`child.level > node.level`), the BOQ Intelligence contract, the stack algorithm's structural guarantees, and the historical design records (EQ-0010, EQ-0011, EQ-0012) are all consistent with each other.

The docstring:
- Describes inversion detection (`child_level <= parent_level`)
- Has no supporting specification in any EQ
- Describes a condition structurally impossible for stack-built hierarchies
- Uses terminology (`structural inversions`) inconsistent with the contract finding type name (`structural_containment`)

---

## Recommendation

**Docstring correction only. No production code change.**

- Update `child_level <= parent_level` to `child.level > node.level`
- Update `structural inversions` to `structural containment`
- Rename local variable `inversions` to `containment_pairs`
- Update the inline comment at line 418 to reflect actual behavior

Project Owner must authorize any fix after Gate 2 (Architecture Verification) review.

---

## Engineering Debt

| ID | Finding | Severity | Blocks Freeze | Planned Resolution | Status |
|----|---------|----------|---------------|-------------------|--------|
| EQ-0015-01 | `_detect_structural_containment()` docstring describes inversion detection (`child_level <= parent_level`) but implementation records containment (`child.level > node.level`). Local variable and docstring terminology inconsistent with contract. | Low | No | Docstring correction (no production code change). Project Owner authorization required. | Open |

---

## Success Criteria

- [x] Exactly one classification determined (Option 1: Documentation Inconsistency)
- [x] Evidence supports docstring correction only (3/3 evidence match)
- [x] No production code modified
- [x] All 4 spike tools executed with JSON evidence
- [x] All 4 evidence reports written
- [x] Engineering debt registered
- [ ] Project Owner Gate 2 review
- [ ] Docstring correction authorized (if approved)

---

## References

- `src/jarvis/parsers/costx/boq_intelligence.py` lines 398–430 (`_detect_structural_containment`)
- `src/jarvis/parsers/costx/boq_intelligence.py` lines 190–280 (`_reconstruct_hierarchy`)
- `docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md` (finding type `structural_containment`)
- EQ-0010: `docs/engineering/questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md`
- EQ-0011: `docs/engineering/questions/EQ_0011_BOQ_Semantic_Intelligence_Boundary.md`
- EQ-0012: `docs/engineering/questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md`
- EQ-0014 Spike 2: `docs/engineering/evidence/EQ_0014_Spike2_Evidence_Report_Test_Correction.md` (discovery source)