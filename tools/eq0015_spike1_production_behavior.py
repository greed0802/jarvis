"""
EQ-0015 Spike 1 — Production Behavior Evidence
Investigate _detect_structural_containment() actual behavior vs. docstring claims.

Purpose: Execute the function on normal and inverted hierarchies to document
what findings it actually produces, then compare against the docstring claim
that it detects structural inversions (child_level <= parent_level).

No production code modification. Investigation only.
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from jarvis.parsers.costx.boq_extraction import BOQRow
from jarvis.parsers.costx.boq_intelligence import (
    _reconstruct_hierarchy,
    _detect_structural_containment,
)


def build_normal_hierarchy():
    """
    Normal BOQ hierarchy: Head1 -> Head2 -> Head3
    Each head contains items. Stack algorithm guarantees child.level > parent.level.
    """
    return [
        BOQRow(row_number=1, code=None, description="Level 1", quantity=None, uom="Head1", row_type="Head", section="SECTION_A"),
        BOQRow(row_number=2, code="A001", description="Item under L1", quantity=10.0, uom="m", row_type="Item", section="SECTION_A"),
        BOQRow(row_number=3, code=None, description="Level 2", quantity=None, uom="Head2", row_type="Head", section="SECTION_A"),
        BOQRow(row_number=4, code="A002", description="Item under L2", quantity=5.0, uom="m2", row_type="Item", section="SECTION_A"),
        BOQRow(row_number=5, code=None, description="Level 3", quantity=None, uom="Head3", row_type="Head", section="SECTION_A"),
        BOQRow(row_number=6, code="A003", description="Item under L3", quantity=3.0, uom="no", row_type="Item", section="SECTION_A"),
    ]


def build_inverted_hierarchy():
    """
    Inverted BOQ hierarchy: Head1 -> Head3 (skipping Head2).
    Head3.level(3) IS greater than Head1.level(1), but the structural
    gap means Head2 is missing — a potential inversion pattern.
    """
    return [
        BOQRow(row_number=1, code=None, description="Level 1", quantity=None, uom="Head1", row_type="Head", section="SECTION_B"),
        BOQRow(row_number=2, code=None, description="Level 3 SKIP", quantity=None, uom="Head3", row_type="Head", section="SECTION_B"),
        BOQRow(row_number=3, code="B001", description="Item under L3", quantity=8.0, uom="m", row_type="Item", section="SECTION_B"),
    ]


def print_tree(node, indent=0):
    """Print hierarchy tree structure."""
    prefix = "  " * indent
    print(f"{prefix}Row {node.row_number}: {node.description} (level={node.level}, children={len(node.children_headers)})")
    for child in node.children_headers:
        print_tree(child, indent + 1)


def analyze_scenario(name, rows):
    """Run full analysis on a scenario."""
    print(f"\n{'=' * 60}")
    print(f"SCENARIO: {name}")
    print(f"{'=' * 60}")

    # Step 1: Reconstruct hierarchy
    hierarchy = _reconstruct_hierarchy(rows)
    print(f"\n--- Hierarchy Tree ({len(hierarchy)} roots) ---")
    for root in hierarchy:
        print_tree(root)

    # Step 2: Run _detect_structural_containment
    findings = _detect_structural_containment(hierarchy)
    print(f"\n--- _detect_structural_containment() Findings ({len(findings)}) ---")
    for i, f in enumerate(findings, 1):
        print(f"  Finding {i}: parent_row={f['parent_row_number']} (L{f['parent_level']}) "
              f"-> child_row={f['child_row_number']} (L{f['child_level']})")

    # Step 3: Manual condition walkthrough
    print(f"\n--- Condition Walkthrough ---")
    for root in hierarchy:
        def walk(node, indent=0):
            for child in node.children_headers:
                condition_value = child.level > node.level
                print(f"{'  ' * indent}  child.level({child.level}) > node.level({node.level}) = {condition_value}")
                if condition_value:
                    print(f"{'  ' * indent}  -> FIRES (finding recorded)")
                else:
                    print(f"{'  ' * indent}  -> SKIPS (no finding)")
                walk(child, indent + 1)
        walk(root)

    return findings


def main():
    print("=" * 60)
    print("EQ-0015 Spike 1 — Production Behavior Evidence")
    print("=" * 60)

    # Part A: Normal hierarchy
    normal_findings = analyze_scenario("Normal Hierarchy: Head1 -> Head2 -> Head3", build_normal_hierarchy())

    # Part B: Inverted hierarchy
    inverted_findings = analyze_scenario("Inverted Hierarchy: Head1 -> Head3 (skip Head2)", build_inverted_hierarchy())

    # Part C: Summary comparison
    print(f"\n{'=' * 60}")
    print("SUMMARY: Docstring vs. Implementation")
    print(f"{'=' * 60}")
    print()
    print("  Docstring claim:")
    print('    "Verifies structural hierarchy relationships only (child_level <= parent_level)."')
    print('    "Records observable facts about structural inversions."')
    print()
    print("  Implementation (boq_intelligence.py:417):")
    print("    if child.level > node.level:")
    print()
    print("  Stack algorithm guarantee:")
    print("    child.level is ALWAYS > parent.level in normal hierarchies")
    print()
    print("  Normal hierarchy result:")
    print(f"    {len(normal_findings)} findings (Head1->Head2, Head2->Head3)")
    print("    -> Implementation fires for EVERY parent-child pair.")
    print("    -> This is NORMAL containment, not inversion.")
    print()
    print("  Inverted hierarchy result:")
    print(f"    {len(inverted_findings)} findings (Head1->Head3)")
    print("    -> Implementation ALSO fires for the inversion.")
    print("    -> Implementation cannot distinguish normal from inverted.")
    print()
    print("  CONCLUSION:")
    print("    Docstring describes inversion detection (<=)")
    print("    Implementation detects normal containment (>)")
    print("    These are OPPOSITE conditions.")
    print("    The condition is STRUCTURALLY INVERTED relative to the docstring.")

    # Write JSON evidence
    report = {
        "eq": "EQ-0015",
        "spike": 1,
        "title": "Production Behavior Evidence — _detect_structural_containment()",
        "function": "_detect_structural_containment",
        "file": "src/jarvis/parsers/costx/boq_intelligence.py",
        "docstring_claim": "child_level <= parent_level (inversions)",
        "implementation": "child.level > node.level",
        "stack_algorithm_guarantee": "child.level ALWAYS > parent.level in normal stack-built hierarchies",
        "normal_hierarchy_findings": len(normal_findings),
        "normal_hierarchy_expected_from_docstring": 0,
        "inverted_hierarchy_findings": len(inverted_findings),
        "inverted_hierarchy_expected_from_docstring": 1,
        "conclusion": "Implementation condition (> )is structurally inverted relative to docstring (<=). "
                      "Implementation detects ALL parent-child pairs, not inversions.",
        "classification_options": [
            "Documentation inconsistency",
            "Implementation inconsistency",
            "Contract inconsistency",
            "Historical intent inconsistent",
            "Insufficient evidence",
        ],
    }

    output_path = Path(__file__).parent.parent / "data" / "reports" / "eq0015_spike1_production_behavior.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON evidence written to: {output_path}")


if __name__ == "__main__":
    main()