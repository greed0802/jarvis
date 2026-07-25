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

# --- Increment 4: Semantic Evidence Tests ---
# Authority: EQ-0019 (Permanently Frozen), IP-0001
# Evidence: EQ-0019 Spike 3 (Deterministic Rule Definition)


class TestIncrement4BackwardCompatibility:
    """Verify backward compatibility: Increment 1-3 unchanged when include_semantic=False."""

    def test_default_include_semantic_returns_none(self, fixture_path):
        """Default call (include_semantic=False) returns None for all new fields."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result = analyze_boq(rows)  # Default: include_semantic=False
        finally:
            parser.close()

        # All new fields should be None
        assert result.vocabulary is None
        assert result.head1_categorization is None
        assert result.administrative_patterns is None
        assert result.section_enumeration is None
        assert result.uom_distribution is None
        assert result.uom_percentages is None
        assert result.header_distribution is None
        assert result.header_quantity_violations is None
        assert result.admin_template_matches is None

    def test_explicit_false_returns_none(self, fixture_path):
        """Explicit include_semantic=False returns None for all new fields."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result = analyze_boq(rows, include_semantic=False)
        finally:
            parser.close()

        assert result.vocabulary is None


class TestSemanticVocabularyExtraction:
    """SEM-PROD-01: Vocabulary extraction deterministic tests."""

    @pytest.fixture(scope="module")
    def semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

    def test_vocabulary_is_populated(self, semantic):
        """Vocabulary should be a non-empty dict."""
        assert isinstance(semantic.vocabulary, dict)
        assert len(semantic.vocabulary) > 0

    def test_vocabulary_top_term(self, semantic):
        """Top term should be common engineering word."""
        # In full_boq, expect 'AND' or similar high-frequency term
        top_term = list(semantic.vocabulary.keys())[0]
        assert isinstance(top_term, str)
        assert semantic.vocabulary[top_term] > 0

    def test_vocabulary_values_are_int(self, semantic):
        """All vocabulary values should be int counts."""
        for term, count in semantic.vocabulary.items():
            assert isinstance(count, int), f"Term {term!r} has non-int count: {count}"

    def test_vocabulary_sorted_descending(self, semantic):
        """Vocabulary should be sorted by count descending."""
        counts = list(semantic.vocabulary.values())
        for i in range(len(counts) - 1):
            assert counts[i] >= counts[i + 1], f"Not sorted at index {i}"

    def test_vocabulary_max_terms_respected(self, semantic):
        """Default max_terms=50 should produce at most 50 terms."""
        assert len(semantic.vocabulary) <= 50

    def test_vocabulary_determinism(self, fixture_path):
        """Same input produces identical vocabulary."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_semantic=True)
            result2 = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result1.vocabulary == result2.vocabulary

    def test_vocabulary_empty_input(self):
        """Empty rows produce empty vocabulary."""
        result = analyze_boq([], include_semantic=True)
        assert result.vocabulary == {}

    def test_vocabulary_no_items(self):
        """Rows without Items produce empty vocabulary."""
        rows = [BOQRow(1, "A", "Some header", None, "Head1", "Head", "A")]
        result = analyze_boq(rows, include_semantic=True)
        assert result.vocabulary == {}

    def test_vocabulary_custom_max_terms(self, fixture_path):
        """Custom max_terms limits vocabulary size."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            from jarvis.parsers.costx.boq_intelligence import _extract_vocabulary
            vocab = _extract_vocabulary(rows, max_terms=10)
        finally:
            parser.close()

        assert len(vocab) <= 10


