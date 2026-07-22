"""
EQ-0015 Spike 4 — Evidence Classification
Synthesize evidence from Spikes 1-3 into exactly one conclusion
from the amended 5-option classification.

Classification options:
  1. Documentation inconsistency
  2. Implementation inconsistency
  3. Contract inconsistency
  4. Historical intent inconsistent
  5. Insufficient evidence

No production code modification. Investigation only.
Project Owner decides after Gate 2 review.
"""

import json
from pathlib import Path


def main():
    print("=" * 70)
    print("EQ-0015 Spike 4 — Evidence Classification")
    print("=" * 70)

    classification = {
        "eq": "EQ-0015",
        "spike": 4,
        "title": "Evidence Classification — _detect_structural_containment() Discrepancy",
        "classification_options": [
            {"id": 1, "name": "Documentation inconsistency", "description": "Docstring is wrong, implementation is correct"},
            {"id": 2, "name": "Implementation inconsistency", "description": "Implementation is wrong, docstring is correct"},
            {"id": 3, "name": "Contract inconsistency", "description": "Contract conflicts with implementation and/or docstring"},
            {"id": 4, "name": "Historical intent inconsistent", "description": "Design records don't match current behavior"},
            {"id": 5, "name": "Insufficient evidence", "description": "Cannot determine from available evidence"},
        ],
        "evidence_summary": [],
        "classification_matrix": [],
    }

    # Evidence Item 1: Production behavior (Spike 1)
    print("\n--- Evidence S1: Production Behavior ---")
    print("  Normal hierarchy: 2 findings (Head1->Head2, Head2->Head3)")
    print("  Inverted hierarchy: 1 finding (Head1->Head3)")
    print("  Implementation fires for EVERY parent-child pair")
    print("  Cannot distinguish normal containment from inversion")
    classification["evidence_summary"].append({
        "source": "Spike 1",
        "finding": "Implementation condition (child.level > node.level) fires for all parent-child pairs. "
                   "Normal hierarchy: 2 findings. Inverted hierarchy: 1 finding. "
                   "Cannot distinguish normal from inverted.",
    })

    # Evidence Item 2: Historical intent (Spike 2)
    print("\n--- Evidence S2: Historical Intent ---")
    print("  EQ-0010: Did NOT specify inversion/containment detection")
    print("  EQ-0011: Did NOT specify child_level <= parent_level")
    print("  EQ-0012/Contract: Defines output shape, not detection condition")
    print("  Internal naming mismatch: 3 different names for same concept")
    classification["evidence_summary"].append({
        "source": "Spike 2",
        "finding": "No EQ (0010, 0011, 0012) specified child_level <= parent_level. "
                   "Contract defines output shape only. Internal naming (containment/inversion/inversions) "
                   "suggests docstring written for intent never implemented.",
    })

    # Evidence Item 3: Algorithm walkthrough (Spike 3)
    print("\n--- Evidence S3: Algorithm Walkthrough ---")
    print("  Stack algorithm guarantees child.level > parent.level ALWAYS")
    print("  Docstring condition (<=) is structurally impossible")
    print("  Would produce ZERO findings for any stack-built hierarchy")
    classification["evidence_summary"].append({
        "source": "Spike 3",
        "finding": "Stack algorithm (line 245: while row.level <= stack[-1].level: stack.pop()) "
                   "guarantees child.level > parent.level always. "
                   "Docstring condition (<=) would produce zero findings for any stack-built hierarchy. "
                   "Docstring condition is structurally impossible.",
    })

    # Classification Matrix
    print(f"\n{'=' * 70}")
    print("CLASSIFICATION MATRIX")
    print(f"{'=' * 70}")
    print()

    matrix = []

    # Option 1: Documentation inconsistency
    opt1 = {
        "option": 1,
        "name": "Documentation inconsistency",
        "verdict": "CONSISTENT with all evidence",
        "matches_evidence": {
            "S1_production_behavior": True,
            "S2_historical_intent": True,
            "S3_algorithm_walkthrough": True,
        },
        "reasoning": (
            "Implementation correctly records parent-child level facts matching the contract output shape. "
            "Docstring describes inversion detection (<=) which: (a) contradicts the implementation (>), "
            "(b) has no supporting historical design specification, (c) is structurally impossible "
            "for stack-built hierarchies. Docstring is the outlier."
        ),
    }

    # Option 2: Implementation inconsistency
    opt2 = {
        "option": 2,
        "name": "Implementation inconsistency",
        "verdict": "INCONSISTENT with evidence",
        "matches_evidence": {
            "S1_production_behavior": False,
            "S2_historical_intent": False,
            "S3_algorithm_walkthrough": False,
        },
        "reasoning": (
            "Would require accepting docstring (<=) as correct and implementation (>) as wrong. "
            "But docstring has no historical design specification. Stack algorithm makes <= impossible "
            "for any hierarchy it produces. 'Fixing' implementation to <= would break it — "
            "zero findings for all hierarchies."
        ),
    }

    # Option 3: Contract inconsistency
    opt3 = {
        "option": 3,
        "name": "Contract inconsistency",
        "verdict": "INCONSISTENT with evidence",
        "matches_evidence": {
            "S1_production_behavior": False,
            "S2_historical_intent": False,
            "S3_algorithm_walkthrough": False,
        },
        "reasoning": (
            "Contract defines output shape (parent_row_number, parent_level, child_row_number, child_level) "
            "and the finding type name 'structural_containment.' Implementation produces exactly this shape. "
            "Contract does NOT specify the detection condition. No contract conflict exists."
        ),
    }

    # Option 4: Historical intent inconsistent
    opt4 = {
        "option": 4,
        "name": "Historical intent inconsistent",
        "verdict": "PARTIALLY CONSISTENT",
        "matches_evidence": {
            "S1_production_behavior": False,
            "S2_historical_intent": True,
            "S3_algorithm_walkthrough": False,
        },
        "reasoning": (
            "There IS evidence of naming inconsistency (containment vs. inversion vs. inversions) "
            "suggesting the original intent may have been inversion detection. But the implementation "
            "and contract evolved to containment recording. The historical record is incomplete — "
            "no specification for the <= condition exists. This is a contributing factor, not the root cause."
        ),
    }

    # Option 5: Insufficient evidence
    opt5 = {
        "option": 5,
        "name": "Insufficient evidence",
        "verdict": "INCONSISTENT with evidence",
        "matches_evidence": {
            "S1_production_behavior": False,
            "S2_historical_intent": False,
            "S3_algorithm_walkthrough": False,
        },
        "reasoning": (
            "Three independent spikes provide convergent evidence. Production behavior is documented. "
            "Historical design records are traced. Algorithm mechanics are proven. Evidence is sufficient "
            "to classify this as a documentation inconsistency."
        ),
    }

    matrix = [opt1, opt2, opt3, opt4, opt5]

    for opt in matrix:
        matches = sum(1 for v in opt["matches_evidence"].values() if v)
        total = len(opt["matches_evidence"])
        print(f"  Option {opt['option']}: {opt['name']}")
        print(f"    Verdict: {opt['verdict']}")
        print(f"    Evidence match: {matches}/{total}")
        if matches == 3:
            print(f"    >>> ONLY OPTION CONSISTENT WITH ALL EVIDENCE <<<")
        print()

    classification["classification_matrix"] = matrix

    # CONCLUSION
    print(f"{'=' * 70}")
    print("FINAL CLASSIFICATION")
    print(f"{'=' * 70}")
    print()
    print("  EXACTLY ONE CONCLUSION:")
    print()
    print("  OPTION 1: DOCUMENTATION INCONSISTENCY")
    print()
    print("  The docstring at boq_intelligence.py:398-411 is inconsistent with")
    print("  the implementation, the contract, the historical design records,")
    print("  and the structural guarantees of the stack algorithm.")
    print()
    print("  Specifically:")
    print("    1. Docstring claims child_level <= parent_level (inversion detection)")
    print("    2. Implementation uses child.level > node.level (containment recording)")
    print("    3. Stack algorithm guarantees child.level > parent.level always")
    print("    4. No EQ specified the <= condition")
    print("    5. Contract defines output shape, not detection condition")
    print("    6. Implementation output matches contract")
    print()
    print("  The docstring is the single inconsistent artifact.")
    print("  All other artifacts (implementation, contract, stack algorithm,")
    print("  historical design records) are consistent with each other.")
    print()
    print("  RECOMMENDATION: Docstring correction (not production code change)")
    print("    - Update 'child_level <= parent_level' to 'child.level > node.level'")
    print("    - Update 'structural inversions' to 'structural containment'")
    print("    - Rename local variable 'inversions' to 'containment_pairs'")
    print()
    print("  Project Owner must authorize any fix after Gate 2 review.")

    classification["conclusion"] = {
        "selected_option": 1,
        "name": "Documentation inconsistency",
        "summary": "Docstring is the single inconsistent artifact. Implementation, contract, "
                   "stack algorithm, and historical design records are all consistent. "
                   "Docstring describes inversion detection (<=) — condition is structurally "
                   "impossible for stack-built hierarchies and has no supporting design specification.",
        "recommendation": "Docstring correction only. No production code change.",
        "requires_project_owner": True,
        "gate": "Gate 2 (Architecture Verification)",
    }

    # Write JSON evidence
    output_path = Path(__file__).parent.parent / "data" / "reports" / "eq0015_spike4_evidence_classification.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(classification, f, indent=2)
    print(f"\nJSON evidence written to: {output_path}")


if __name__ == "__main__":
    main()