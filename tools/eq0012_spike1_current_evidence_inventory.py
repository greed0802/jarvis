#!/usr/bin/env python3
"""EQ-0012 Spike 1: Current Evidence Inventory

Systematic inventory of all evidence fields produced by BOQ Intelligence
(Increments 1-3), documenting types, semantics, and traceability to
engineering evidence.

Authority:
- EQ-0012 BOQ Intelligence Public Evidence Contract
- Engineering_Governance.md v1.0
"""

from dataclasses import dataclass
import json
from pathlib import Path

@dataclass(frozen=True)
class EvidenceField:
    """Documentation of a single evidence field in BOQ Intelligence."""
    
    field_name: str
    increment: int  # Which increment introduced this field (1, 2, or 3)
    python_type: str  # Python type annotation
    required: bool  # Always present vs. optional (None allowed)
    semantics: str  # What this field represents
    traceability: str  # Which EQ/Spike established this evidence
    stability: str  # "Stable" | "Potentially Unstable" | "Unknown"
    notes: str  # Additional observations

def inventory_increment_1_fields() -> list[EvidenceField]:
    """Inventory Increment 1: Observation Evidence."""
    return [
        EvidenceField(
            field_name="row_classification",
            increment=1,
            python_type="dict[str, int]",
            required=True,
            semantics="Count of rows by type (Head, Note, Section, Item, Other). Deterministic row type classification from BOQRow.row_type field.",
            traceability="EQ-0007 Production Extraction Report, EQ-0009 Context Discovery Report. Row types defined in boq_extraction.py.",
            stability="Stable",
            notes="Frozen structure. Keys: {'Head', 'Note', 'Section', 'Item', 'Other'}. Values: non-negative integers. Sum equals total row count."
        ),
        EvidenceField(
            field_name="section_statistics",
            increment=1,
            python_type="dict[str, dict[str, int]]",
            required=True,
            semantics="Per-section quantity distribution. Outer key: section name. Inner keys: 'negative_qty' (count of rows with quantity < 0), 'positive_qty' (count of rows with quantity > 0).",
            traceability="EQ-0009 Context Discovery Report. Section-based analysis of quantity patterns.",
            stability="Stable",
            notes="Sorted by section name. Only sections with quantities are included. Inner dict always has both 'negative_qty' and 'positive_qty' keys."
        ),
        EvidenceField(
            field_name="boq_statistics",
            increment=1,
            python_type="dict[str, int | float]",
            required=True,
            semantics="BOQ-wide statistics: total_rows, code_rows, description_rows, quantity_rows, uom_rows, section_rows. Count of rows where each field is non-None.",
            traceability="EQ-0007 Production Extraction Report. Field presence analysis.",
            stability="Stable",
            notes="Fixed keys: {'total_rows', 'code_rows', 'description_rows', 'quantity_rows', 'uom_rows', 'section_rows'}. All values are non-negative integers."
        ),
        EvidenceField(
            field_name="known_anomalies",
            increment=1,
            python_type="list[dict[str, int | str | float]]",
            required=True,
            semantics="Identity-level anomalies detected through deterministic rules. Currently: OMISSION section items with positive quantity (expected negative).",
            traceability="EQ-0009 Context Discovery Report. Omission/Addition domain rules.",
            stability="Stable",
            notes="Each anomaly dict contains: {'row_number': int, 'code': str | None, 'quantity': float, 'section': str}. Sorted by row_number."
        ),
    ]