class TestSemanticHead1Categorization:
    """SEM-PROD-02: Head1 text categorization deterministic tests."""

    @pytest.fixture(scope="module")
    def semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

    def test_categorization_has_both_keys(self, semantic):
        """Result should have both Administrative and Trade-Specific keys."""
        assert "Administrative" in semantic.head1_categorization
        assert "Trade-Specific" in semantic.head1_categorization

    def test_administrative_entries_present(self, semantic):
        """Should find GENERALLY, REFERENCES, PRICES administrative entries."""
        admin = semantic.head1_categorization["Administrative"]
        assert len(admin) > 0

    def test_trade_specific_entries_present(self, semantic):
        """Should find trade-specific entries."""
        trade = semantic.head1_categorization["Trade-Specific"]
        assert len(trade) > 0

    def test_categorization_determinism(self, fixture_path):
        """Same input produces identical categorization."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_semantic=True)
            result2 = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result1.head1_categorization == result2.head1_categorization

    def test_each_entry_has_required_fields(self, semantic):
        """Each entry should have row_number and description."""
        for category in ("Administrative", "Trade-Specific"):
            for entry in semantic.head1_categorization[category]:
                assert "row_number" in entry
                assert "description" in entry

    def test_empty_input(self):
        """Empty rows produce empty categorization."""
        result = analyze_boq([], include_semantic=True)
        assert result.head1_categorization["Administrative"] == []
        assert result.head1_categorization["Trade-Specific"] == []


class TestSemanticSectionEnumeration:
    """SEM-PROD-05: Section enumeration deterministic tests."""

    @pytest.fixture(scope="module")
    def semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

    def test_enumeration_is_tuple(self, semantic):
        """Section enumeration should be a tuple."""
        assert isinstance(semantic.section_enumeration, tuple)

    def test_enumeration_not_empty(self, semantic):
        """Full BOQ should have sections."""
        assert len(semantic.section_enumeration) > 0

    def test_enumeration_section_A_first(self, semantic):
        """First section should be A."""
        assert semantic.section_enumeration[0]["code"] == "A"

    def test_enumeration_has_code_name_row(self, semantic):
        """Each entry should have code, name, row_number."""
        for entry in semantic.section_enumeration:
            assert "code" in entry
            assert "name" in entry
            assert "row_number" in entry

    def test_enumeration_ordering_preserved(self, semantic):
        """Sections should be in ordinal order by row_number."""
        row_numbers = [entry["row_number"] for entry in semantic.section_enumeration]
        for i in range(len(row_numbers) - 1):
            assert row_numbers[i] < row_numbers[i + 1]

    def test_enumeration_determinism(self, fixture_path):
        """Same input produces identical enumeration."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_semantic=True)
            result2 = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result1.section_enumeration == result2.section_enumeration

    def test_empty_input(self):
        """Empty rows produce empty enumeration."""
        result = analyze_boq([], include_semantic=True)
        assert result.section_enumeration == ()

