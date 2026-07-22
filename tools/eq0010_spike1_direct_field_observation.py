"""EQ-0010 Spike 1: Direct Field Observation.

Engineering Investigation — NOT production code.

This spike establishes what is Observable from BOQRow fields alone.
It enumerates all fields, produces presence statistics, and documents
field value distributions.

Follows Engineering_Governance.md v1.0.

Governance: Engineering_Governance.md v1.0
Fixture: tests/fixtures/costx/full_boq.xlsx
Pipeline: WorkbookParser -> extract_boq() -> BOQRow
"""

import sys
import json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from jarvis.parsers.costx.workbook_parser import WorkbookParser
from jarvis.parsers.costx.boq_extraction import extract_boq, BOQRow

FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "costx" / "full_boq.xlsx"


def run_observation():
    """Execute production pipeline and produce field observations."""
    parser = WorkbookParser()
    try:
        parser.load(FIXTURE)
        parser.validate()
        workbook = parser.workbook
        rows = extract_boq(workbook)

        assert all(isinstance(r, BOQRow) for r in rows), "extract_boq must return BOQRow instances"
        assert len(rows) > 0, "Must extract at least one row"

        obs = {}

        # --- Pipeline metadata ---
        obs["fixture_path"] = str(FIXTURE)
        obs["fixture_exists"] = FIXTURE.exists()
        obs["total_rows"] = len(rows)

        # --- Field presence statistics ---
        fields = {
            "row_number": lambda r: r.row_number is not None,
            "code": lambda r: r.code is not None,
            "description": lambda r: r.description is not None,
            "quantity": lambda r: r.quantity is not None,
            "uom": lambda r: r.uom is not None,
            "row_type": lambda r: r.row_type is not None,
            "section": lambda r: r.section is not None,
        }

        field_stats = {}
        for field_name, check in fields.items():
            present = sum(1 for r in rows if check(r))
            absent = len(rows) - present
            field_stats[field_name] = {
                "present": present,
                "absent": absent,
                "present_pct": round(present / len(rows) * 100, 2),
            }
        obs["field_presence"] = field_stats

        # --- Row type distribution ---
        row_type_counts = Counter(r.row_type for r in rows)
        obs["row_type_counts"] = dict(sorted(row_type_counts.items()))

        # --- UOM distinct values and counts ---
        uom_counts = Counter(r.uom for r in rows if r.uom is not None)
        obs["uom_values"] = dict(sorted(uom_counts.items(), key=lambda x: -x[1]))

        # --- Section values ---
        section_counts = Counter(r.section if r.section else "(none)" for r in rows)
        obs["section_distribution"] = dict(sorted(section_counts.items(), key=lambda x: -x[1]))

        # --- Row type by section ---
        row_type_by_section = {}
        for r in rows:
            sec = r.section if r.section else "(none)"
            if sec not in row_type_by_section:
                row_type_by_section[sec] = Counter()
            row_type_by_section[sec][r.row_type] += 1
        obs["row_type_by_section"] = {
            sec: dict(sorted(counts.items()))
            for sec, counts in sorted(row_type_by_section.items())
        }

        # --- First and last rows ---
        def row_to_dict(r):
            return {
                "row_number": r.row_number,
                "code": r.code,
                "description": r.description,
                "quantity": r.quantity,
                "uom": r.uom,
                "row_type": r.row_type,
                "section": r.section,
            }

        obs["first_row"] = row_to_dict(rows[0])
        obs["last_row"] = row_to_dict(rows[-1])

        # --- Row number range ---
        row_numbers = [r.row_number for r in rows]
        obs["row_number_range"] = {
            "min": min(row_numbers),
            "max": max(row_numbers),
            "contiguous": row_numbers == list(range(min(row_numbers), max(row_numbers) + 1)),
        }

        # --- Distinct code and description counts ---
        unique_codes = set(r.code for r in rows if r.code is not None)
        unique_descs = set(r.description for r in rows if r.description is not None)
        obs["unique_code_count"] = len(unique_codes)
        obs["unique_description_count"] = len(unique_descs)

        # --- Code and description empty string analysis ---
        empty_codes = sum(1 for r in rows if r.code is not None and r.code.strip() == "")
        empty_descs = sum(1 for r in rows if r.description is not None and r.description.strip() == "")
        obs["empty_string_values"] = {
            "code": empty_codes,
            "description": empty_descs,
        }

        # --- Quantity statistics ---
        quantities = [r.quantity for r in rows if r.quantity is not None]
        if quantities:
            obs["quantity_statistics"] = {
                "min": min(quantities),
                "max": max(quantities),
                "count_negative": sum(1 for q in quantities if q < 0),
                "count_zero": sum(1 for q in quantities if q == 0.0),
                "count_positive": sum(1 for q in quantities if q > 0),
                "distinct_values": len(set(quantities)),
            }

        # --- Null field patterns (which fields are null together) ---
        null_patterns = Counter()
        for r in rows:
            pattern = []
            if r.code is None:
                pattern.append("code")
            if r.description is None:
                pattern.append("description")
            if r.quantity is None:
                pattern.append("quantity")
            if r.uom is None:
                pattern.append("uom")
            if r.section is None:
                pattern.append("section")
            key = ",".join(pattern) if pattern else "(all present)"
            null_patterns[key] += 1
        obs["null_field_patterns"] = dict(null_patterns.most_common())

        return obs
    finally:
        parser.close()


def main():
    print("=" * 70)
    print("EQ-0010 SPIKE 1: DIRECT FIELD OBSERVATION")
    print("=" * 70)
    print()
    print(f"Fixture: {FIXTURE}")
    print(f"Fixture exists: {FIXTURE.exists()}")
    print()

    print("--- RUN 1 ---")
    run1 = run_observation()
    print(json.dumps(run1, indent=2, default=str))
    print()

    print("--- RUN 2 ---")
    run2 = run_observation()
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
    print("--- OBSERVABLE CAPABILITIES FROM SPIKE 1 ---")
    print()
    print("Directly observable BOQRow fields:")
    for field in ["row_number", "code", "description", "quantity", "uom", "row_type", "section"]:
        stats = run1["field_presence"][field]
        print(f"  {field}: present={stats['present']}, absent={stats['absent']}, "
              f"present_pct={stats['present_pct']}%")

    print()
    print("Row type counts:")
    for rt, count in run1["row_type_counts"].items():
        print(f"  {rt}: {count}")

    print()
    print("Distinct UOM values:", len(run1["uom_values"]))
    print("Distinct codes:", run1["unique_code_count"])
    print("Distinct descriptions:", run1["unique_description_count"])

    print()
    print("=" * 70)
    print("SPIKE 1 COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()