def inventory_increment_2_fields() -> list[EvidenceField]:
    """Inventory Increment 2: Hierarchy Evidence."""
    return [
        EvidenceField(
            field_name="hierarchy",
            increment=2,
            python_type="tuple[BOQHeaderNode, ...] | None",
            required=False,
            semantics="Reconstructed BOQ heading tree. Root-level headers (Head1 nodes) with recursive children. None if include_hierarchy=False.",
            traceability="EQ-0010 Spike 4: Hierarchy Reconstruction. Stack-based deterministic algorithm.",
            stability="Stable",
            notes="BOQHeaderNode is frozen dataclass with fields: level, row_number, uom, description, section, depth, parent_row_number, children_headers, children_items. Tree structure reflects Head1-5 nesting."
        ),
        EvidenceField(
            field_name="hierarchy_statistics",
            increment=2,
            python_type="dict[str, int | float] | None",
            required=False,
            semantics="Statistics derived from reconstructed hierarchy: total_headers, total_items, max_depth, headers_by_level, root_count.",
            traceability="EQ-0010 Spike 4: Hierarchy reconstruction statistics.",
            stability="Stable",
            notes="None if include_hierarchy=False. Keys: {'total_headers', 'total_items', 'max_depth', 'headers_by_level', 'root_count'}. headers_by_level is nested dict."
        ),
    ]

def inventory_increment_3_fields() -> list[EvidenceField]:
    """Inventory Increment 3: Detection Evidence."""
    return [
        EvidenceField(
            field_name="detected_level_skips",
            increment=3,
            python_type="tuple[dict[str, int], ...] | None",
            required=False,
            semantics="Level progression skips detected in hierarchy. Records parent→child transitions where child_level - parent_level > 1 (e.g., Head1→Head3).",
            traceability="EQ-0010 Spike 3: Row Sequence Analysis. EQ-0011 Spike 2: Evidence vs Assessment Decomposition (detection only, not legitimacy).",
            stability="Stable",
            notes="None if include_detection=False. Each dict: {'parent_row': int, 'child_row': int, 'parent_level': int, 'child_level': int, 'skip': int}. No assessment of legitimacy."
        ),
        EvidenceField(
            field_name="zero_quantity_items",
            increment=3,
            python_type="tuple[dict[str, int | str | float | None], ...] | None",
            required=False,
            semantics="Items with quantity exactly equal to 0.0. Detection only, no assessment of acceptability.",
            traceability="EQ-0010 Spike 1: Direct Field Observation. EQ-0011 Spike 2: Evidence vs Assessment Decomposition (detection only).",
            stability="Stable",
            notes="None if include_detection=False. Each dict: {'row_number': int, 'code': str | None, 'description': str | None, 'quantity': float, 'uom': str | None, 'section': str | None}."
        ),
        EvidenceField(
            field_name="structural_containment_findings",
            increment=3,
            python_type="tuple[dict[str, int], ...] | None",
            required=False,
            semantics="Structural parent-child level consistency. Reports cases where child header level exceeds parent level (e.g., Head3 under Head2 but child is Head4).",
            traceability="EQ-0010 Spike 4: Hierarchy Reconstruction. EQ-0011 Spike 3: Boundary Validation (structural only, not semantic).",
            stability="Stable",
            notes="None if include_detection=False. Each dict: {'parent_row': int, 'child_row': int, 'parent_level': int, 'child_level': int}. Structural containment only."
        ),
        EvidenceField(
            field_name="completeness_findings",
            increment=3,
            python_type="tuple[dict[str, int | str], ...] | None",
            required=False,
            semantics="Basic completeness: sections that lack measurable items (quantity field present). Detection only, does not assess whether this is acceptable.",
            traceability="EQ-0010 Spike 3: Row Sequence Analysis. EQ-0011 Spike 3: Boundary Validation (basic structural, not project scope).",
            stability="Stable",
            notes="None if include_detection=False. Each dict: {'section': str, 'total_rows': int, 'item_count': int}. item_count=0 indicates no measurable items."
        ),
    ]

