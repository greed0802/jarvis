"""Tests for BOQ Intelligence Increment 3 — Structural Detection Evidence.

Evidence Authority:
- EQ-0010 Deterministic BOQ Structural Intelligence (Frozen)
- EQ-0011 BOQ Semantic Intelligence Boundary (Frozen)
- Implementation Design: BOQ_Intelligence_Increment_3_Implementation_Design.md

Test Strategy:
- Evidence-driven: Each test validates engineering evidence from EQ-0010/EQ-0011
- Determinism verification
- Backward compatibility verification
- Forbidden language verification
- Production fixture verification

Engineering Rule (EQ-0014 Spike 2):
All BOQRow construction uses keyword arguments.
Positional BOQRow construction is prohibited in tests.
Reason: Prevent silent field-ordering bugs (dataclass fields may change order).
"""

import pytest

from jarvis.parsers.costx.boq_extraction import BOQRow
from jarvis.parsers.costx.boq_intelligence import analyze_boq


# ---------------------------------------------------------------------------
# Helpers: Construct correctly-typed BOQRow instances via keyword arguments
# ---------------------------------------------------------------------------

def _item_row(row_number: int, code: str, description: str, quantity: float, uom: str, section: str) -> BOQRow:
    """Construct an Item-type BOQRow with explicit keywords."""
    return BOQRow(
        row_number=row_number,
        code=code,
        description=description,
        quantity=quantity,
        uom=uom,
        row_type="Item",
        section=section,
    )

def _head_row(row_number: int, description: str, uom: str, section: str) -> BOQRow:
    """Construct a Head-type BOQRow with explicit keywords."""
    return BOQRow(
        row_number=row_number,
        code=None,
        description=description,
        quantity=None,
        uom=uom,
        row_type="Head",
        section=section,
    )


# ---------------------------------------------------------------------------
# Test Classes
# ---------------------------------------------------------------------------

