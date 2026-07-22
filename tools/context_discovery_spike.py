"""EQ-0009 Context Discovery Spike.

Engineering Investigation — NOT production code.

This spike records what structured information can be deterministically
assembled from the current production pipeline. It does not interpret,
classify observations as Context, or evaluate architecture.

Allowed imports: WorkbookParser, extract_boq, BOQRow.
Fixture: tests/fixtures/costx/full_boq.xlsx

Steps:
1. Load full_boq.xlsx
2. Validate workbook
3. Execute extract_boq()
4. Record every observable output produced by the production pipeline
5. Produce structured engineering observations
6. Repeat execution
7. Verify deterministic output
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from jarvis.parsers.costx.workbook_parser import WorkbookParser
from jarvis.parsers.costx.boq_extraction import extract_boq, BOQRow

FIXTURE = Path(__file__).resolve().parent.parent / "tests" / "fixtures" / "costx" / "full_boq.xlsx"


def run_pipeline():
    """Execute the production pipeline and return raw observations."""
    parser = WorkbookParser()
    try:
        parser.load(FIXTURE)
        parser.validate()

        workbook = parser.workbook
        ws = workbook[workbook.sheetnames[0]]

        rows = extract_boq(workbook)

        assert all(isinstance(r, BOQRow) for r in rows), "extract_boq must return BOQRow instances"

        observations = {}

        observations["fixture_path"] = str(FIXTURE)
        observations["fixture_exists"] = FIXTURE.exists()
        observations["workbook_sheet_names"] = workbook.sheetnames
        observations["workbook_max_row"] = ws.max_row
        observations["workbook_max_column"] = ws.max_column
        observations["validation_passed"] = True

        observations["extraction_row_count"] = len(rows)

        observations["first_data_row_examined"] = 6

        if rows:
            observations["first_row"] = {
                "row_number": rows[0].row_number,
                "code": rows[0].code,
                "description": rows[0].description,
                "quantity": rows[0].quantity,
                "uom": rows[0].uom,
                "row_type": rows[0].row_type,
                "section": rows[0].section,
            }
            observations["last_row"] = {
                "row_number": rows[-1].row_number,
                "code": rows[-1].code,
                "description": rows[-1].description,
                "quantity": rows[-1].quantity,
                "uom": rows[-1].uom,
                "row_type": rows[-1].row_type,
                "section": rows[-1].section,
            }

        row_types = {}
        for r in rows:
            row_types[r.row_type] = row_types.get(r.row_type, 0) + 1
        observations["row_type_counts"] = dict(sorted(row_types.items()))

        sections = {}
        for r in rows:
            key = r.section if r.section else "(none)"
            sections[key] = sections.get(key, 0) + 1
        observations["section_counts"] = dict(sorted(sections.items()))

        uom_values = set()
        for r in rows:
            if r.uom is not None:
                uom_values.add(r.uom)
        observations["distinct_uom_values"] = sorted(uom_values)

        code_present = sum(1 for r in rows if r.code is not None)
        code_absent = sum(1 for r in rows if r.code is None)
        observations["code_field"] = {"present": code_present, "absent": code_absent}

        desc_present = sum(1 for r in rows if r.description is not None)
        desc_absent = sum(1 for r in rows if r.description is None)
        observations["description_field"] = {"present": desc_present, "absent": desc_absent}

        qty_present = sum(1 for r in rows if r.quantity is not None)
        qty_absent = sum(1 for r in rows if r.quantity is None)
        observations["quantity_field"] = {"present": qty_present, "absent": qty_absent}

        uom_present = sum(1 for r in rows if r.uom is not None)
        uom_absent = sum(1 for r in rows if r.uom is None)
        observations["uom_field"] = {"present": uom_present, "absent": uom_absent}

        section_present = sum(1 for r in rows if r.section is not None)
        section_absent = sum(1 for r in rows if r.section is None)
        observations["section_field"] = {"present": section_present, "absent": section_absent}

        quantities = [r.quantity for r in rows if r.quantity is not None]
        if quantities:
            observations["quantity_range"] = {
                "min": min(quantities),
                "max": max(quantities),
                "count_nonzero": sum(1 for q in quantities if q != 0.0),
                "count_zero": sum(1 for q in quantities if q == 0.0),
            }

        row_numbers = [r.row_number for r in rows]
        observations["row_number_range"] = {
            "min": min(row_numbers),
            "max": max(row_numbers),
            "contiguous": row_numbers == list(range(min(row_numbers), max(row_numbers) + 1)),
        }

        unique_codes = set()
        for r in rows:
            if r.code is not None:
                unique_codes.add(r.code)
        observations["unique_code_count"] = len(unique_codes)

        unique_descriptions = set()
        for r in rows:
            if r.description is not None:
                unique_descriptions.add(r.description)
        observations["unique_description_count"] = len(unique_descriptions)

        row_type_by_section = {}
        for r in rows:
            sec = r.section if r.section else "(none)"
            if sec not in row_type_by_section:
                row_type_by_section[sec] = {}
            row_type_by_section[sec][r.row_type] = row_type_by_section[sec].get(r.row_type, 0) + 1
        observations["row_type_by_section"] = {
            sec: dict(sorted(types.items())) for sec, types in sorted(row_type_by_section.items())
        }

        section_transitions = []
        prev_section = None
        for r in rows:
            if r.section != prev_section:
                section_transitions.append({
                    "row_number": r.row_number,
                    "from": prev_section if prev_section else "(none)",
                    "to": r.section if r.section else "(none)",
                })
                prev_section = r.section
        observations["section_transitions"] = section_transitions

        null_patterns = {}
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
            null_patterns[key] = null_patterns.get(key, 0) + 1
        observations["null_field_patterns"] = dict(sorted(null_patterns.items(), key=lambda x: -x[1]))

        head_rows = [r for r in rows if r.row_type == "Head"]
        if head_rows:
            head_levels = set()
            for r in head_rows:
                if r.uom and r.uom.startswith("Head"):
                    head_levels.add(r.uom)
            observations["head_levels_observed"] = sorted(head_levels)

        item_rows = [r for r in rows if r.row_type == "Item"]
        if item_rows:
            item_uoms = set()
            for r in item_rows:
                if r.uom is not None:
                    item_uoms.add(r.uom)
            observations["item_uom_values"] = sorted(item_uoms)

        note_rows = [r for r in rows if r.row_type == "Note"]
        observations["note_row_count"] = len(note_rows)

        section_rows = [r for r in rows if r.row_type == "Section"]
        section_descs = []
        for r in section_rows:
            section_descs.append({
                "row_number": r.row_number,
                "description": r.description,
            })
        observations["section_row_details"] = section_descs

        return observations
    finally:
        parser.close()


def main():
    print("=" * 70)
    print("EQ-0009 CONTEXT DISCOVERY SPIKE")
    print("=" * 70)
    print()

    print("--- RUN 1 ---")
    run1 = run_pipeline()
    print(json.dumps(run1, indent=2, default=str))
    print()

    print("--- RUN 2 ---")
    run2 = run_pipeline()
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
    print("SPIKE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()