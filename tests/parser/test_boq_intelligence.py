"""Acceptance tests for BOQ Intelligence Increment 1 + Increment 2.

Verifies the production pipeline:
    WorkbookParser → extract_boq() → analyze_boq()

Increment 1 tests: All expected values from tests/reference/eq0007_evidence.py
Increment 2 tests: Evidence from EQ-0010 Spike 4

Fixture integrity verified via tests/fixtures/FIXTURE_METADATA.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
from jarvis.parsers.costx.boq_intelligence import (
    BOQHeaderNode,
    BOQIntelligenceResult,
    analyze_boq,
)
from jarvis.parsers.costx.workbook_parser import WorkbookParser
from tests.fixtures.FIXTURE_METADATA import verify_fixture
from tests.reference.eq0007_evidence import (
    KNOWN_ANOMALIES,
    ROW_CLASSIFICATION,
    SECTION_STATISTICS,
    TOTAL_ROWS,
)


@pytest.fixture(scope="module")
def fixture_path():
    return verify_fixture("full_boq.xlsx")


@pytest.fixture(scope="module")
def intelligence(fixture_path):
    parser = WorkbookParser()
    try:
        parser.load(fixture_path)
        parser.validate()
        rows = extract_boq(parser.workbook)
        return analyze_boq(rows)
    finally:
        parser.close()


class TestFixtureIntegrity:
    def test_fixture_verified(self, fixture_path):
        assert fixture_path.exists()
        assert fixture_path.name == "full_boq.xlsx"


class TestProductionPipelineClassification:
    def test_total_row_count(self, intelligence):
        assert intelligence.row_classification == ROW_CLASSIFICATION

    def test_total_rows_matches(self, intelligence):
        assert intelligence.boq_statistics["total_rows"] == TOTAL_ROWS

    def test_each_row_type_count(self, intelligence):
        for row_type, expected_count in ROW_CLASSIFICATION.items():
            assert intelligence.row_classification[row_type] == expected_count


class TestProductionPipelineSectionStatistics:
    def test_section_statistics_match(self, intelligence):
        assert intelligence.section_statistics == SECTION_STATISTICS

    def test_omission_negative_qty(self, intelligence):
        assert intelligence.section_statistics["OMISSION"]["negative_qty"] == 169

    def test_omission_positive_qty(self, intelligence):
        assert intelligence.section_statistics["OMISSION"]["positive_qty"] == 7

    def test_addition_negative_qty(self, intelligence):
        assert intelligence.section_statistics["ADDITION"]["negative_qty"] == 0

    def test_addition_positive_qty(self, intelligence):
        assert intelligence.section_statistics["ADDITION"]["positive_qty"] == 3


class TestIdentityLevelAnomalies:
    def test_anomaly_count(self, intelligence):
        assert len(intelligence.known_anomalies) == len(KNOWN_ANOMALIES)

    def test_anomaly_exact_identity(self, intelligence):
        assert intelligence.known_anomalies == KNOWN_ANOMALIES

    def test_each_anomaly_identity(self, intelligence):
        for expected in KNOWN_ANOMALIES:
            assert expected in intelligence.known_anomalies

    def test_anomaly_fields_complete(self, intelligence):
        for anomaly in intelligence.known_anomalies:
            assert "row_number" in anomaly
            assert "code" in anomaly
            assert "quantity" in anomaly
            assert "section" in anomaly
            assert anomaly["section"] == "OMISSION"
            assert anomaly["quantity"] > 0


class TestBOQStatistics:
    def test_total_rows(self, intelligence):
        assert intelligence.boq_statistics["total_rows"] == 6349

    def test_code_rows(self, intelligence):
        assert intelligence.boq_statistics["code_rows"] == 4257

    def test_description_rows(self, intelligence):
        assert intelligence.boq_statistics["description_rows"] == 6278

    def test_quantity_rows(self, intelligence):
        assert intelligence.boq_statistics["quantity_rows"] == 3605

    def test_uom_rows(self, intelligence):
        assert intelligence.boq_statistics["uom_rows"] == 6161

    def test_section_rows(self, intelligence):
        assert intelligence.boq_statistics["section_rows"] == 491


class TestDeterminism:
    def test_deterministic_across_runs(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result_1 = analyze_boq(rows)
            result_2 = analyze_boq(rows)
        finally:
            parser.close()

        assert result_1.row_classification == result_2.row_classification
        assert result_1.section_statistics == result_2.section_statistics
        assert result_1.boq_statistics == result_2.boq_statistics
        assert result_1.known_anomalies == result_2.known_anomalies


class TestResultStructure:
    def test_result_is_frozen_dataclass(self, intelligence):
        assert isinstance(intelligence, BOQIntelligenceResult)
        with pytest.raises(AttributeError):
            intelligence.row_classification = {}

    def test_result_fields_present(self, intelligence):
        assert hasattr(intelligence, "row_classification")
        assert hasattr(intelligence, "section_statistics")
        assert hasattr(intelligence, "boq_statistics")
        assert hasattr(intelligence, "known_anomalies")


class TestEdgeCases:
    def test_empty_row_list(self):
        result = analyze_boq([])
        assert result.row_classification == {
            "Head": 0, "Note": 0, "Section": 0, "Item": 0, "Other": 0,
        }
        assert result.section_statistics == {}
        assert result.boq_statistics["total_rows"] == 0
        assert result.known_anomalies == []

    def test_no_sections(self):
        rows = [BOQRow(1, "A", "desc", 10.0, "m", "Item", None)]
        result = analyze_boq(rows)
        assert result.section_statistics == {}
        assert result.known_anomalies == []

    def test_unknown_row_type_raises(self):
        rows = [BOQRow(1, "A", "desc", 10.0, "m", "Heading", None)]
        with pytest.raises(ValueError, match="Unknown row type"):
            analyze_boq(rows)

# --- Increment 2 Tests ---
# Evidence: EQ-0010 Spike 4

@pytest.fixture(scope="module")
def intelligence_with_hierarchy(fixture_path):
    """Intelligence result with hierarchy reconstruction enabled."""
    parser = WorkbookParser()
    try:
        parser.load(fixture_path)
        parser.validate()
        rows = extract_boq(parser.workbook)
        return analyze_boq(rows, include_hierarchy=True)
    finally:
        parser.close()

class TestIncrement2BackwardCompatibility:
    """Verify Increment 1 behavior unchanged when hierarchy disabled."""
    
    def test_increment1_without_hierarchy(self, fixture_path):
        """Verify default behavior matches Increment 1 exactly."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result = analyze_boq(rows)  # Default: include_hierarchy=False
        finally:
            parser.close()
        
        # Increment 1 fields present
        assert result.row_classification is not None
        assert result.section_statistics is not None
        assert result.boq_statistics is not None
        assert result.known_anomalies is not None
        
        # Increment 2 fields None when disabled
        assert result.hierarchy is None
        assert result.hierarchy_statistics is None