def analyze_field_stability():
    """Analyze which fields must remain stable across contract versions."""
    
    increment_1 = inventory_increment_1_fields()
    increment_2 = inventory_increment_2_fields()
    increment_3 = inventory_increment_3_fields()
    
    all_fields = increment_1 + increment_2 + increment_3
    
    print("=" * 80)
    print("EQ-0012 SPIKE 1: CURRENT EVIDENCE INVENTORY")
    print("=" * 80)
    print()
    
    print("EVIDENCE FIELD INVENTORY")
    print("-" * 80)
    print()
    
    for increment_num, fields in [(1, increment_1), (2, increment_2), (3, increment_3)]:
        print(f"\n### INCREMENT {increment_num} FIELDS ###\n")
        for field in fields:
            print(f"Field: {field.field_name}")
            print(f"  Type: {field.python_type}")
            print(f"  Required: {'Yes' if field.required else 'No (opt-in)'}")
            print(f"  Semantics: {field.semantics}")
            print(f"  Traceability: {field.traceability}")
            print(f"  Stability: {field.stability}")
            print(f"  Notes: {field.notes}")
            print()
    
    print("\n" + "=" * 80)
    print("STABILITY ANALYSIS")
    print("=" * 80)
    print()
    
    required_fields = [f for f in all_fields if f.required]
    optional_fields = [f for f in all_fields if not f.required]
    
    print(f"Required Fields (always present): {len(required_fields)}")
    for f in required_fields:
        print(f"  - {f.field_name} (Increment {f.increment})")
    
    print(f"\nOptional Fields (opt-in via parameters): {len(optional_fields)}")
    for f in optional_fields:
        print(f"  - {f.field_name} (Increment {f.increment})")
    
    print("\n" + "=" * 80)
    print("TRACEABILITY MAP")
    print("=" * 80)
    print()
    
    print("All fields trace to frozen engineering evidence:")
    print()
    
    by_source = {}
    for field in all_fields:
        sources = field.traceability.split(". ")[0]  # First sentence
        if sources not in by_source:
            by_source[sources] = []
        by_source[sources].append(field.field_name)
    
    for source, fields in sorted(by_source.items()):
        print(f"{source}:")
        for f in fields:
            print(f"  - {f}")
        print()
    
    print("=" * 80)
    print("FIELD STABILITY CLASSIFICATION")
    print("=" * 80)
    print()
    
    print("STABLE FIELDS (must not change):")
    stable = [f for f in all_fields if f.stability == "Stable"]
    print(f"  Count: {len(stable)}/{len(all_fields)}")
    for f in stable:
        print(f"  - {f.field_name}")
    
    print()
    print("OBSERVATION:")
    print("  All 10 evidence fields are classified as Stable.")
    print("  This reflects:")
    print("    1. All fields trace to frozen engineering evidence (EQ-0007, EQ-0009, EQ-0010, EQ-0011)")
    print("    2. All fields implement approved capabilities")
    print("    3. All fields have passed production validation")
    print("    4. No speculative or experimental fields exist")
    print()
    print("  Stability Assessment: HIGH")
    print("  Contract Version: Should begin at v1.0 (no alpha/beta needed)")
    
    return {
        "increment_1": [vars(f) for f in increment_1],
        "increment_2": [vars(f) for f in increment_2],
        "increment_3": [vars(f) for f in increment_3],
        "total_fields": len(all_fields),
        "required_fields": len(required_fields),
        "optional_fields": len(optional_fields),
        "stable_fields": len(stable),
    }

def export_inventory(data: dict, output_path: Path):
    """Export inventory to JSON for reference."""
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\n✓ Inventory exported to: {output_path}")

def main():
    """Execute Spike 1: Current Evidence Inventory."""
    
    # Analyze all evidence fields
    inventory_data = analyze_field_stability()
    
    # Export for reference
    output_dir = Path("data/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    export_inventory(inventory_data, output_dir / "eq0012_spike1_evidence_inventory.json")
    
    print("\n" + "=" * 80)
    print("SPIKE 1 COMPLETE")
    print("=" * 80)
    print()
    print("Next Steps:")
    print("  1. Review inventory findings")
    print("  2. Create Spike 1 Evidence Report")
    print("  3. Proceed to Spike 2: Contract Structure & Versioning Policy")

if __name__ == "__main__":
    main()