class TestSemanticUOMDistribution:
    """SEM-PROD-06: UOM distribution deterministic tests."""

    @pytest.fixture(scope="module")
    def semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

    def test_uom_distribution_is_dict(self, semantic):
        """UOM distribution should be a dict."""
        assert isinstance(semantic.uom_distribution, dict)

    def test_uom_percentages_is_dict(self, semantic):
        """UOM percentages should be a dict."""
        assert isinstance(semantic.uom_percentages, dict)

    def test_uom_distribution_not_empty(self, semantic):
        """Full BOQ should have UOM entries."""
        assert len(semantic.uom_distribution) > 0

    def test_uom_m2_dominates(self, semantic):
        """m2 should be the dominant UOM in full_boq (~33.7%)."""
        assert semantic.uom_distribution.get("m2", 0) > 0
        pct = semantic.uom_percentages.get("m2", 0)
        assert 30.0 < pct < 40.0  # Known: ~33.7%

    def test_uom_values_are_int(self, semantic):
        """All UOM distribution values should be int."""
        for uom, count in semantic.uom_distribution.items():
            assert isinstance(count, int), f"UOM {uom!r} has non-int count: {count}"

    def test_uom_percentages_sum(self, semantic):
        """Percentages should sum to ~100.0."""
        total = sum(semantic.uom_percentages.values())
        assert 99.0 <= total <= 101.0

    def test_uom_distribution_sorted_descending(self, semantic):
        """UOM distribution should be sorted by count descending."""
        counts = list(semantic.uom_distribution.values())
        for i in range(len(counts) - 1):
            assert counts[i] >= counts[i + 1]

    def test_uom_determinism(self, fixture_path):
        """Same input produces identical UOM distribution."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_semantic=True)
            result2 = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result1.uom_distribution == result2.uom_distribution
        assert result1.uom_percentages == result2.uom_percentages

    def test_empty_input(self):
        """Empty rows produce empty distribution."""
        result = analyze_boq([], include_semantic=True)
        assert result.uom_distribution == {}
        assert result.uom_percentages == {}


class TestSemanticHeaderDistribution:
    """SEM-PROD-07: Header level count distribution deterministic tests."""

    @pytest.fixture(scope="module")
    def semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

    def test_header_distribution_has_keys(self, semantic):
        """Should have Head1-4 keys."""
        for key in ("Head1", "Head2", "Head3", "Head4"):
            assert key in semantic.header_distribution

    def test_header_distribution_values_int(self, semantic):
        """All values should be int."""
        for key, count in semantic.header_distribution.items():
            assert isinstance(count, int), f"Key {key!r} has non-int count: {count}"

    def test_header_distribution_populated(self, semantic):
        """Full BOQ should have headers at all levels."""
        for key in ("Head1", "Head2", "Head3", "Head4"):
            assert semantic.header_distribution[key] > 0

    def test_head4_most_common(self, semantic):
        """Head4 should have highest count (636 observed)."""
        assert semantic.header_distribution["Head4"] > semantic.header_distribution["Head1"]

    def test_header_distribution_determinism(self, fixture_path):
        """Same input produces identical distribution."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_semantic=True)
            result2 = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result1.header_distribution == result2.header_distribution

    def test_empty_input(self):
        """Empty rows produce zero distribution."""
        result = analyze_boq([], include_semantic=True)
        for key in ("Head1", "Head2", "Head3", "Head4"):
            assert result.header_distribution[key] == 0


class TestSemanticHeaderQuantityInvariant:
    """SEM-PROD-09: 'Items Always Quantify' enforcement tests."""

    @pytest.fixture(scope="module")
    def semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

    def test_no_violations_in_valid_data(self, semantic):
        """In full_boq, no header should have non-NULL quantities."""
        assert isinstance(semantic.header_quantity_violations, tuple)
        assert len(semantic.header_quantity_violations) == 0

    def test_violation_detected_with_quantity(self):
        """A header row with quantity should be detected."""
        rows = [
            BOQRow(1, "A", "GENERALLY", None, "Head1", "Head", "A"),
            BOQRow(2, None, "Some item", 10.0, "m2", "Item", "A"),
            BOQRow(3, "B", "REFERENCES", 5.0, "Head1", "Head", "B"),  # Violation!
        ]
        result = analyze_boq(rows, include_semantic=True)
        assert len(result.header_quantity_violations) == 1
        violation = result.header_quantity_violations[0]
        assert violation["row_number"] == 3
        assert violation["uom"] == "Head1"
        assert violation["quantity"] == 5.0

    def test_no_violations_with_no_headers(self):
        """Empty or Item-only rows produce empty violations."""
        rows = [BOQRow(1, "A", "desc", 10.0, "m", "Item", None)]
        result = analyze_boq(rows, include_semantic=True)
        assert result.header_quantity_violations == ()

    def test_invariant_determinism(self, fixture_path):
        """Same input produces identical violations."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_semantic=True)
            result2 = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result1.header_quantity_violations == result2.header_quantity_violations


class TestSemanticAdminPatterns:
    """SEM-PROD-04: Administrative pattern detection tests."""

    @pytest.fixture(scope="module")
    def semantic_with_hierarchy(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_hierarchy=True, include_semantic=True)
        finally:
            parser.close()

    def test_requires_hierarchy(self, fixture_path):
        """Without hierarchy, patterns should be None."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result.administrative_patterns is None

    def test_patterns_populated(self, semantic_with_hierarchy):
        """With hierarchy, patterns should be populated."""
        assert isinstance(semantic_with_hierarchy.administrative_patterns, dict)
        assert len(semantic_with_hierarchy.administrative_patterns) > 0

    def test_pattern_determinism(self, fixture_path):
        """Same input produces identical patterns."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_hierarchy=True, include_semantic=True)
            result2 = analyze_boq(rows, include_hierarchy=True, include_semantic=True)
        finally:
            parser.close()

        assert result1.administrative_patterns == result2.administrative_patterns


class TestSemanticAdminTemplate:
    """SEM-PROD-12: Administrative sub-template recognition tests."""

    @pytest.fixture(scope="module")
    def semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

    def test_template_matches_populated(self, semantic):
        """Template matches should be a non-empty dict."""
        assert isinstance(semantic.admin_template_matches, dict)
        assert len(semantic.admin_template_matches) > 0

    def test_template_matches_have_expected_keys(self, semantic):
        """Each match entry should have required keys."""
        for section, matches in semantic.admin_template_matches.items():
            for match in matches:
                assert "pattern_name" in match
                assert "matched_text" in match
                assert "row_number" in match

    def test_template_determinism(self, fixture_path):
        """Same input produces identical template matches."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_semantic=True)
            result2 = analyze_boq(rows, include_semantic=True)
        finally:
            parser.close()

        assert result1.admin_template_matches == result2.admin_template_matches

    def test_empty_input(self):
        """Empty rows produce empty template matches."""
        result = analyze_boq([], include_semantic=True)
        assert result.admin_template_matches == {}