class TestHierarchyReconstructionDeterminism:
    """Verify reconstruction produces identical results.
    
    Evidence: EQ-0010 Spike 4 (Run 1 == Run 2: True).
    """
    
    def test_hierarchy_determinism(self, fixture_path):
        """Repeated execution produces identical hierarchy."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_hierarchy=True)
            result2 = analyze_boq(rows, include_hierarchy=True)
        finally:
            parser.close()
        
        assert result1.hierarchy == result2.hierarchy
        assert result1.hierarchy_statistics == result2.hierarchy_statistics

class TestHierarchyReconstructionStatistics:
    """Verify reconstruction statistics match Spike 4 evidence.
    
    Evidence: EQ-0010 Spike 4 (2011 headers, 294 roots, 0 orphan items).
    Fixture: tests/fixtures/costx/full_boq.xlsx
    """
    
    def test_total_headers(self, intelligence_with_hierarchy):
        """Verify total headers placed in tree."""
        assert intelligence_with_hierarchy.hierarchy_statistics["total_headers"] == 2011
    
    def test_root_headers(self, intelligence_with_hierarchy):
        """Verify root-level headers."""
        assert intelligence_with_hierarchy.hierarchy_statistics["root_headers"] == 294
        assert len(intelligence_with_hierarchy.hierarchy) == 294
    
    def test_hierarchy_not_none(self, intelligence_with_hierarchy):
        """Verify hierarchy is populated."""
        assert intelligence_with_hierarchy.hierarchy is not None
        assert len(intelligence_with_hierarchy.hierarchy) > 0

class TestHierarchyDepthDistribution:
    """Verify computed depth distribution matches Spike 4 evidence.
    
    Evidence: EQ-0010 Spike 4 (D1:294, D2:397, D3:639, D4:621, D5:60).
    """
    
    def test_depth_distribution(self, intelligence_with_hierarchy):
        """Verify depth distribution from Spike 4."""
        expected = {1: 294, 2: 397, 3: 639, 4: 621, 5: 60}
        actual = intelligence_with_hierarchy.hierarchy_statistics["depth_distribution"]
        assert actual == expected
    
    def test_depth_1_count(self, intelligence_with_hierarchy):
        """Verify depth 1 (root) headers."""
        depth_dist = intelligence_with_hierarchy.hierarchy_statistics["depth_distribution"]
        assert depth_dist[1] == 294
    
    def test_depth_5_count(self, intelligence_with_hierarchy):
        """Verify deepest depth 5 headers."""
        depth_dist = intelligence_with_hierarchy.hierarchy_statistics["depth_distribution"]
        assert depth_dist[5] == 60

class TestHierarchyParentAssignment:
    """Verify parent relationships assigned correctly.
    
    Evidence: EQ-0010 Spike 4 (parent assignment via stack pop).
    """
    
    def test_root_headers_no_parent(self, intelligence_with_hierarchy):
        """All root headers have parent_row_number == None."""
        for node in intelligence_with_hierarchy.hierarchy:
            assert node.parent_row_number is None
            assert node.depth == 1
    
    def test_child_headers_have_parent(self, intelligence_with_hierarchy):
        """All non-root headers have parent_row_number != None."""
        def check_children(node: BOQHeaderNode):
            for child in node.children_headers:
                assert child.parent_row_number is not None
                assert child.parent_row_number == node.row_number
                assert child.depth == node.depth + 1
                check_children(child)
        
        for root in intelligence_with_hierarchy.hierarchy:
            check_children(root)

class TestHierarchyItemsPerHeader:
    """Verify items-per-header computation matches Spike 4 evidence.
    
    Evidence: EQ-0010 Spike 4 (Head1:1.28, Head2:0.66, Head3:1.71, Head4:2.80, Head5:1.92).
    """
    
    def test_items_per_header_head1(self, intelligence_with_hierarchy):
        """Verify Head1 items-per-header ratio."""
        items_per = intelligence_with_hierarchy.hierarchy_statistics["items_per_header_by_uom"]
        assert abs(items_per["Head1"] - 1.28) < 0.01
    
    def test_items_per_header_head2(self, intelligence_with_hierarchy):
        """Verify Head2 items-per-header ratio."""
        items_per = intelligence_with_hierarchy.hierarchy_statistics["items_per_header_by_uom"]
        assert abs(items_per["Head2"] - 0.66) < 0.01
    
    def test_items_per_header_head3(self, intelligence_with_hierarchy):
        """Verify Head3 items-per-header ratio."""
        items_per = intelligence_with_hierarchy.hierarchy_statistics["items_per_header_by_uom"]
        assert abs(items_per["Head3"] - 1.71) < 0.01
    
    def test_items_per_header_head4(self, intelligence_with_hierarchy):
        """Verify Head4 items-per-header ratio."""
        items_per = intelligence_with_hierarchy.hierarchy_statistics["items_per_header_by_uom"]
        assert abs(items_per["Head4"] - 2.80) < 0.01
    
    def test_items_per_header_head5(self, intelligence_with_hierarchy):
        """Verify Head5 items-per-header ratio."""
        items_per = intelligence_with_hierarchy.hierarchy_statistics["items_per_header_by_uom"]
        assert abs(items_per["Head5"] - 1.92) < 0.01

class TestHierarchyNodeStructure:
    """Verify BOQHeaderNode structure is immutable and well-formed."""
    
    def test_header_node_is_frozen(self, intelligence_with_hierarchy):
        """BOQHeaderNode is frozen dataclass."""
        node = intelligence_with_hierarchy.hierarchy[0]
        assert isinstance(node, BOQHeaderNode)
        with pytest.raises(AttributeError):
            node.level = 99
    
    def test_header_node_fields(self, intelligence_with_hierarchy):
        """All expected fields present in BOQHeaderNode."""
        node = intelligence_with_hierarchy.hierarchy[0]
        assert hasattr(node, "level")
        assert hasattr(node, "row_number")
        assert hasattr(node, "uom")
        assert hasattr(node, "description")
        assert hasattr(node, "section")
        assert hasattr(node, "depth")
        assert hasattr(node, "parent_row_number")
        assert hasattr(node, "children_headers")
        assert hasattr(node, "children_items")
    
    def test_children_are_tuples(self, intelligence_with_hierarchy):
        """Children collections are immutable tuples."""
        node = intelligence_with_hierarchy.hierarchy[0]
        assert isinstance(node.children_headers, tuple)
        assert isinstance(node.children_items, tuple)

class TestHierarchyEdgeCases:
    """Test hierarchy reconstruction edge cases."""
    
    def test_empty_rows_hierarchy(self):
        """Empty row list produces empty hierarchy."""
        result = analyze_boq([], include_hierarchy=True)
        assert result.hierarchy == ()
        assert result.hierarchy_statistics["total_headers"] == 0
        assert result.hierarchy_statistics["root_headers"] == 0
    
    def test_no_headers_hierarchy(self):
        """Rows without Head produce empty hierarchy."""
        rows = [BOQRow(1, "A", "desc", 10.0, "m", "Item", None)]
        result = analyze_boq(rows, include_hierarchy=True)
        assert result.hierarchy == ()
        assert result.hierarchy_statistics["total_headers"] == 0
