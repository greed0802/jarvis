#!/usr/bin/env python3
"""
Semantic Pattern Analysis Tool — EQ-0018 BOQ Semantic Intelligence.

Extracts observable semantic patterns from CostX BOQ fixtures.
Reports evidence only — no inference, no classification.

Usage:
    ./.venv/bin/python tools/semantic_pattern_analysis.py
    ./.venv/bin/python tools/semantic_pattern_analysis.py --fixture full_boq.xlsx
    ./.venv/bin/python tools/semantic_pattern_analysis.py --all
    ./.venv/bin/python tools/semantic_pattern_analysis.py --fixture Base_Structural_CostX.xlsx --verbose
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import openpyxl

FIXTURE_DIR = Path("tests/fixtures/costx")


# ---------------------------------------------------------------------------
# CostX named style patch (same as workbook_inspector)
# ---------------------------------------------------------------------------

from openpyxl.styles.named_styles import _NamedCellStyle

_NAMED_PATCH = False


def _patch_named_style():
    global _NAMED_PATCH
    if _NAMED_PATCH:
        return
    orig = _NamedCellStyle.__init__

    def patched(self, name=None, **kw):
        if name is None:
            name = ""
        orig(self, name=name, **kw)

    _NamedCellStyle.__init__ = patched
    _NAMED_PATCH = True


def load_workbook(path):
    _patch_named_style()
    return openpyxl.load_workbook(path, data_only=True)


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

HEADER_LABELS = {"Head1", "Head2", "Head3", "Head4", "Head5"}
NOTE_LABEL = "Note"
SECTION_LABELS = HEADER_LABELS | {NOTE_LABEL}

# Known Head1-level pattern labels (section codes like A, B, C, D...)
SECTION_CODES_PATTERN = r"^[A-Z]$"


def extract_rows(ws) -> list[dict]:
    """Extract all rows with observable structure."""
    rows = []
    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=False):
        cells = {}
        for cell in row:
            # Handle MergedCell objects (CostX uses merged cells for title rows)
            try:
                col_letter = cell.column_letter
            except AttributeError:
                col_letter = ""
            cells[cell.column] = {
                "value": cell.value,
                "type": getattr(cell, "data_type", None),
                "col_letter": col_letter,
            }
        rows.append(cells)
    return rows


def parse_boq_structure(ws) -> dict:
    """
    Parse the CostX BOQ structure from the worksheet.
    Returns structured representation of hierarchy.
    """
    rows = extract_rows(ws)

    structure = {
        "sections": [],  # Top-level sections (A, B, C...)
        "hierarchy_labels": defaultdict(list),  # Head1, Head2, etc.
        "items": [],  # Measured items
        "notes": [],  # Notes
        "headers": [],  # All header rows
        "totals": [],  # Total/subtotal rows
    }

    current_section = None
    current_path = []  # Stack of current hierarchy

    for row_idx, cells in enumerate(rows):
        # Get cell values by column
        b_val = cells.get(2, {}).get("value", "")  # Column B = Description
        d_val = cells.get(4, {}).get("value", "")  # Column D = Hierarchy label
        a_val = cells.get(1, {}).get("value", "")  # Column A = Code
        c_val = cells.get(3, {}).get("value", None)  # Column C = Quantity
        d_uom = cells.get(4, {}).get("value", "")  # Column D = also UOM

        # Skip totally empty rows
        if not any(c.get("value") for c in cells.values()):
            continue

        # Detect section breaks (bold, single-letter codes like A, B, C)
        if a_val and isinstance(a_val, str) and len(a_val.strip()) == 1 and a_val.strip().isalpha():
            if b_val:
                section_name = str(b_val).strip()
                current_section = {
                    "code": a_val.strip(),
                    "name": section_name,
                    "start_row": row_idx + 1,
                }
                structure["sections"].append(current_section)
                structure["headers"].append({
                    "row": row_idx + 1,
                    "type": "section",
                    "code": a_val.strip(),
                    "text": str(b_val).strip(),
                    "bold": _is_bold(cells),
                })

        # Detect hierarchy labels from column D
        d_text = str(d_val).strip() if d_val else ""
        if d_text in HEADER_LABELS:
            structure["hierarchy_labels"][d_text].append({
                "row": row_idx + 1,
                "text": str(b_val).strip() if b_val else "",
                "code": str(a_val).strip() if a_val else "",
            })
            structure["headers"].append({
                "row": row_idx + 1,
                "type": d_text,
                "text": str(b_val).strip() if b_val else "",
                "code": str(a_val).strip() if a_val else "",
            })

        # Detect notes
        if d_text == NOTE_LABEL:
            structure["notes"].append({
                "row": row_idx + 1,
                "text": str(b_val).strip() if b_val else "",
                "code": str(a_val).strip() if a_val else "",
            })

        # Detect measured items (have quantity in C column)
        if c_val is not None and d_text not in SECTION_LABELS:
            structure["items"].append({
                "row": row_idx + 1,
                "code": str(a_val).strip() if a_val else "",
                "description": str(b_val).strip() if b_val else "",
                "quantity": c_val,
                "uom": d_uom.strip() if isinstance(d_uom, str) else "",
            })

        # Detect total rows
        if b_val and isinstance(b_val, str) and "TOTAL" in str(b_val).upper():
            structure["totals"].append({
                "row": row_idx + 1,
                "text": str(b_val).strip(),
                "bold": _is_bold(cells),
            })

    return structure


def _is_bold(cells: dict) -> bool:
    """Check if any cell in row has bold font."""
    for c in cells.values():
        cell_obj = c.get("_cell")
        if cell_obj and cell_obj.font and cell_obj.font.bold:
            return True
    return False


# ---------------------------------------------------------------------------
# Pattern extraction
# ---------------------------------------------------------------------------


def extract_naming_conventions(items: list) -> dict:
    """Extract naming conventions from items."""
    words = Counter()
    prefixes = Counter()
    patterns = Counter()

    for item in items:
        desc = item.get("description", "")
        words.update(w.strip(".,;:()") for w in desc.split() if len(w) > 2)

        # Extract prefix patterns (first 1-3 words)
        parts = desc.split()
        if parts:
            prefixes[parts[0]] += 1
        if len(parts) >= 2:
            patterns[f"{parts[0]} {parts[1]}"] += 1

    return {
        "common_words": words.most_common(50),
        "common_prefixes": prefixes.most_common(30),
        "common_phrases": patterns.most_common(30),
    }


def extract_uom_patterns(items: list) -> dict:
    """Extract UOM patterns."""
    uom_counts = Counter()
    uom_by_section = defaultdict(Counter)

    for item in items:
        uom_counts[item["uom"]] += 1

    return {
        "uom_frequencies": uom_counts.most_common(20),
    }


def extract_vocabulary(items: list) -> dict:
    """Extract recurring engineering vocabulary."""
    # Key engineering terms to track
    engineering_terms = [
        "Concrete", "Excavation", "Footing", "Column", "Slab",
        "Reinforcement", "Formwork", "Waterproofing", "Backfill",
        "Pile", "Drainage", "Masonry", "Blockwork", "Brickwork",
        "Steel", "Timber", "Roofing", "Plaster", "Render",
        "Tiling", "Painting", "Joinery", "Carpentry", "FFE",
        "Aluminium", "Glazing", "Hydraulic", "Mechanical",
        "Electrical", "Fire", "Insulation", "Waterproofing",
        "Damp", "Membrane", "Sealant", "Grout", "Mortar",
        "Fabric", "Mesh", "Bar", "Strand", "Cable",
        "Soffit", "Beam", "Wall", "Floor", "Ceiling",
        "Stair", "Ramp", "Kerb", "Path", "Road",
        "Duct", "Pipe", "Cable", "Tray", "Lining",
        "Primer", "Sealer", "Coating", "Finish",
        "Allow", "Provisional", "Prime", "Cost",
        "Preliminary", "Site", "Establishment",
    ]

    term_counts = defaultdict(lambda: {"count": 0, "contexts": []})

    for item in items:
        desc = item.get("description", "")
        desc_lower = desc.lower()
        for term in engineering_terms:
            if term.lower() in desc_lower:
                term_counts[term]["count"] += 1
                if len(term_counts[term]["contexts"]) < 5:
                    term_counts[term]["contexts"].append(desc[:100])

    return {
        "vocabulary": {k: v for k, v in sorted(term_counts.items(), key=lambda x: -x[1]["count"])},
    }


def extract_hierarchy_patterns(headers: list) -> dict:
    """Extract hierarchy patterns."""
    head1_texts = []
    head2_texts = []
    head3_texts = []
    head4_texts = []

    for h in headers:
        if h["type"] == "Head1":
            head1_texts.append(h["text"])
        elif h["type"] == "Head2":
            head2_texts.append(h["text"])
        elif h["type"] == "Head3":
            head3_texts.append(h["text"])
        elif h["type"] == "Head4":
            head4_texts.append(h["text"])

    # Detect semantic categories for Head1
    head1_categories = Counter()
    for t in head1_texts:
        t_upper = t.upper()
        # Detect trade sections
        if any(x in t_upper for x in ["DEMOLITION", "SITE PREP", "EARTHWORK", "CIVIL"]):
            head1_categories["Site Works"] += 1
        elif any(x in t_upper for x in ["STRUCTURAL", "CONCRETE", "FORMWORK", "REINFORCEMENT", "STEEL"]):
            head1_categories["Structural"] += 1
        elif any(x in t_upper for x in ["CEILING", "FLOOR", "WALL", "ROOFING", "CLADDING"]):
            head1_categories["Envelope/Finishes"] += 1
        elif any(x in t_upper for x in ["DOOR", "WINDOW", "GLAZING"]):
            head1_categories["Openings"] += 1
        elif any(x in t_upper for x in ["PAINTING", "TILING", "JOINERY", "FFE", "SIGNAGE"]):
            head1_categories["Fit-out"] += 1
        elif any(x in t_upper for x in ["HYDRAULIC", "FIRE", "MECHANICAL", "ELECTRICAL"]):
            head1_categories["Services"] += 1
        elif any(x in t_upper for x in ["LANDSCAPE", "EXTERNAL"]):
            head1_categories["External Works"] += 1
        elif any(x in t_upper for x in ["PRELIMINARY", "GFA", "MAIN WORKS"]):
            head1_categories["Preliminaries/General"] += 1
        elif any(x in t_upper for x in ["PROVISIONAL", "PRIME COST"]):
            head1_categories["Provisional Sums"] += 1
        else:
            head1_categories["Other"] += 1

    return {
        "head1_count": len(head1_texts),
        "head2_count": len(head2_texts),
        "head3_count": len(head3_texts),
        "head4_count": len(head4_texts),
        "head1_texts": head1_texts[:30],
        "head2_texts": head2_texts[:30],
        "head3_texts": head3_texts[:30],
        "head4_texts": head4_texts[:30],
        "head1_semantic_categories": dict(head1_categories.most_common()),
    }


# ---------------------------------------------------------------------------
# Trade-specific fixture analysis
# ---------------------------------------------------------------------------

TRADE_FIXTURES = {
    "Base_Structural_CostX.xlsX": "Structural",
    "Base_Structural_Steel_CostX.xlsX": "Structural Steel",
    "Base_Roofing_CostX.xlsX": "Roofing",
    "Base_Ceiling_BOQ_CostX.xlsX": "Ceiling",
    "Base_Demolition_CostX.xlsX": "Demolition",
    "Base_Doors_and_Windows_CostX.xlsX": "Doors and Windows",
    "Base_External Wall Finishes_CostX.xlsX": "External Wall Finishes",
    "Base_Floor_Finishes_CostX.xlsX": "Floor Finishes",
    "Base_Interior_Wall_Finishes_CostX.xlsX": "Interior Wall Finishes",
    "Base_Joinery_CostX.xlsX": "Joinery",
    "Base_Landscape_CostX.xlsX": "Landscape",
    "Base_Metal Works_CostX.xlsX": "Metal Works",
    "Base_Signage_CostX.xlsX": "Signage",
    "Base_Site Preparation_Civil_Earthworks_and_Demolition_CostX.xlsX": "Site Preparation",
    "Base_FFE_CostX.xlsX": "FFE",
    "Base_Wall_Types_CostX.xlsX": "Wall Types",
}


def analyze_all_fixtures(verbose: bool = False) -> dict:
    """Analyze all CostX fixtures."""
    results = {}

    for filename, trade in sorted(TRADE_FIXTURES.items()):
        path = FIXTURE_DIR / filename
        if not path.exists():
            print(f"[WARNING] Fixture not found: {path}")
            continue

        try:
            wb = load_workbook(str(path))
            ws = wb.active
            structure = parse_boq_structure(ws)
            results[trade] = structure
            if verbose:
                print(f"\n{'='*60}")
                print(f"[ANALYSIS] {trade} ({filename})")
                print(f"{'='*60}")
                print(f"  Sections: {len(structure['sections'])}")
                print(f"  Head1 count: {sum(1 for h in structure['headers'] if h['type'] == 'Head1')}")
                print(f"  Head2 count: {sum(1 for h in structure['headers'] if h['type'] == 'Head2')}")
                print(f"  Head3 count: {sum(1 for h in structure['headers'] if h['type'] == 'Head3')}")
                print(f"  Head4 count: {sum(1 for h in structure['headers'] if h['type'] == 'Head4')}")
                print(f"  Items: {len(structure['items'])}")
                print(f"  Notes: {len(structure['notes'])}")
            wb.close()
        except Exception as e:
            print(f"[ERROR] Failed to analyze {filename}: {e}")

    return results


# ---------------------------------------------------------------------------
# Main analysis — full_boq
# ---------------------------------------------------------------------------


def analyze_full_boq(verbose: bool = False) -> dict:
    """Comprehensive analysis of the main full BOQ fixture."""
    path = FIXTURE_DIR / "full_boq.xlsx"
    if not path.exists():
        print(f"[ERROR] Full BOQ fixture not found: {path}")
        return {}

    wb = load_workbook(str(path))
    ws = wb.active
    structure = parse_boq_structure(ws)

    # Naming conventions
    naming = extract_naming_conventions(structure["items"])

    # UOM patterns
    uom = extract_uom_patterns(structure["items"])

    # Vocabulary
    vocab = extract_vocabulary(structure["items"])

    # Hierarchy patterns
    hierarchy = extract_hierarchy_patterns(structure["headers"])

    # Section breakdown
    section_summary = []
    for s in structure["sections"]:
        section_summary.append({
            "code": s["code"],
            "name": s["name"],
        })

    result = {
        "filename": "full_boq.xlsx",
        "total_items": len(structure["items"]),
        "total_notes": len(structure["notes"]),
        "total_headers": len(structure["headers"]),
        "sections": section_summary,
        "hierarchy": hierarchy,
        "naming_conventions": naming,
        "uom_patterns": uom,
        "vocabulary": vocab,
    }

    if verbose:
        print(f"\n{'='*60}")
        print(f"FULL BOQ ANALYSIS")
        print(f"{'='*60}")
        print(f"Total items: {result['total_items']}")
        print(f"Total notes: {result['total_notes']}")
        print(f"Total headers: {result['total_headers']}")
        print(f"\nSections:")
        for s in section_summary:
            print(f"  {s['code']}: {s['name']}")
        print(f"\nHierarchy:")
        print(f"  Head1: {hierarchy['head1_count']}")
        print(f"  Head2: {hierarchy['head2_count']}")
        print(f"  Head3: {hierarchy['head3_count']}")
        print(f"  Head4: {hierarchy['head4_count']}")
        print(f"\nUOM Patterns:")
        for uom_name, count in uom["uom_frequencies"][:15]:
            print(f"  {uom_name}: {count}")
        print(f"\nTop Vocabulary:")
        for term, data in list(vocab["vocabulary"].items())[:30]:
            print(f"  {term}: {data['count']} occurrences")

    wb.close()
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Semantic Pattern Analysis — EQ-0018")
    parser.add_argument("--fixture", help="Analyze a specific fixture file")
    parser.add_argument("--all", action="store_true", help="Analyze all trade-specific fixtures")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.all:
        results = analyze_all_fixtures(verbose=args.verbose)
        if args.json:
            print(json.dumps(results, indent=2, default=str))
    elif args.fixture:
        # Analyze specific fixture
        path = FIXTURE_DIR / args.fixture
        if not path.exists():
            print(f"[ERROR] File not found: {path}")
            return 1
        wb = load_workbook(str(path))
        ws = wb.active
        structure = parse_boq_structure(ws)
        hierarchy = extract_hierarchy_patterns(structure["headers"])
        naming = extract_naming_conventions(structure["items"])
        uom = extract_uom_patterns(structure["items"])
        vocab = extract_vocabulary(structure["items"])
        result = {
            "filename": args.fixture,
            "total_items": len(structure["items"]),
            "hierarchy": hierarchy,
            "naming_conventions": naming,
            "uom_patterns": uom,
            "vocabulary": vocab,
        }
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(f"\n{'='*60}")
            print(f"ANALYSIS: {args.fixture}")
            print(f"{'='*60}")
            print(f"Total items: {result['total_items']}")
            print(f"Head1 count: {hierarchy['head1_count']}")
            print(f"Head2 count: {hierarchy['head2_count']}")
            print(f"Head3 count: {hierarchy['head3_count']}")
            print(f"Head4 count: {hierarchy['head4_count']}")
            if hierarchy['head1_texts']:
                print(f"\nHead1 texts:")
                for t in hierarchy['head1_texts']:
                    print(f"  {t}")
        wb.close()
    else:
        # Default: analyze full BOQ
        result = analyze_full_boq(verbose=args.verbose)
        if args.json:
            print(json.dumps(result, indent=2, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())