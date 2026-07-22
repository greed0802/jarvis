"""
EQ-0015 Spike 2 — Historical Engineering Intent Trace
Trace the design intent for _detect_structural_containment() through
EQ-0010, EQ-0011, EQ-0012, and the BOQ Intelligence contract.

Purpose: Determine whether the current condition (child.level > node.level)
matches the original engineering intent, or whether the docstring (child_level <= parent_level)
described a different intent that was never implemented.

No production code modification. Investigation only.
"""

import json
from pathlib import Path


def main():
    print("=" * 70)
    print("EQ-0015 Spike 2 — Historical Engineering Intent Trace")
    print("=" * 70)

    findings = {
        "eq": "EQ-0015",
        "spike": 2,
        "title": "Historical Engineering Intent Trace — _detect_structural_containment()",
        "sources_analyzed": [
            "docs/engineering/questions/EQ_0010_Deterministic_BOQ_Structural_Intelligence.md",
            "docs/engineering/questions/EQ_0011_BOQ_Semantic_Intelligence_Boundary.md",
            "docs/engineering/questions/EQ_0012_BOQ_Intelligence_Public_Evidence_Contract.md",
            "docs/contracts/BOQ_Intelligence_Public_Evidence_Contract_v1.0.md",
            "src/jarvis/parsers/costx/boq_intelligence.py (docstring + implementation)",
        ],
        "evidence_items": [],
    }

    # Evidence Item 1: EQ-0010 — Foundation
    print("\n--- Evidence 1: EQ-0010 (Deterministic BOQ Structural Intelligence) ---")
    print("  Status: Not frozen (investigation phase)")
    print("  Spike 4: Structural Pattern Detection")
    print("    Defined patterns: level progression, empty headers, orphan items, section integrity")
    print("    Did NOT define structural inversion detection")
    print("    Did NOT define containment checking")
    print("  Capability V-004: Scope Containment — classified as Domain Dependent")
    print("    \"scope containment: children fit within parent scope\"")
    print("    This is SEMANTIC scope, not structural level comparison")
    print("  CONCLUSION: EQ-0010 did NOT specify a structural containment detector.")
    print("    The docstring claim \"Evidence: EQ-0010 Spike 4\" is a reference to")
    print("    hierarchy reconstruction, not to inversion/containment detection.")
    findings["evidence_items"].append({
        "id": "E1",
        "source": "EQ-0010 + Spike 4",
        "finding": "EQ-0010 defined hierarchy reconstruction (stack algorithm) and level progression patterns. "
                   "It did NOT define structural inversion or containment detection. "
                   "The docstring reference to EQ-0010 Spike 4 traces to hierarchy reconstruction, "
                   "not to the <= condition.",
    })

    # Evidence Item 2: EQ-0011 — Engineering Boundary
    print("\n--- Evidence 2: EQ-0011 (BOQ Semantic Intelligence Boundary) ---")
    print("  Status: Investigation approved, not started")
    print("  Core distinction: Detection vs. Decision")
    print("    Detection = observable structural facts (no professional judgment)")
    print("    Decision = semantic interpretation (professional QS judgment)")
    print("  Spike 3 (Boundary Validation) referenced in docstring")
    print("    The spike established: what is a fact vs. what is an assessment")
    print("    Did NOT specify an inversion detection algorithm")
    print("    Did NOT define child_level <= parent_level as a boundary condition")
    print("  CONCLUSION: EQ-0011 defined the boundary philosophy (detection vs. decision)")
    print("    but did NOT specify the specific condition for structural containment.")
    findings["evidence_items"].append({
        "id": "E2",
        "source": "EQ-0011 + Spike 3",
        "finding": "EQ-0011 established the Detection vs. Decision boundary. "
                   "Spike 3 validated what constitutes a structural fact vs. professional judgment. "
                   "Neither specified the child_level <= parent_level condition for containment detection.",
    })

    # Evidence Item 3: EQ-0012 + Contract
    print("\n--- Evidence 3: EQ-0012 + BOQ Intelligence Contract ---")
    print("  Contract: BOQ_Intelligence_Public_Evidence_Contract_v1.0.md")
    print("  Finding type: 'structural_containment'")
    print("  Fields: parent_row_number, parent_level, child_row_number, child_level")
    print("  Description: Records structural hierarchy relationships")
    print("  Does NOT mention 'inversions' as the purpose")
    print("  Does NOT specify child_level <= parent_level")
    print("  The finding type name 'structural_containment' is NEUTRAL")
    print("    — it records containment facts, not necessarily inversion facts")
    print("  CONCLUSION: The contract defines the output shape, not the detection condition.")
    print("    The implementation produces the correct output shape per the contract.")
    findings["evidence_items"].append({
        "id": "E3",
        "source": "EQ-0012 + BOQ Intelligence Contract v1.0",
        "finding": "Contract defines finding type 'structural_containment' with fields "
                   "(parent_row_number, parent_level, child_row_number, child_level). "
                   "Does NOT specify child_level <= parent_level as the detection condition. "
                   "Implementation produces correct output shape per contract.",
    })

    # Evidence Item 4: Internal naming mismatch
    print("\n--- Evidence 4: Internal Naming Mismatch ---")
    print("  Function: _detect_structural_containment()")
    print("  Docstring: 'Records observable facts about structural inversions.'")
    print("  Local variable: 'inversions: list[dict[str, int]] = []'")
    print("  Contract finding type: 'structural_containment'")
    print("  Finding: THREE different names for the same concept:")
    print("    - Function name: structural_containment")
    print("    - Docstring: structural inversions")
    print("    - Variable: inversions")
    print("  This suggests evolution of intent during development:")
    print("    Original intent may have been inversion detection (variable name)")
    print("    Docstring was written for inversion detection (<= condition)")
    print("    But implementation was written for containment recording (> condition)")
    print("    Contract adopted the neutral name 'structural_containment'")
    print("    Naming was never reconciled across the three artifacts")
    findings["evidence_items"].append({
        "id": "E4",
        "source": "Internal naming analysis",
        "finding": "Three different names for same concept: function='structural_containment', "
                   "docstring='structural inversions', variable='inversions'. "
                   "Suggests evolution of intent: original inversion detection (<=) "
                   "became containment recording (>) during implementation, "
                   "but docstring and variable were never updated to match.",
    })

    # Evidence Item 5: Production code docstring vs implementation
    print("\n--- Evidence 5: Production Code Docstring vs Implementation ---")
    print("  Line 402: 'Verifies structural hierarchy relationships only (child_level <= parent_level).'")
    print("  Line 403: 'Records observable facts about structural inversions.'")
    print("  Line 417: 'if child.level > node.level:'")
    print("  Stack guarantee: child.level ALWAYS > parent.level")
    print("  Result: Docstring describes detection of INVERSIONS (<=)")
    print("          Implementation records ALL parent-child relationships (>)")
    print("          These are OPPOSITE conditions")
    findings["evidence_items"].append({
        "id": "E5",
        "source": "boq_intelligence.py lines 398-430",
        "finding": "Docstring (line 402): child_level <= parent_level (inversions). "
                   "Implementation (line 417): child.level > node.level (all containment). "
                   "Stack algorithm guarantees child.level > parent.level always. "
                   "These describe opposite conditions.",
    })

    # Summary
    print(f"\n{'=' * 70}")
    print("HISTORICAL INTENT CONCLUSION")
    print(f"{'=' * 70}")
    print()
    print("  No EQ (0010, 0011, 0012) specified child_level <= parent_level")
    print("  as the detection condition for structural containment.")
    print()
    print("  The contract defines the OUTPUT SHAPE, not the DETECTION CONDITION.")
    print()
    print("  The docstring (<= condition, inversion detection) has NO")
    print("  supporting evidence in EQ-0010 Spike 4 or EQ-0011 Spike 3.")
    print()
    print("  Internal naming mismatch (containment vs. inversion vs. inversions)")
    print("  suggests the docstring was written for an inversion-detection intent")
    print("  that was never implemented — or was changed during development")
    print("  without updating the docstring.")
    print()
    print("  CLASSIFICATION: Documentation Inconsistency")
    print("    - Implementation correctly records parent-child level facts")
    print("    - Output matches the contract shape")
    print("    - Docstring describes inversion detection (<=) which has no")
    print("      historical design specification and contradicts implementation")

    findings["conclusion"] = (
        "Documentation Inconsistency. No EQ specified child_level <= parent_level. "
        "Contract defines output shape only, not detection condition. "
        "Docstring's inversion detection intent has no supporting evidence in EQ-0010 or EQ-0011. "
        "Implementation correctly records parent-child level facts per contract. "
        "Docstring should describe containment recording (> ), not inversion detection (<=)."
    )

    # Write JSON evidence
    output_path = Path(__file__).parent.parent / "data" / "reports" / "eq0015_spike2_historical_intent.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(findings, f, indent=2)
    print(f"\nJSON evidence written to: {output_path}")


if __name__ == "__main__":
    main()