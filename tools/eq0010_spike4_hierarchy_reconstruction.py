"""EQ-0010 Spike 4: Hierarchy Reconstruction.

Engineering Investigation — NOT production code.

This spike implements a deterministic stack-based tree reconstruction
algorithm to answer: Given a linear BOQRow sequence with Head1-5 labels,
can a unique heading tree be reconstructed deterministically?

Success Criterion: Can a deterministic stack-based algorithm reconstruct
a unique heading tree from linear BOQRow data?

Governance: Engineering_Governance.md v1.0
Fixture: tests/fixtures/costx/full_boq.xlsx
"""

import sys
import json
from pathlib import Path
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from jarvis.parsers.costx.workbook_parser import WorkbookParser
from jarvis.parsers.costx.boq_extraction import extract_boq, BOQRow

FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "costx" / "full_boq.xlsx"


def head_level(uom_str):
    """Extract numeric level from Head1-5 string."""
    if uom_str and uom_str.startswith("Head") and uom_str[4:].isdigit():
        return int(uom_str[4:])
    return None


def run_hierarchy_reconstruction():
    """Build deterministic heading tree using stack algorithm."""
    parser = WorkbookParser()
    try:
        parser.load(FIXTURE)
        parser.validate()
        workbook = parser.workbook
        rows = extract_boq(workbook)
        assert len(rows) > 0

        obs = {}

        # --- Tree Reconstruction Algorithm ---
        # Stack tracks the current path from root to current position
        # Each stack entry: {"level": int, "row_number": int, "uom": str, "description": str,
        #                    "children_headers": [], "children_items": []}
        #
        # Algorithm:
        # 1. When encountering a Head row, pop stack until top level < current head level
        # 2. Push new header onto stack as child of current top
        # 3. When encountering an Item row, add to current top's children_items
        # 4. Track root-level headers as top-level tree entries

        tree = []  # Root-level: list of header nodes
        stack = []  # Current path

        # Also track each header's assigned parent for verification
        parent_assignments = []  # Each: {header, parent_header, level}

        orphan_items = []  # Items that appear without any parent header

        for i, r in enumerate(rows):
            if r.row_type == "Head" and r.uom:
                level = head_level(r.uom)
                if level is None:
                    continue

                node = {
                    "level": level,
                    "row_number": r.row_number,
                    "uom": r.uom,
                    "description": r.description,
                    "section": r.section,
                    "children_headers": [],
                    "children_items": [],
                    "depth": 0,
                    "parent_uom": None,
                    "parent_row_number": None,
                }

                # Pop stack until top level < current level
                # (This finds the parent for this new header)
                while stack and stack[-1]["level"] >= level:
                    stack.pop()

                if stack:
                    # Parent is the current stack top
                    parent = stack[-1]
                    parent["children_headers"].append(node)
                    node["depth"] = parent["depth"] + 1
                    node["parent_uom"] = parent["uom"]
                    node["parent_row_number"] = parent["row_number"]
                else:
                    # Root-level header (no parent)
                    tree.append(node)
                    node["depth"] = 1
                    node["parent_uom"] = None
                    node["parent_row_number"] = None

                parent_assignments.append({
                    "header_uom": r.uom,
                    "header_row": r.row_number,
                    "parent_uom": node["parent_uom"],
                    "parent_row": node["parent_row_number"],
                    "depth": node["depth"],
                    "level": level,
                })

                stack.append(node)

            elif r.row_type == "Item":
                if stack:
                    stack[-1]["children_items"].append({
                        "row_number": r.row_number,
                        "code": r.code,
                        "description": r.description,
                        "quantity": r.quantity,
                        "uom": r.uom,
                    })
                else:
                    # Item without any parent header — orphan
                    orphan_items.append({
                        "row_number": r.row_number,
                        "description": r.description,
                    })

        # --- Analysis ---

        # 1. Tree size and structure
        obs["total_headers_placed"] = len(parent_assignments)
        obs["tree_root_headers"] = len(tree)
        obs["orphan_items_found"] = len(orphan_items)

        # 2. Depth analysis
        depths = defaultdict(int)
        for pa in parent_assignments:
            depths[pa["depth"]] += 1
        obs["depth_distribution"] = dict(sorted(depths.items()))

        # 3. Level vs depth analysis (does Head N always map to depth N?)
        level_vs_depth = Counter()
        for pa in parent_assignments:
            combo = (pa["level"], pa["depth"])
            level_vs_depth[combo] += 1
        obs["level_vs_depth_cross"] = {
            f"L{l}_D{d}": c for (l, d), c in sorted(level_vs_depth.items())
        }

        # 4. Unique parent-child mappings
        parent_child_maps = defaultdict(set)
        for pa in parent_assignments:
            if pa["parent_uom"]:
                parent_child_maps[pa["parent_uom"]].add(pa["header_uom"])
        obs["parent_child_mappings"] = {
            uom: sorted(children)
            for uom, children in sorted(parent_child_maps.items())
        }

        # 5. Root-level header distribution
        root_levels = defaultdict(int)
        for t in tree:
            root_levels[t["uom"]] += 1
        obs["root_header_uom_distribution"] = dict(sorted(root_levels.items()))

        # 6. Tree uniqueness check
        # Count how many distinct tree shapes exist at root level
        tree_shapes = set()
        for t in tree:
            # Shape = (uom, number of direct children, number of items)
            shape = (t["uom"], len(t["children_headers"]), len(t["children_items"]))
            tree_shapes.add(shape)
        obs["distinct_tree_shapes"] = len(tree_shapes)

        # 7. Parent assignment determinism
        # The algorithm must produce the SAME tree every time
        # This is verified by the outer determinism check

        # 8. Items per tree node
        items_per_node = defaultdict(lambda: {"count": 0, "nodes": 0})
        for pa in parent_assignments:
            items_per_node[pa["header_uom"]]["nodes"] += 1
            # Count items under this header (not recursively — just immediate)
        # Better: count items per header from the tree
        def count_immediate_items(node):
            return len(node["children_items"])

        item_counts = defaultdict(list)
        for t in tree:
            stack2 = [t]
            while stack2:
                n = stack2.pop()
                item_counts[n["uom"]].append({
                    "header": n["uom"],
                    "description": n["description"],
                    "immediate_items": len(n["children_items"]),
                    "total_child_headers": len(n["children_headers"]),
                })
                for child in n["children_headers"]:
                    stack2.append(child)
        obs["header_item_summary"] = {
            uom: {
                "total_headers": len(entries),
                "total_immediate_items": sum(e["immediate_items"] for e in entries),
                "avg_immediate_items": round(
                    sum(e["immediate_items"] for e in entries) / len(entries), 2
                ),
            }
            for uom, entries in sorted(item_counts.items())
        }

        # 9. Empty headers (from reconstructed tree)
        empty_header_count = 0
        def count_empty(node):
            nonlocal empty_header_count
            if len(node["children_items"]) == 0 and len(node["children_headers"]) == 0:
                empty_header_count += 1
            for child in node["children_headers"]:
                count_empty(child)
        root_empty_count = 0
        for t in tree:
            if len(t["children_items"]) == 0 and len(t["children_headers"]) == 0:
                root_empty_count += 1
            for child in t["children_headers"]:
                count_empty(child)
        obs["empty_headers_from_tree"] = {
            "root_empty": root_empty_count,
            "nested_empty": empty_header_count,
            "total_empty": root_empty_count + empty_header_count,
        }

        return obs
    finally:
        parser.close()


