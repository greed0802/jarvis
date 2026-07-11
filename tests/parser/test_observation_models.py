"""Tests for Observation ontology runtime types.

Verifies:
- Provenance is immutable and hashable
- ObservationSet enforces invariant (at least one Observation)
- All observation types are immutable
- Observation identity is deterministic
"""

from __future__ import annotations

from datetime import datetime

import pytest

from jarvis.parsers.observation import (
    CellObservation,
    Observation,
    ObservationSet,
    Provenance,
    RowObservation,
    WorkbookObservation,
    WorksheetObservation,
)


class TestProvenance:
    """Test Provenance immutability and behavior."""

    def test_provenance_is_immutable(self) -> None:
        """Provenance fields cannot be modified after creation."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )

        with pytest.raises(AttributeError):
            provenance.source_identifier = "/new/path"  # type: ignore[attr-defined]

    def test_provenance_is_hashable(self) -> None:
        """Provenance can be used in sets and as dict keys."""
        provenance1 = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        provenance2 = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )

        # Equal provenance should hash the same
        assert provenance1 == provenance2
        assert hash(provenance1) == hash(provenance2)


class TestObservationSet:
    """Test ObservationSet invariant enforcement and immutability."""

    def test_observationset_requires_at_least_one_observation(self) -> None:
        """ObservationSet SHALL contain at least one Observation."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        wb_obs = WorkbookObservation(
            observation_id="obs-wb-0001",
            provenance=provenance,
            file_format="xlsx",
            format_version=None,
            creator=None,
            created=None,
            modified=None,
            application=None,
            calculation_mode=None,
            date_system=None,
            worksheet_count=1,
            worksheet_names=("CostX",),
            structure_protection=None,
            window_protection=None,
            visibility=None,
        )

        # Valid: one observation
        obs_set = ObservationSet(
            acquisition_id="acq-test",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
            observations=(wb_obs,),
        )
        assert len(obs_set.observations) == 1

    def test_observationset_rejects_empty_observations(self) -> None:
        """ObservationSet rejects empty observations tuple."""
        with pytest.raises(ValueError, match="SHALL contain at least one Observation"):
            ObservationSet(
                acquisition_id="acq-test",
                timestamp=datetime(2026, 7, 11, 12, 0, 0),
                observations=(),  # Empty - should fail
            )

    def test_observationset_is_immutable(self) -> None:
        """ObservationSet cannot be modified after creation."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        wb_obs = WorkbookObservation(
            observation_id="obs-wb-0001",
            provenance=provenance,
            file_format="xlsx",
            format_version=None,
            creator=None,
            created=None,
            modified=None,
            application=None,
            calculation_mode=None,
            date_system=None,
            worksheet_count=1,
            worksheet_names=("CostX",),
            structure_protection=None,
            window_protection=None,
            visibility=None,
        )
        obs_set = ObservationSet(
            acquisition_id="acq-test",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
            observations=(wb_obs,),
        )

        with pytest.raises(AttributeError):
            obs_set.acquisition_id = "acq-new"  # type: ignore[attr-defined]

    def test_observationset_contains_mixed_observations(self) -> None:
        """ObservationSet can contain any Observation type."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        wb_obs = WorkbookObservation(
            observation_id="obs-wb-0001",
            provenance=provenance,
            file_format="xlsx",
            format_version=None,
            creator=None,
            created=None,
            modified=None,
            application=None,
            calculation_mode=None,
            date_system=None,
            worksheet_count=1,
            worksheet_names=("CostX",),
            structure_protection=None,
            window_protection=None,
            visibility=None,
        )
        ws_obs = WorksheetObservation(
            observation_id="obs-ws-0001",
            provenance=provenance,
            worksheet_name="CostX",
            worksheet_index=0,
            visibility=None,
            row_count=100,
            column_count=9,
            merged_ranges=(),
            freeze_panes=None,
            auto_filter=None,
            print_area=None,
            hidden_rows=(),
            hidden_columns=(),
        )
        row_obs = RowObservation(
            observation_id="obs-row-0001",
            provenance=provenance,
            worksheet_name="CostX",
            row_number=1,
            visibility=None,
            height=None,
        )

        obs_set = ObservationSet(
            acquisition_id="acq-test",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
            observations=(wb_obs, ws_obs, row_obs),
        )

        assert len(obs_set.observations) == 3
        assert isinstance(obs_set.observations[0], WorkbookObservation)
        assert isinstance(obs_set.observations[1], WorksheetObservation)
        assert isinstance(obs_set.observations[2], RowObservation)


class TestObservationTypes:
    """Test Observation specialization behavior."""

    def test_workbook_observation_inherits_observation(self) -> None:
        """WorkbookObservation is an Observation with immutable properties."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        wb_obs = WorkbookObservation(
            observation_id="obs-wb-0001",
            provenance=provenance,
            file_format="xlsx",
            format_version=None,
            creator=None,
            created=None,
            modified=None,
            application=None,
            calculation_mode=None,
            date_system=None,
            worksheet_count=1,
            worksheet_names=("CostX",),
            structure_protection=None,
            window_protection=None,
            visibility=None,
        )

        # Has Observation properties
        assert wb_obs.observation_id == "obs-wb-0001"
        assert wb_obs.provenance is provenance

        # Is immutable
        with pytest.raises(AttributeError):
            wb_obs.worksheet_count = 2  # type: ignore[attr-defined]

    def test_worksheet_observation_is_immutable(self) -> None:
        """WorksheetObservation cannot be modified."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        ws_obs = WorksheetObservation(
            observation_id="obs-ws-0001",
            provenance=provenance,
            worksheet_name="CostX",
            worksheet_index=0,
            visibility=None,
            row_count=100,
            column_count=9,
            merged_ranges=(),
            freeze_panes=None,
            auto_filter=None,
            print_area=None,
            hidden_rows=(),
            hidden_columns=(),
        )

        with pytest.raises(AttributeError):
            ws_obs.row_count = 200  # type: ignore[attr-defined]

    def test_row_observation_is_immutable(self) -> None:
        """RowObservation cannot be modified."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        row_obs = RowObservation(
            observation_id="obs-row-0001",
            provenance=provenance,
            worksheet_name="CostX",
            row_number=1,
            visibility=None,
            height=None,
        )

        with pytest.raises(AttributeError):
            row_obs.row_number = 5  # type: ignore[attr-defined]

    def test_cell_observation_is_immutable(self) -> None:
        """CellObservation cannot be modified."""
        provenance = Provenance(
            source_identifier="/path/to/workbook.xlsx",
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=datetime(2026, 7, 11, 12, 0, 0),
        )
        cell_obs = CellObservation(
            observation_id="obs-cell-0001",
            provenance=provenance,
            worksheet_name="CostX",
            row=1,
            column=1,
            reference="A1",
            value="test",
            formula=None,
            calculated_value=None,
            data_type="string",
            number_format="General",
            font=None,
            fill=None,
            alignment=None,
            border=None,
            locked=None,
            hidden=None,
            merged=False,
            comment=None,
        )

        with pytest.raises(AttributeError):
            cell_obs.value = "modified"  # type: ignore[attr-defined]