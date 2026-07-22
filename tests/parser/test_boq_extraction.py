"""Tests for deterministic BOQ row extraction (EQ-0007)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from jarvis.parsers.costx.boq_extraction import BOQRow, extract_boq
from jarvis.parsers.costx.loader import load_workbook


FIXTURE = Path(__file__).parent.parent / "fixtures" / "costx" / "full_boq.xlsx"


@pytest.fixture
def loaded_workbook():
    """Load the full_boq.xlsx fixture for extraction testing."""
    wb = load_workbook(FIXTURE, data_only=True)
    yield wb
    wb.close()


@pytest.fixture
def extracted_rows(loaded_workbook):
    """Extract rows once for reuse across tests."""
    return extract_boq(loaded_workbook)


class TestBOQExtractionCounts:
    """Verify that extraction from full_boq.xlsx produces expected counts."""

    def test_total_row_count(self, extracted_rows):
        assert len(extracted_rows) == 6349

    def test_classification_counts(self, extracted_rows):
        counts = {"Head": 0, "Note": 0, "Section": 0, "Item": 0, "Other": 0}
        for row in extracted_rows:
            counts[row.row_type] += 1
        assert counts["Head"] == 2011
        assert counts["Note"] == 520
        assert counts["Section"] == 15
        assert counts["Item"] == 3605
        assert counts["Other"] == 198


class TestBOQRowStructure:
    """Verify that BOQRow objects contain correct field values."""

    def test_row_has_all_fields(self, extracted_rows):
        for r in extracted_rows:
            assert hasattr(r, "row_number")
            assert hasattr(r, "code")
            assert hasattr(r, "description")
            assert hasattr(r, "quantity")
            assert hasattr(r, "uom")
            assert hasattr(r, "row_type")
            assert hasattr(r, "section")

    def test_row_types_are_valid(self, extracted_rows):
        valid_types = {"Head", "Note", "Section", "Item", "Other"}
        for r in extracted_rows:
            assert r.row_type in valid_types


class TestBOQSectionPropagation:
    """Verify that section context propagates correctly."""

    def test_pre_omission_section_none(self, extracted_rows):
        # First OMISSION marker row is 5864, which already carries section="OMISSION"
        pre_omission = [r for r in extracted_rows if r.row_number < 5864]
        assert all(r.section is None for r in pre_omission)

    def test_omission_section_propagated(self, extracted_rows):
        omission_rows = [r for r in extracted_rows if r.section == "OMISSION"]
        assert len(omission_rows) > 0

    def test_addition_section_propagated(self, extracted_rows):
        addition_rows = [r for r in extracted_rows if r.section == "ADDITION"]
        assert len(addition_rows) > 0

    def test_section_types(self, extracted_rows):
        valid_sections = {None, "OMISSION", "ADDITION"}
        for r in extracted_rows:
            assert r.section in valid_sections


class TestBOQOmissionAnomalies:
    """Verify reproduction of the seven known OMISSION anomalies."""

    def test_seven_anomalies_detected(self, extracted_rows):
        anomalies = [
            (r.row_number, r.code, r.quantity)
            for r in extracted_rows
            if r.section == "OMISSION"
            and r.quantity is not None
            and r.quantity > 0
        ]
        expected = [
            (6202, "BE/2", 21),
            (6343, "BH/24", 6),
            (6344, "BH/25", 4),
            (6345, "BH/26", 1),
            (6346, "BH/27", 3),
            (6347, "BH/28", 5),
            (6348, "BH/29", 5),
        ]
        assert len(anomalies) == 7
        for anomaly in expected:
            assert anomaly in anomalies


class TestBOQDeterministic:
    """Verify that extraction is deterministic."""

    def test_deterministic_results(self, loaded_workbook):
        rows_1 = extract_boq(loaded_workbook)
        rows_2 = extract_boq(loaded_workbook)
        assert len(rows_1) == len(rows_2)
        for r1, r2 in zip(rows_1, rows_2):
            assert r1.row_number == r2.row_number
            assert r1.row_type == r2.row_type
            assert r1.section == r2.section