def main():
    print("=" * 70)
    print("EQ-0010 SPIKE 4: HIERARCHY RECONSTRUCTION")
    print("=" * 70)
    print()
    print(f"Fixture: {FIXTURE}")
    print(f"Fixture exists: {FIXTURE.exists()}")
    print()

    print("--- RUN 1 ---")
    run1 = run_hierarchy_reconstruction()
    print(json.dumps(run1, indent=2, default=str))
    print()

    print("--- RUN 2 ---")
    run2 = run_hierarchy_reconstruction()
    print(json.dumps(run2, indent=2, default=str))
    print()

    print("--- DETERMINISM CHECK ---")
    match = json.dumps(run1, sort_keys=True, default=str) == json.dumps(run2, sort_keys=True, default=str)
    print(f"Run 1 == Run 2: {match}")
    print()

    if not match:
        print("DIFFERENCES:")
        for key in set(list(run1.keys()) + list(run2.keys())):
            v1 = json.dumps(run1.get(key), sort_keys=True, default=str)
            v2 = json.dumps(run2.get(key), sort_keys=True, default=str)
            if v1 != v2:
                print(f"  {key}:")
                print(f"    Run 1: {v1}")
                print(f"    Run 2: {v2}")

    print()
    print("=" * 70)
    print("SPIKE 4 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()