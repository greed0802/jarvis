"""Acceptance tests for BOQ Intelligence Increment 1.

Verifies the production pipeline:
    WorkbookParser → extract_boq() → analyze_boq()

All expected values imported from tests/reference/eq0007_evidence.py.
Fixture integrity verified via tests/fixtures/FIXTURE_METADATA.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
from jarvis.parsers.costx.boq_intelligence import (
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