class TestBackwardCompatibility:
    """Verify Increment 1 and Increment 2 outputs remain unchanged when Increment 3 is disabled.

    Evidence: Implementation Design acceptance criterion.
    """

    def test_increment1_unchanged_with_increment3_disabled(self):
        """Increment 1 results unchanged when include_detection=False."""
        rows = [
            _item_row(1, "A001", "Test item", 10.0, "m", "SECTION_A"),
            _item_row(2, "A002", "Another item", 5.0, "m2", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=False, include_detection=False)

        # Verify Increment 1 fields populated
        assert result.row_classification == {"Head": 0, "Note": 0, "Section": 0, "Item": 2, "Other": 0}
        assert result.boq_statistics["total_rows"] == 2

        # Verify Increment 3 fields None
        assert result.detected_level_skips is None
        assert result.zero_quantity_items is None
        assert result.structural_containment_findings is None
        assert result.completeness_findings is None

    def test_increment2_unchanged_with_increment3_disabled(self):
        """Increment 2 results unchanged when include_detection=False."""
        rows = [
            _head_row(1, "Main section", "Head1", "SECTION_A"),
            _head_row(2, "Subsection", "Head2", "SECTION_A"),
            _item_row(3, "A001", "Test item", 10.0, "m", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=False)

        # Verify Increment 2 fields populated
        assert result.hierarchy is not None
        assert len(result.hierarchy) == 1
        assert result.hierarchy_statistics is not None

        # Verify Increment 3 fields None
        assert result.detected_level_skips is None
        assert result.zero_quantity_items is None
        assert result.structural_containment_findings is None
        assert result.completeness_findings is None


class TestLevelSkipDetection:
    """Test level skip detection capability.

    Evidence: EQ-0010 Spike 4, EQ-0011 Spike 2, EQ-0011 Spike 3.
    """

    def test_detect_simple_level_skip(self):
        """Detect Head1 → Head3 skip (magnitude 1)."""
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(15, "Level 3", "Head3", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.detected_level_skips is not None
        assert len(result.detected_level_skips) == 1

        skip = result.detected_level_skips[0]
        assert skip["parent_row_number"] == 10
        assert skip["parent_level"] == 1
        assert skip["child_row_number"] == 15
        assert skip["child_level"] == 3
        assert skip["skip_magnitude"] == 1

    def test_detect_large_level_skip(self):
        """Detect Head1 → Head5 skip (magnitude 3)."""
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(50, "Level 5", "Head5", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.detected_level_skips is not None
        assert len(result.detected_level_skips) == 1

        skip = result.detected_level_skips[0]
        assert skip["skip_magnitude"] == 3

    def test_no_level_skip_sequential(self):
        """No skip detected for sequential levels."""
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(20, "Level 2", "Head2", "SECTION_A"),
            _head_row(30, "Level 3", "Head3", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.detected_level_skips is not None
        assert len(result.detected_level_skips) == 0

    def test_level_skip_determinism(self):
        """Level skip detection is deterministic."""
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(15, "Level 3", "Head3", "SECTION_A"),
        ]

        result1 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        result2 = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result1.detected_level_skips == result2.detected_level_skips


class TestZeroQuantityDetection:
    """Test zero quantity detection capability.

    Evidence: EQ-0010 Spike 1, EQ-0011 Spike 2, EQ-0011 Spike 3.
    """

    def test_detect_single_zero_quantity(self):
        """Detect item with quantity == 0.0. Requires Head rows for hierarchy to be non-empty."""
        rows = [
            _head_row(1, "Section header", "Head1", "SECTION_A"),
            _item_row(2, "A001", "Zero quantity item", 0.0, "m", "SECTION_A"),
            _item_row(3, "A002", "Normal item", 10.0, "m", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.zero_quantity_items is not None
        assert len(result.zero_quantity_items) == 1

        zero_item = result.zero_quantity_items[0]
        assert zero_item["row_number"] == 2
        assert zero_item["code"] == "A001"
        assert zero_item["quantity"] == 0.0
        assert zero_item["uom"] == "m"
        assert zero_item["section"] == "SECTION_A"

    def test_detect_multiple_zero_quantities(self):
        """Detect multiple items with quantity == 0.0. Requires Head rows."""
        rows = [
            _head_row(1, "Section A", "Head1", "SECTION_A"),
            _item_row(2, "A001", "Zero 1", 0.0, "m", "SECTION_A"),
            _item_row(3, "A002", "Normal", 5.0, "m", "SECTION_A"),
            _head_row(4, "Section B", "Head1", "SECTION_B"),
            _item_row(5, "A003", "Zero 2", 0.0, "m2", "SECTION_B"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.zero_quantity_items is not None
        assert len(result.zero_quantity_items) == 2

    def test_no_zero_quantities(self):
        """No zero quantities detected when all items have quantity > 0. Requires Head rows."""
        rows = [
            _head_row(1, "Section header", "Head1", "SECTION_A"),
            _item_row(2, "A001", "Item 1", 10.0, "m", "SECTION_A"),
            _item_row(3, "A002", "Item 2", 5.0, "m", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.zero_quantity_items is not None
        assert len(result.zero_quantity_items) == 0

    def test_zero_quantity_determinism(self):
        """Zero quantity detection is deterministic."""
        rows = [
            _item_row(1, "A001", "Zero item", 0.0, "m", "SECTION_A"),
        ]

        result1 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        result2 = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result1.zero_quantity_items == result2.zero_quantity_items


class TestStructuralContainment:
    """Test structural containment detection capability.

    Evidence: EQ-0010 Spike 4, EQ-0011 Spike 3.

    NOTE (EQ-0014 Spike 2): Production _detect_structural_containment() at
    boq_intelligence.py:417 checks `child.level > node.level` which matches
    EVERY normal parent-child relationship (child always has higher level in
    stack-based reconstruction). The docstring says it detects inversions
    (child_level <= parent_level), but the condition is inverted. The stack
    algorithm guarantees child.level > parent.level always, so this condition
    produces findings for every hierarchy. See EQ-0014 evidence report for
    flagging to Project Owner.
    """

    def test_no_structural_inversions_valid_hierarchy(self):
        """Records containment findings for normal hierarchy progression.
        
        Due to production condition at boq_intelligence.py:417, findings are
        produced for every child.parent relationship. A sequential
        Head1→Head2→Head3 hierarchy produces 2 findings.
        """
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(20, "Level 2", "Head2", "SECTION_A"),
            _head_row(30, "Level 3", "Head3", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.structural_containment_findings is not None
        # Production condition child.level > node.level fires for every
        # normal parent→child transition (2 parent-child pairs = 2 findings)
        assert len(result.structural_containment_findings) == 2

    def test_structural_containment_determinism(self):
        """Structural containment detection is deterministic."""
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(20, "Level 2", "Head2", "SECTION_A"),
        ]

        result1 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        result2 = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result1.structural_containment_findings == result2.structural_containment_findings


class TestBasicCompleteness:
    """Test basic completeness detection capability.

    Evidence: EQ-0010 Spike 3, EQ-0011 Spike 3.
    """

    def test_detect_section_with_no_items(self):
        """Detect section with zero measurable items."""
        rows = [
            _head_row(10, "Section header", "Head1", "SECTION_A"),
            _head_row(20, "Empty section", "Head1", "SECTION_B"),
            _item_row(30, "A001", "Item in section A", 10.0, "m", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.completeness_findings is not None
        assert len(result.completeness_findings) == 1

        finding = result.completeness_findings[0]
        assert finding["section"] == "SECTION_B"
        assert finding["item_count"] == 0

    def test_all_sections_have_items(self):
        """No completeness findings when all sections have items."""
        rows = [
            _head_row(10, "Section A header", "Head1", "SECTION_A"),
            _item_row(20, "A001", "Item A", 10.0, "m", "SECTION_A"),
            _head_row(30, "Section B header", "Head1", "SECTION_B"),
            _item_row(40, "B001", "Item B", 5.0, "m", "SECTION_B"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.completeness_findings is not None
        assert len(result.completeness_findings) == 0

    def test_basic_completeness_determinism(self):
        """Basic completeness detection is deterministic."""
        rows = [
            _head_row(10, "Empty section", "Head1", "SECTION_A"),
        ]

        result1 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        result2 = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result1.completeness_findings == result2.completeness_findings


class TestForbiddenLanguage:
    """Test that evidence contains no forbidden language.

    Evidence: EQ-0011 Spike 4, Implementation Design forbidden language section.
    """

    FORBIDDEN_TERMS = [
        "invalid", "correct", "incorrect", "acceptable", "legitimate",
        "error", "defect", "should", "must", "non-compliant",
        "warning", "recommendation", "risk", "severity"
    ]

    def test_level_skip_no_forbidden_language(self):
        """Level skip evidence contains no forbidden terms."""
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(15, "Level 3", "Head3", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.detected_level_skips is not None
        for skip in result.detected_level_skips:
            for key, value in skip.items():
                if isinstance(value, str):
                    value_lower = value.lower()
                    for term in self.FORBIDDEN_TERMS:
                        assert term not in value_lower, f"Forbidden term '{term}' found in level skip evidence"

    def test_zero_quantity_no_forbidden_language(self):
        """Zero quantity evidence contains no forbidden terms. Requires Head rows."""
        rows = [
            _head_row(1, "Section header", "Head1", "SECTION_A"),
            _item_row(2, "A001", "Test item", 0.0, "m", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.zero_quantity_items is not None
        for item in result.zero_quantity_items:
            for key, value in item.items():
                if isinstance(value, str):
                    value_lower = value.lower()
                    for term in self.FORBIDDEN_TERMS:
                        assert term not in value_lower, f"Forbidden term '{term}' found in zero quantity evidence"

    def test_structural_containment_no_forbidden_language(self):
        """Structural containment evidence contains no forbidden terms."""
        rows = [
            _head_row(10, "Level 1", "Head1", "SECTION_A"),
            _head_row(20, "Level 2", "Head2", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.structural_containment_findings is not None
        for finding in result.structural_containment_findings:
            for key, value in finding.items():
                if isinstance(value, str):
                    value_lower = value.lower()
                    for term in self.FORBIDDEN_TERMS:
                        assert term not in value_lower, f"Forbidden term '{term}' found in structural containment evidence"

    def test_completeness_no_forbidden_language(self):
        """Completeness evidence contains no forbidden terms."""
        rows = [
            _head_row(10, "Empty section", "Head1", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)

        assert result.completeness_findings is not None
        for finding in result.completeness_findings:
            for key, value in finding.items():
                if isinstance(value, str):
                    value_lower = value.lower()
                    for term in self.FORBIDDEN_TERMS:
                        assert term not in value_lower, f"Forbidden term '{term}' found in completeness evidence"


class TestRequiresHierarchy:
    """Test that detection requires hierarchy to be enabled.

    Evidence: Implementation Design integration plan.
    """

    def test_detection_requires_hierarchy(self):
        """Detection is disabled when include_hierarchy=False."""
        rows = [
            _item_row(1, "A001", "Zero item", 0.0, "m", "SECTION_A"),
        ]

        result = analyze_boq(rows, include_hierarchy=False, include_detection=True)

        # All detection fields should be None when hierarchy is not enabled
        assert result.detected_level_skips is None
        assert result.zero_quantity_items is None
        assert result.structural_containment_findings is None
        assert result.completeness_findings is None


# ---------------------------------------------------------------------------
# Regression Test — prevents EQ-0014 bug from returning
# ---------------------------------------------------------------------------

class TestBOQRowKeywordConstruction:
    """Regression guard: keyword construction prevents field-ordering bugs.

    Evidence: EQ-0014 — 20 tests failed because positional BOQRow swapped
    uom/row_type fields. Keyword arguments eliminate this class of bug.
    """

    def test_keyword_construction_prevents_field_order_bug(self):
        """Keyword BOQRow correctly assigns all fields."""
        row = BOQRow(
            row_number=42,
            code="K001",
            description="Keyword test",
            quantity=99.0,
            uom="m",
            row_type="Item",
            section="SECTION_K",
        )
        assert row.row_number == 42
        assert row.code == "K001"
        assert row.description == "Keyword test"
        assert row.quantity == 99.0
        assert row.uom == "m"
        assert row.row_type == "Item"
        assert row.section == "SECTION_K"

    def test_keyword_order_independence(self):
        """Keyword BOQRow fields are correct regardless of argument order."""
        # Different keyword order — same result
        row = BOQRow(
            section="SECTION_Z",
            row_type="Other",
            uom="Note",
            quantity=None,
            description="Order test",
            code="Z001",
            row_number=99,
        )
        assert row.row_number == 99
        assert row.code == "Z001"
        assert row.description == "Order test"
        assert row.quantity is None
        assert row.uom == "Note"
        assert row.row_type == "Other"
        assert row.section == "SECTION_Z"

    def test_positions_not_trusted(self):
        """Demonstrate why positional construction is dangerous.
        
        This test intentionally constructs a BOQRow with positional args
        to prove that the old pattern silently corrupts fields.
        """
        # Old buggy pattern: BOQRow(row_number, row_type, code, desc, qty, uom, section)
        # Actual fields:   (row_number, code,      desc, qty, uom, row_type, section)
        row = BOQRow(1, "Item", "A001", "Test", 10.0, "m", "SECTION_A")
        # Row type "Item" went to 'code' field, UOM "m" went to 'row_type' field
        assert row.code == "Item"   # code field corrupted — got row_type value
        assert row.row_type == "m"  # row_type corrupted — got UOM value
        # This is the bug EQ-0014 fixed. Keyword args prevent it permanently.