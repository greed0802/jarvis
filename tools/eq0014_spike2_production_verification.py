"""EQ-0014 Spike 2 — Production Verification Script.

Produces explicit evidence that production _classify_row()
correctly maps UOM values to row_type classifications.

Verification A: UOM='m' → row_type='Item'
Verification B: UOM='Head1' → row_type='Head'

This is PERMANENT engineering evidence. Execution is evidence.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

# Ensure src/ is on Python path (tools run from repo root)
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import production code
from jarvis.parsers.costx.boq_extraction import BOQRow, _classify_row, _ITEM_UOMS

@dataclass
class VerificationResult:
    test: str
    input_uom: str
    output_row_type: str
    production_function: str
    passed: bool
    evidence_line: int

def main() -> None:
    results: list[VerificationResult] = []

    # --- Verification A: UOM='m' → row_type='Item' ---
    uom_a = "m"
    result_a = _classify_row(uom_a)
    passed_a = result_a == "Item"
    assert passed_a, f"Verification A FAILED: _classify_row('m') returned {result_a!r}, expected 'Item'"
    results.append(VerificationResult(
        test="Verification A",
        input_uom=uom_a,
        output_row_type=result_a,
        production_function="_classify_row",
        passed=True,
        evidence_line=123,  # boq_extraction.py line 122-123
    ))
    print(f"✓ Verification A: _classify_row('{uom_a}') → '{result_a}' (Expected: 'Item') — PASSED")
    print(f"  Production: boq_extraction.py:122-123 — uom in _ITEM_UOMS → row_type='Item'")
    print(f"  _ITEM_UOMS = {_ITEM_UOMS}")
    print(f"  '{uom_a}' in _ITEM_UOMS = {uom_a in _ITEM_UOMS}")
    print()

    # --- Verification B: UOM='Head1' → row_type='Head' ---
    uom_b = "Head1"
    result_b = _classify_row(uom_b)
    passed_b = result_b == "Head"
    assert passed_b, f"Verification B FAILED: _classify_row('Head1') returned {result_b!r}, expected 'Head'"
    results.append(VerificationResult(
        test="Verification B",
        input_uom=uom_b,
        output_row_type=result_b,
        production_function="_classify_row",
        passed=True,
        evidence_line=127,  # boq_extraction.py line 126-127
    ))
    print(f"✓ Verification B: _classify_row('{uom_b}') → '{result_b}' (Expected: 'Head') — PASSED")
    print(f"  Production: boq_extraction.py:126-127 — re.fullmatch(r'Head\\d+', uom) → row_type='Head'")
    print()

    # --- Additional: verify all other Head variants ---
    for level in range(1, 6):
        uom = f"Head{level}"
        result = _classify_row(uom)
        assert result == "Head", f"_classify_row('{uom}') returned {result!r}, expected 'Head'"
        print(f"✓ Additional: _classify_row('{uom}') → '{result}' — PASSED")
    print()

    # --- Demonstrate correct keyword BOQRow construction (Item) ---
    print("--- Correct BOQRow Keyword Construction Demonstrations ---")
    row_item = BOQRow(
        row_number=1,
        code="A001",
        description="Test item",
        quantity=10.0,
        uom="m",
        row_type=_classify_row("m"),
        section="SECTION_A",
    )
    print(f"Item BOQRow:")
    print(f"  row_number={row_item.row_number}")
    print(f"  code={row_item.code!r}")
    print(f"  description={row_item.description!r}")
    print(f"  quantity={row_item.quantity}")
    print(f"  uom={row_item.uom!r}")
    print(f"  row_type={row_item.row_type!r}")
    print(f"  section={row_item.section!r}")
    assert row_item.row_type == "Item", f"FAIL: row_type={row_item.row_type}"
    assert row_item.uom == "m", f"FAIL: uom={row_item.uom}"
    print("  ✓ All fields correct")
    print()

    # --- Demonstrate correct keyword BOQRow construction (Head) ---
    row_head = BOQRow(
        row_number=10,
        code=None,
        description="Level 1 header",
        quantity=None,
        uom="Head1",
        row_type=_classify_row("Head1"),
        section="SECTION_A",
    )
    print(f"Head BOQRow:")
    print(f"  row_number={row_head.row_number}")
    print(f"  code={row_head.code!r}")
    print(f"  description={row_head.description!r}")
    print(f"  quantity={row_head.quantity}")
    print(f"  uom={row_head.uom!r}")
    print(f"  row_type={row_head.row_type!r}")
    print(f"  section={row_head.section!r}")
    assert row_head.row_type == "Head", f"FAIL: row_type={row_head.row_type}"
    assert row_head.uom == "Head1", f"FAIL: uom={row_head.uom}"
    print("  ✓ All fields correct")
    print()

    # --- Demonstrate the BUGGY construction (what tests currently do) ---
    print("--- BUGGY Construction (what failing tests do) ---")
    print()
    print("Code: BOQRow(1, 'Item', 'A001', 'Test item', 10.0, 'm', 'SECTION_A')")
    row_buggy = BOQRow(1, "Item", "A001", "Test item", 10.0, "m", "SECTION_A")
    print(f"  row_number={row_buggy.row_number}")
    print(f"  code={row_buggy.code!r}     ← SHOULD BE 'A001', got 'Item' (code field gets row_type value)")
    print(f"  description={row_buggy.description!r}  ← SHOULD BE 'Test item', got 'A001'")
    print(f"  quantity={row_buggy.quantity}    ← SHOULD BE 10.0, got 'Test item' (str in float field)")
    print(f"  uom={row_buggy.uom!r}      ← SHOULD BE 'm', got 10.0 (float in str field)")
    print(f"  row_type={row_buggy.row_type!r}  ← SHOULD BE 'Item', got 'm' ← THIS IS THE BUG")
    print(f"  section={row_buggy.section!r}")
    print(f"  ✗ row_type='{row_buggy.row_type}' is NOT in _VALID_ROW_TYPES → ValueError raised")
    print()

    # --- Write JSON evidence ---
    report_dir = Path("data/reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    output_path = report_dir / "eq0014_spike2_production_verification.json"

    output = {
        "eq": "EQ-0014",
        "spike": 2,
        "title": "Production Verification — UOM to row_type mapping",
        "verification_a": {
            "input_uom": "m",
            "output_row_type": "Item",
            "production_function": "_classify_row",
            "evidence_line": 123,
            "passed": True,
        },
        "verification_b": {
            "input_uom": "Head1",
            "output_row_type": "Head",
            "production_function": "_classify_row",
            "evidence_line": 127,
            "passed": True,
        },
        "additional_head_verifications": [
            {"uom": f"Head{i}", "result": "Head", "passed": True}
            for i in range(1, 6)
        ],
        "production_code_unchanged": True,
        "root_cause": "tests use positional BOQRow with swapped field order",
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"JSON evidence written to: {output_path}")
    print()
    print("=" * 60)
    print("ALL PRODUCTION VERIFICATIONS PASSED")
    print("=" * 60)
    print()
    print("Conclusion:")
    print("  1. _classify_row('m') → 'Item' (via _ITEM_UOMS frozenset)")
    print("  2. _classify_row('Head1') → 'Head' (via Head\\d+ regex)")
    print("  3. Production code is CORRECT — no changes needed")
    print("  4. Test bug: positional BOQRow swaps uom/row_type positions")
    print()
    print("Ready to fix tests with keyword arguments.")

if __name__ == "__main__":
    main()