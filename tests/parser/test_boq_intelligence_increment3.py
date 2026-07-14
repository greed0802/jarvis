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
"""

import pytest

from jarvis.parsers.costx.boq_extraction import BOQRow
from jarvis.parsers.costx.boq_intelligence import analyze_boq

class TestBackwardCompatibility:
    """Verify Increment 1 and Increment 2 outputs remain unchanged when Increment 3 is disabled.
    
    Evidence: Implementation Design acceptance criterion.
    """
    
    def test_increment1_unchanged_with_increment3_disabled(self):
        """Increment 1 results unchanged when include_detection=False."""
        rows = [
            BOQRow(1, "Item", "A001", "Test item", 10.0, "m", "SECTION_A"),
            BOQRow(2, "Item", "A002", "Another item", 5.0, "m2", "SECTION_A"),
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
            BOQRow(1, "Head", None, "Main section", None, "Head1", "SECTION_A"),
            BOQRow(2, "Head", None, "Subsection", None, "Head2", "SECTION_A"),
            BOQRow(3, "Item", "A001", "Test item", 10.0, "m", "SECTION_A"),
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
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(15, "Head", None, "Level 3", None, "Head3", "SECTION_A"),
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
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(50, "Head", None, "Level 5", None, "Head5", "SECTION_A"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result.detected_level_skips is not None
        assert len(result.detected_level_skips) == 1
        
        skip = result.detected_level_skips[0]
        assert skip["skip_magnitude"] == 3
    
    def test_no_level_skip_sequential(self):
        """No skip detected for sequential levels."""
        rows = [
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(20, "Head", None, "Level 2", None, "Head2", "SECTION_A"),
            BOQRow(30, "Head", None, "Level 3", None, "Head3", "SECTION_A"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result.detected_level_skips is not None
        assert len(result.detected_level_skips) == 0
    
    def test_level_skip_determinism(self):
        """Level skip detection is deterministic."""
        rows = [
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(15, "Head", None, "Level 3", None, "Head3", "SECTION_A"),
        ]
        
        result1 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        result2 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result1.detected_level_skips == result2.detected_level_skips

class TestZeroQuantityDetection:
    """Test zero quantity detection capability.
    
    Evidence: EQ-0010 Spike 1, EQ-0011 Spike 2, EQ-0011 Spike 3.
    """
    
    def test_detect_single_zero_quantity(self):
        """Detect item with quantity == 0.0."""
        rows = [
            BOQRow(1, "Item", "A001", "Zero quantity item", 0.0, "m", "SECTION_A"),
            BOQRow(2, "Item", "A002", "Normal item", 10.0, "m", "SECTION_A"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result.zero_quantity_items is not None
        assert len(result.zero_quantity_items) == 1
        
        zero_item = result.zero_quantity_items[0]
        assert zero_item["row_number"] == 1
        assert zero_item["code"] == "A001"
        assert zero_item["quantity"] == 0.0
        assert zero_item["uom"] == "m"
        assert zero_item["section"] == "SECTION_A"
    
    def test_detect_multiple_zero_quantities(self):
        """Detect multiple items with quantity == 0.0."""
        rows = [
            BOQRow(1, "Item", "A001", "Zero 1", 0.0, "m", "SECTION_A"),
            BOQRow(2, "Item", "A002", "Normal", 5.0, "m", "SECTION_A"),
            BOQRow(3, "Item", "A003", "Zero 2", 0.0, "m2", "SECTION_B"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result.zero_quantity_items is not None
        assert len(result.zero_quantity_items) == 2
    
    def test_no_zero_quantities(self):
        """No zero quantities detected when all items have quantity > 0."""
        rows = [
            BOQRow(1, "Item", "A001", "Item 1", 10.0, "m", "SECTION_A"),
            BOQRow(2, "Item", "A002", "Item 2", 5.0, "m", "SECTION_A"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result.zero_quantity_items is not None
        assert len(result.zero_quantity_items) == 0
    
    def test_zero_quantity_determinism(self):
        """Zero quantity detection is deterministic."""
        rows = [
            BOQRow(1, "Item", "A001", "Zero item", 0.0, "m", "SECTION_A"),
        ]
        
        result1 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        result2 = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result1.zero_quantity_items == result2.zero_quantity_items

class TestStructuralContainment:
    """Test structural containment detection capability.
    
    Evidence: EQ-0010 Spike 4, EQ-0011 Spike 3.
    """
    
    def test_no_structural_inversions_valid_hierarchy(self):
        """No inversions detected in valid hierarchy."""
        rows = [
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(20, "Head", None, "Level 2", None, "Head2", "SECTION_A"),
            BOQRow(30, "Head", None, "Level 3", None, "Head3", "SECTION_A"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result.structural_containment_findings is not None
        assert len(result.structural_containment_findings) == 0
    
    def test_structural_containment_determinism(self):
        """Structural containment detection is deterministic."""
        rows = [
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(20, "Head", None, "Level 2", None, "Head2", "SECTION_A"),
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
            BOQRow(10, "Head", None, "Section header", None, "Head1", "SECTION_A"),
            BOQRow(20, "Head", None, "Empty section", None, "Head1", "SECTION_B"),
            BOQRow(30, "Item", "A001", "Item in section A", 10.0, "m", "SECTION_A"),
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
            BOQRow(10, "Head", None, "Section A header", None, "Head1", "SECTION_A"),
            BOQRow(20, "Item", "A001", "Item A", 10.0, "m", "SECTION_A"),
            BOQRow(30, "Head", None, "Section B header", None, "Head1", "SECTION_B"),
            BOQRow(40, "Item", "B001", "Item B", 5.0, "m", "SECTION_B"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=True, include_detection=True)
        
        assert result.completeness_findings is not None
        assert len(result.completeness_findings) == 0
    
    def test_basic_completeness_determinism(self):
        """Basic completeness detection is deterministic."""
        rows = [
            BOQRow(10, "Head", None, "Empty section", None, "Head1", "SECTION_A"),
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
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(15, "Head", None, "Level 3", None, "Head3", "SECTION_A"),
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
        """Zero quantity evidence contains no forbidden terms."""
        rows = [
            BOQRow(1, "Item", "A001", "Test item", 0.0, "m", "SECTION_A"),
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
            BOQRow(10, "Head", None, "Level 1", None, "Head1", "SECTION_A"),
            BOQRow(20, "Head", None, "Level 2", None, "Head2", "SECTION_A"),
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
            BOQRow(10, "Head", None, "Empty section", None, "Head1", "SECTION_A"),
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
            BOQRow(1, "Item", "A001", "Zero item", 0.0, "m", "SECTION_A"),
        ]
        
        result = analyze_boq(rows, include_hierarchy=False, include_detection=True)
        
        # All detection fields should be None when hierarchy is not enabled
        assert result.detected_level_skips is None
        assert result.zero_quantity_items is None
        assert result.structural_containment_findings is None
        assert result.completeness_findings is None