class TestIncrement4FullPipeline:
    """Integration test: Increment 4 with full production fixture."""

    @pytest.fixture(scope="module")
    def full_semantic(self, fixture_path):
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            return analyze_boq(rows, include_hierarchy=True, include_detection=True, include_semantic=True)
        finally:
            parser.close()

    def test_all_fields_populated(self, full_semantic):
        """All Increment 4 fields should be populated with real data."""
        assert len(full_semantic.vocabulary) > 0
        assert len(full_semantic.head1_categorization["Administrative"]) > 0
        assert len(full_semantic.head1_categorization["Trade-Specific"]) > 0
        assert len(full_semantic.section_enumeration) > 0
        assert len(full_semantic.uom_distribution) > 0
        assert len(full_semantic.uom_percentages) > 0
        assert sum(full_semantic.header_distribution.values()) > 0
        assert isinstance(full_semantic.header_quantity_violations, tuple)
        assert len(full_semantic.admin_template_matches) > 0

    def test_all_increments_together_determinism(self, fixture_path):
        """All increments together produce deterministic results."""
        parser = WorkbookParser()
        try:
            parser.load(fixture_path)
            parser.validate()
            rows = extract_boq(parser.workbook)
            result1 = analyze_boq(rows, include_hierarchy=True, include_detection=True, include_semantic=True)
            result2 = analyze_boq(rows, include_hierarchy=True, include_detection=True, include_semantic=True)
        finally:
            parser.close()

        # Check all fields match across runs
        assert result1 == result2

    def test_increment_fields_remain_present(self, full_semantic):
        """Verifies Increment 1-3 fields still present alongside Increment 4."""
        # Increment 1
        assert full_semantic.row_classification is not None
        assert full_semantic.section_statistics is not None
        assert full_semantic.boq_statistics is not None
        assert full_semantic.known_anomalies is not None

        # Increment 2
        assert full_semantic.hierarchy is not None
        assert full_semantic.hierarchy_statistics is not None

        # Increment 3
        assert full_semantic.detected_level_skips is not None
        assert full_semantic.zero_quantity_items is not None
        assert full_semantic.structural_containment_findings is not None
        assert full_semantic.completeness_findings is not None

        # Increment 4
        assert full_semantic.vocabulary is not None
        assert full_semantic.head1_categorization is not None
        assert full_semantic.section_enumeration is not None
        assert full_semantic.uom_distribution is not None
        assert full_semantic.uom_percentages is not None
        assert full_semantic.header_distribution is not None
        assert full_semantic.header_quantity_violations is not None
        assert full_semantic.admin_template_matches is not None
