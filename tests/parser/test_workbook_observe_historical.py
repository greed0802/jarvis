"""Historical tests for WorkbookParser.observe() integration.

ADR-0025 (2026-07-11) evaluated and rejected the Observation Runtime as the active
production architecture. The observe() method is not part of the supported production
parser interface and these tests are preserved for historical reference only.

See: docs/decisions/ADR_0025_Observation_Runtime_Architecture.md

These tests were relocated from test_workbook_parser.py after ADR-0025 disposition.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jarvis.parsers.costx.workbook_parser import WorkbookParser


class TestWorkbookObserveHistorical:
    """Historical test for WorkbookParser.observe() method.

    NOTE: These tests are for historical reference only. The observe() method
    was removed from WorkbookParser as part of ADR-0025 disposition.
    """

    def test_observe_returns_observationset(self) -> None:
        """observe() returns an ObservationSet instance."""
        from jarvis.parsers.observation import ObservationSet

        # This test documents historical behavior
        # WorkbookParser.observe() was removed - this class preserved for reference
        pytest.skip("Historical test: observe() method was removed")

    def test_observe_raises_runtime_error_without_workbook(self) -> None:
        """observe() raises RuntimeError when no workbook loaded."""
        pytest.skip("Historical test: observe() method was removed")

    def test_observationset_contains_workbook_observation(self) -> None:
        """ObservationSet contains a WorkbookObservation as first element."""
        pytest.skip("Historical test: observe() method was removed")

    def test_observationset_contains_worksheet_observation(self) -> None:
        """ObservationSet contains a WorksheetObservation."""
        pytest.skip("Historical test: observe() method was removed")

    def test_observationset_contains_row_observations(self) -> None:
        """ObservationSet contains RowObservations for each row."""
        pytest.skip("Historical test: observe() method was removed")

    def test_observationset_contains_cell_observations(self) -> None:
        """ObservationSet contains CellObservations for each cell."""
        pytest.skip("Historical test: observe() method was removed")

    def test_observation_has_provenance(self) -> None:
        """Each observation has valid provenance with source, observer, procedure."""
        pytest.skip("Historical test: observe() method was removed")

    def test_observations_are_immutable(self) -> None:
        """Observations returned cannot be modified (frozen dataclass)."""
        pytest.skip("Historical test: observe() method was removed")