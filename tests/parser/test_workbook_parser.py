"""Tests for M6.1 WorkbookParser skeleton.

Verifies:
- parser object can be created
- valid workbook loads successfully
- missing workbook raises appropriate exception
- workbook reference is retained
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jarvis.parsers.costx.workbook_parser import WorkbookParser


class TestWorkbookParserCreation:
    """Test WorkbookParser object creation."""

    def test_parser_object_can_be_created(self) -> None:
        """WorkbookParser can be instantiated."""
        parser = WorkbookParser()
        assert parser is not None

    def test_parser_starts_unloaded(self) -> None:
        """Parser starts with no workbook loaded."""
        parser = WorkbookParser()
        assert parser.is_loaded is False
        assert parser.workbook is None
        assert parser.path is None


class TestWorkbookLoading:
    """Test workbook loading behavior."""

    def test_valid_workbook_loads_successfully(self) -> None:
        """Parser loads a valid workbook and retains reference."""
        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        assert parser.is_loaded is True
        assert parser.workbook is not None
        assert parser.path == workbook_path

        parser.close()
        assert parser.is_loaded is False

    def test_missing_workbook_raises_file_not_found(self) -> None:
        """Missing workbook raises FileNotFoundError."""
        parser = WorkbookParser()
        missing_path = Path("tests/fixtures/costx/nonexistent.xlsx")

        with pytest.raises(FileNotFoundError, match="Workbook not found"):
            parser.load(missing_path)

        assert parser.is_loaded is False

    def test_directory_path_raises_file_not_found(self) -> None:
        """Directory path raises FileNotFoundError."""
        parser = WorkbookParser()
        directory_path = Path("tests/fixtures/costx")

        with pytest.raises(FileNotFoundError, match="Path is not a file"):
            parser.load(directory_path)

        assert parser.is_loaded is False

    def test_close_clears_workbook_reference(self) -> None:
        """Close method clears the workbook reference."""
        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)
        assert parser.is_loaded is True

        parser.close()
        assert parser.is_loaded is False
        assert parser.workbook is None
        assert parser.path is None


class TestWorkbookObserve:
    """Test WorkbookParser.observe() method for ObservationSet emission."""

    def test_observe_returns_observationset(self) -> None:
        """observe() returns an ObservationSet instance."""
        from jarvis.parsers.observation import ObservationSet

        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        result = parser.observe()

        assert isinstance(result, ObservationSet)
        assert result.acquisition_id is not None
        assert result.timestamp is not None

        parser.close()

    def test_observe_raises_runtime_error_without_workbook(self) -> None:
        """observe() raises RuntimeError when no workbook loaded."""
        parser = WorkbookParser()

        with pytest.raises(RuntimeError, match="Cannot validate: no workbook loaded"):
            parser.observe()

    def test_observationset_contains_workbook_observation(self) -> None:
        """ObservationSet contains a WorkbookObservation as first element."""
        from jarvis.parsers.observation import WorkbookObservation

        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        result = parser.observe()

        assert len(result.observations) >= 1
        assert isinstance(result.observations[0], WorkbookObservation)

        parser.close()

    def test_observationset_contains_worksheet_observation(self) -> None:
        """ObservationSet contains a WorksheetObservation."""
        from jarvis.parsers.observation import WorksheetObservation

        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        result = parser.observe()

        # Find the WorksheetObservation
        ws_obs = next(
            (obs for obs in result.observations if isinstance(obs, WorksheetObservation)),
            None
        )
        assert ws_obs is not None
        assert ws_obs.worksheet_name == "CostX"
        assert ws_obs.row_count >= 1

        parser.close()

    def test_observationset_contains_row_observations(self) -> None:
        """ObservationSet contains RowObservations for each row."""
        from jarvis.parsers.observation import RowObservation

        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        result = parser.observe()

        # Count RowObservations
        row_count = sum(1 for obs in result.observations if isinstance(obs, RowObservation))
        assert row_count >= 1

        parser.close()

    def test_observationset_contains_cell_observations(self) -> None:
        """ObservationSet contains CellObservations for each cell."""
        from jarvis.parsers.observation import CellObservation

        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        result = parser.observe()

        # Count CellObservations
        cell_count = sum(1 for obs in result.observations if isinstance(obs, CellObservation))
        assert cell_count >= 1

        parser.close()

    def test_observation_has_provenance(self) -> None:
        """Each observation has valid provenance with source, observer, procedure."""
        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        result = parser.observe()

        for obs in result.observations:
            assert obs.provenance.source_identifier == str(workbook_path)
            assert obs.provenance.observer == "WorkbookParser"
            assert obs.provenance.procedure == "CostX workbook observation"
            assert obs.provenance.timestamp is not None

        parser.close()

    def test_observations_are_immutable(self) -> None:
        """Observations returned cannot be modified (frozen dataclass)."""
        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)

        result = parser.observe()

        # Attempt to modify an observation should raise
        wb_obs = result.observations[0]
        with pytest.raises(AttributeError):
            wb_obs.worksheet_count = 999  # type: ignore[attr-defined]

        parser.close()
