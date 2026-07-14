"""EQ-0010 Spike 2: UOM Pattern Analysis.

Engineering Investigation — NOT production code.

This spike investigates whether the observed UOM string patterns (Head1-5)
can be deterministically interpreted as structural hierarchy using only
production evidence.

Question: Can UOM string patterns be deterministically interpreted as
structural hierarchy, or do they remain observational labels?

Governance: Engineering_Governance.md v1.0
Fixture: tests/fixtures/costx/full_boq.xlsx
"""

import sys
import json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from jarvis.parsers.costx.workbook_parser import WorkbookParser
from jarvis.parsers.costx.boq_extraction import extract_boq, BOQRow

FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "costx" / "full_boq.xlsx"


def run_uom_analysis():
    """Execute production pipeline and produce UOM pattern observations."""
    parser = WorkbookParser()
    try:
        parser.load(FIXTURE)
        parser.validate()
        workbook = parser.workbook
        rows = extract_boq(workbook)

        assert len(rows) > 0, "Must extract at least one row"

        obs = {}

        # --- 1. Head UOM sequence patterns ---
        head_sequence = []
        for i, r in enumerate(rows):
            if r.row_type == "Head" and r.uom:
                head_sequence.append({
                    "index": i,
                    "row_number": r.row_number,
                    "uom": r.uom,
                    "description": r.description,
                    "section": r.section if r.section else "(none)",
                })
        obs["head_row_count"] = len(head_sequence)
        obs["head_uom_distribution"] = dict(sorted(
            Counter(h["uom"] for h in head_sequence).items()
        ))

        # --- 2. UOM transition patterns (what follows what) ---
        uom_transitions = Counter()
        for i in range(len(rows) - 1):
            uom_a = rows[i].uom if rows[i].uom else "(none)"
            uom_b = rows[i + 1].uom if rows[i + 1].uom else "(none)"
            uom_transitions[(uom_a, uom_b)] += 1
        obs["uom_transition_count"] = len(uom_transitions)
        obs["uom_top_transitions"] = [
            {"from": k[0], "to": k[1], "count": v}
            for k, v in uom_transitions.most_common(30)
        ]

        # --- 3. Head-to-Item relationships ---
        head_item_distances = []
        for i, r in enumerate(rows):
            if r.row_type != "Head":
                continue
            item_count = 0
            for j in range(i + 1, len(rows)):
                if rows[j].row_type == "Head":
                    break
                if rows[j].row_type == "Item":
                    item_count += 1
                if rows[j].row_type == "Section":
                    break
            head_item_distances.append({
                "row_number": r.row_number,
                "uom": r.uom,
                "description": r.description,
                "items_following": item_count,
            })
        obs["head_item_distance_count"] = len(head_item_distances)
        obs["head_items_following_distribution"] = dict(
            sorted(Counter(h["items_following"] for h in head_item_distances).items())
        )
        empty_headers = [h for h in head_item_distances if h["items_following"] == 0]
        obs["empty_header_count"] = len(empty_headers)
        obs["empty_headers_by_uom"] = dict(
            sorted(Counter(h["uom"] for h in empty_headers).items())
        )

        # --- 4. Head level progression ---
        progression_patterns = Counter()
        for i in range(len(head_sequence) - 1):
            current = head_sequence[i]["uom"]
            next_uom = head_sequence[i + 1]["uom"]
            progression_patterns[(current, next_uom)] += 1
        obs["head_progression_patterns"] = [
            {"from": k[0], "to": k[1], "count": v}
            for k, v in sorted(progression_patterns.items(), key=lambda x: -x[1])
        ]

        # --- 5. Head5 analysis ---
        head5_rows = [h for h in head_sequence if h["uom"] == "Head5"]
        head5_by_section = Counter(h["section"] for h in head5_rows)
        obs["head5_count"] = len(head5_rows)
        obs["head5_by_section"] = dict(sorted(head5_by_section.items()))

        # --- 6. Head sequence by section ---
        head_by_section = {}
        for section_label in ["OMISSION", "ADDITION", "(none)"]:
            seq = [h for h in head_sequence if h["section"] == section_label]
            if seq:
                head_by_section[section_label] = dict(
                    sorted(Counter(h["uom"] for h in seq).items())
                )
            else:
                head_by_section[section_label] = {}
        obs["head_uom_by_section"] = head_by_section

        # --- 7. Head5 context ---
        head5_followed_by = Counter()
        for h in head_sequence:
            if h["uom"] != "Head5":
                continue
            idx = h["index"]
            if idx + 1 < len(rows):
                head5_followed_by[rows[idx + 1].row_type] += 1
        obs["head5_followed_by"] = dict(sorted(head5_followed_by.items()))

        # --- 8. Head1 context ---
        head1_followed_by = Counter()
        for h in head_sequence:
            if h["uom"] != "Head1":
                continue
            idx = h["index"]
            if idx + 1 < len(rows):
                head1_followed_by[rows[idx + 1].row_type] += 1
        obs["head1_followed_by"] = dict(sorted(head1_followed_by.items()))

        # --- 9. Item UOM patterns ---
        item_uom_dist = Counter()
        for r in rows:
            if r.row_type == "Item" and r.uom:
                item_uom_dist[r.uom] += 1
        obs["item_count"] = sum(item_uom_dist.values())
        obs["item_uom_distribution"] = dict(sorted(item_uom_dist.items()))

        # UOM transitions involving Items (Head -> Item directly)
        item_following_heads = Counter()
        for i in range(len(rows) - 1):
            if rows[i].row_type == "Head" and rows[i + 1].row_type == "Item":
                item_following_heads[(rows[i].uom, rows[i + 1].uom)] += 1
        obs["item_following_head_by_uom"] = [
            {"head_uom": k[0], "item_uom": k[1], "count": v}
            for k, v in sorted(item_following_heads.items(), key=lambda x: -x[1])
        ]

        return obs
    finally:
        parser.close()


def main():
    print("=" * 70)
    print("EQ-0010 SPIKE 2: UOM PATTERN ANALYSIS")
    print("=" * 70)
    print()
    print(f"Fixture: {FIXTURE}")
    print(f"Fixture exists: {FIXTURE.exists()}")
    print()

    print("--- RUN 1 ---")
    run1 = run_uom_analysis()
    print(json.dumps(run1, indent=2, default=str))
    print()

    print("--- RUN 2 ---")
    run2 = run_uom_analysis()
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
    print("SPIKE 2 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()