"""EQ-0010 Spike 3: Row Sequence Analysis.

Engineering Investigation — NOT production code.

This spike investigates whether Head1-5 indicator labels plus row sequences
deterministically define structural hierarchy (depth, parent headers,
empty headers, orphan items, heading tree structure).

Question: Can Head1-5 UOM strings be deterministically interpreted as
hierarchical levels based on row sequence patterns?

Governance: Engineering_Governance.md v1.0
Fixture: tests/fixtures/costx/full_boq.xlsx
"""

import sys
import json
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from jarvis.parsers.costx.workbook_parser import WorkbookParser
from jarvis.parsers.costx.boq_extraction import extract_boq, BOQRow

FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "costx" / "full_boq.xlsx"


def run_sequence_analysis():
    """Execute production pipeline and produce sequence observations."""
    parser = WorkbookParser()
    try:
        parser.load(FIXTURE)
        parser.validate()
        workbook = parser.workbook
        rows = extract_boq(workbook)
        assert len(rows) > 0

        obs = {}

        # --- 1. Row type sequence analysis ---
        # For each row type, what row types follow?
        row_type_transitions = Counter()
        for i in range(len(rows) - 1):
            row_type_transitions[(rows[i].row_type, rows[i + 1].row_type)] += 1
        obs["row_type_transition_count"] = len(row_type_transitions)
        obs["row_type_top_transitions"] = [
            {"from": k[0], "to": k[1], "count": v}
            for k, v in row_type_transitions.most_common(20)
        ]

        # --- 2. Head sequence: adjacency patterns ---
        # Build the ordered list of Head UOM values as they appear
        head_uom_sequence = []
        for r in rows:
            if r.row_type == "Head" and r.uom:
                head_uom_sequence.append(r.uom)

        obs["head_uom_sequence_count"] = len(head_uom_sequence)

        # Adjacent Head transitions (what Head UOM follows another Head UOM)
        head_adjacent_transitions = Counter()
        for i in range(len(head_uom_sequence) - 1):
            head_adjacent_transitions[
                (head_uom_sequence[i], head_uom_sequence[i + 1])
            ] += 1
        obs["head_adjacent_transitions"] = [
            {"from": k[0], "to": k[1], "count": v}
            for k, v in sorted(head_adjacent_transitions.items(),
                               key=lambda x: -x[1])
        ]

        # --- 3. What follows each Head UOM? (by row_type) ---
        head_followed_by = defaultdict(Counter)
        for i, r in enumerate(rows):
            if r.row_type == "Head" and r.uom:
                if i + 1 < len(rows):
                    head_followed_by[r.uom][rows[i + 1].row_type] += 1
        obs["head_followed_by_type"] = {
            uom: dict(counter) for uom, counter in sorted(head_followed_by.items())
        }

        # --- 4. What follows each Head UOM? (by uom, when next is also Head) ---
        head_followed_by_uom = defaultdict(Counter)
        for i, r in enumerate(rows):
            if r.row_type == "Head" and r.uom:
                if i + 1 < len(rows) and rows[i + 1].row_type == "Head" and rows[i + 1].uom:
                    head_followed_by_uom[r.uom][rows[i + 1].uom] += 1
        obs["head_followed_by_uom_when_head"] = {
            uom: dict(counter) for uom, counter in sorted(head_followed_by_uom.items())
        }

        # --- 5. Head-to-Head progression: numeric analysis ---
        # Extract the digit from Head1-5 to compare numerically
        def head_level(uom_str):
            if uom_str and uom_str.startswith("Head") and uom_str[4:].isdigit():
                return int(uom_str[4:])
            return None

        head_level_sequence = [head_level(u) for u in head_uom_sequence]
        head_level_sequence = [h for h in head_level_sequence if h is not None]

        # Count progression types
        progression_types = Counter()
        for i in range(len(head_level_sequence) - 1):
            curr = head_level_sequence[i]
            nxt = head_level_sequence[i + 1]
            if nxt == curr + 1:
                progression_types["deepen"] += 1
            elif nxt == curr - 1:
                progression_types["backtrack"] += 1
            elif nxt == curr:
                progression_types["same_level"] += 1
            elif nxt > curr + 1:
                progression_types["skip_deepen"] += 1
            elif nxt < curr - 1:
                progression_types["skip_backtrack"] += 1

        obs["head_level_progression_types"] = dict(
            sorted(progression_types.items(), key=lambda x: -x[1])
        )

        # --- 6. Items per Head and their positions ---
        # For each Head row, collect the Item UOMs that follow before next non-Head
        head_item_uoms = defaultdict(Counter)
        empty_heads = Counter()
        for i, r in enumerate(rows):
            if r.row_type != "Head" or not r.uom:
                continue
            found_items = False
            for j in range(i + 1, len(rows)):
                if rows[j].row_type == "Head":
                    break
                if rows[j].row_type == "Section":
                    break
                if rows[j].row_type == "Item" and rows[j].uom:
                    head_item_uoms[r.uom][rows[j].uom] += 1
                    found_items = True
            if not found_items:
                empty_heads[r.uom] += 1

        obs["head_item_uoms"] = {
            uom: dict(counter)
            for uom, counter in sorted(head_item_uoms.items())
        }
        obs["empty_head_counts"] = dict(sorted(empty_heads.items()))

        # --- 7. Immediate adjacency: Head to Item ---
        head_to_item_immediate = Counter()
        for i in range(len(rows) - 1):
            if (rows[i].row_type == "Head" and rows[i].uom and
                    rows[i + 1].row_type == "Item"):
                head_to_item_immediate[rows[i].uom] += 1
        obs["head_to_item_immediate"] = dict(
            sorted(head_to_item_immediate.items())
        )

        # --- 8. Head sequence by section ---
        head_by_section = defaultdict(list)
        for r in rows:
            if r.row_type == "Head" and r.uom:
                sec = r.section if r.section else "(none)"
                head_by_section[sec].append(r.uom)
        obs["head_sequence_by_section_lengths"] = {
            sec: len(seq) for sec, seq in sorted(head_by_section.items())
        }

        # Progression within each section
        for section_label in sorted(head_by_section.keys()):
            seq = head_by_section[section_label]
            prog = Counter()
            for i in range(len(seq) - 1):
                curr = head_level(seq[i])
                nxt = head_level(seq[i + 1])
                if curr is None or nxt is None:
                    continue
                if nxt == curr + 1:
                    prog["deepen"] += 1
                elif nxt == curr - 1:
                    prog["backtrack"] += 1
                elif nxt == curr:
                    prog["same_level"] += 1
                elif nxt > curr + 1:
                    prog["skip_deepen"] += 1
                elif nxt < curr - 1:
                    prog["skip_backtrack"] += 1
            obs[f"progression_{section_label}"] = dict(
                sorted(prog.items(), key=lambda x: -x[1])
            )

        return obs
    finally:
        parser.close()


def main():
    print("=" * 70)
    print("EQ-0010 SPIKE 3: ROW SEQUENCE ANALYSIS")
    print("=" * 70)
    print()
    print(f"Fixture: {FIXTURE}")
    print(f"Fixture exists: {FIXTURE.exists()}")
    print()

    print("--- RUN 1 ---")
    run1 = run_sequence_analysis()
    print(json.dumps(run1, indent=2, default=str))
    print()

    print("--- RUN 2 ---")
    run2 = run_sequence_analysis()
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
    print("SPIKE 3 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()