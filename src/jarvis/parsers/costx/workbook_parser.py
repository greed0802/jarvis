"""Deterministic CostX workbook parser.

This module provides the initial implementation of the CostX workbook parser.

M6.1 establishes the parser lifecycle only:
- load a workbook
- retain a workbook reference
- release workbook resources

M6.2 adds workbook validation for the supported format.

Observable property acquisition produces immutable ObservationSet instances.

WorkbookObservation, WorksheetObservation, RowObservation, CellObservation
are acquired from the loaded workbook without interpretation.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path

from openpyxl.workbook.workbook import Workbook

from jarvis.parsers.costx.loader import load_workbook
from jarvis.parsers.observation import (
    CellObservation,
    Observation,
    ObservationSet,
    Provenance,
    RowObservation,
    WorkbookObservation,
    WorksheetObservation,
)


class WorkbookParser:
    """Deterministic CostX workbook parser.

    WorkbookParser is an Observer in the ontological sense.
    It executes a Procedure to acquire observable properties from workbook Sources
    and produces an immutable ObservationSet containing Observations.

    The single Procedure for acquisition is "CostX workbook observation".
    Individual Observation types distinguish the level of observation.
    """

    def __init__(self) -> None:
        """Initialize the parser with no workbook loaded."""
        self._workbook: Workbook | None = None
        self._path: Path | None = None

    def load(self, workbook_path: Path) -> None:
        """Load a workbook for future parsing.

        Args:
            workbook_path: Path to the CostX BOQ workbook (.xlsx file).

        Raises:
            FileNotFoundError: If the workbook file does not exist.
        """
        if not workbook_path.exists():
            raise FileNotFoundError(f"Workbook not found: {workbook_path}")

        if not workbook_path.is_file():
            raise FileNotFoundError(f"Path is not a file: {workbook_path}")

        # Delegate workbook loading to the CostX loader.
        # The loader encapsulates workbook compatibility behavior.
        self._path = workbook_path
        self._workbook = load_workbook(workbook_path)

    @property
    def workbook(self) -> Workbook | None:
        """Get the loaded workbook reference.

        Returns:
            The openpyxl Workbook instance if loaded, None otherwise.

        Note:
            This property is retained for backward compatibility.
            Production code should use observe() instead.

        TODO(M7): Remove after downstream migration.
        """
        return self._workbook

    @property
    def path(self) -> Path | None:
        """Return the loaded workbook path.

        Returns:
            The Path of the loaded workbook if loaded, None otherwise.

        Note:
            This property is retained for backward compatibility.
            Production code should use observe() instead.

        TODO(M7): Remove after downstream migration.
        """
        return self._path

    @property
    def is_loaded(self) -> bool:
        """Check if a workbook is currently loaded.

        Returns:
            True if a workbook is loaded, False otherwise.
        """
        return self._workbook is not None

    def validate(self) -> None:
        """Validate the loaded workbook matches the supported CostX BOQ format.

        Validates:
        - Workbook is loaded
        - Workbook contains worksheet "CostX"
        - Workbook contains exactly one worksheet
        - Worksheet is not empty

        Raises:
            RuntimeError: If workbook is not loaded.
            ValueError: If workbook does not match the supported format.
        """
        # Check workbook is loaded
        workbook = self._workbook
        if workbook is None:
            raise RuntimeError("Cannot validate: no workbook loaded")

        sheet_names = workbook.sheetnames

        # Validate exactly one worksheet
        if len(sheet_names) != 1:
            raise ValueError(
                f"Expected exactly 1 worksheet, found {len(sheet_names)}"
            )

        # Validate worksheet named "CostX"
        if sheet_names[0] != "CostX":
            raise ValueError(
                f"Expected worksheet named 'CostX', found '{sheet_names[0]}'"
            )

        # Validate worksheet is not empty
        # Use the known worksheet name since we validated above
        ws = workbook["CostX"]
        if ws.max_row < 1:
            raise ValueError("Worksheet is empty")

    def observe(self) -> ObservationSet:
        """Acquire observable properties and return an immutable ObservationSet.

        The ObservationSet contains:
        - WorkbookObservation (workbook-level properties)
        - WorksheetObservation (worksheet-level properties)
        - RowObservation (one per row in the worksheet)
        - CellObservation (one per cell in the worksheet)

        All observations are immutable and have deterministic identity
        based on their position within the acquisition run.

        Raises:
            RuntimeError: If no workbook is loaded.
            ValueError: If workbook does not match the supported format.

        Returns:
            An immutable ObservationSet containing all observations.
        """
        # Validate preconditions to ensure parser contract
        self.validate()

        workbook = self._workbook
        if workbook is None:
            # This should not happen after validate(), but guard anyway
            raise RuntimeError("Cannot observe: no workbook loaded")

        # Create acquisition session metadata
        timestamp = datetime.now()
        observations: list[Observation] = []

        # Build shared provenance for this acquisition run
        # Single Procedure: "CostX workbook observation"
        # This is the Procedure name for the entire acquisition process
        source_identifier = str(self._path) if self._path else ""

        # Build deterministic acquisition ID
        # Combines source identifier with workbook structural fingerprint
        acquisition_id = self._compute_structural_id(source_identifier, workbook)

        shared_provenance = Provenance(
            source_identifier=source_identifier,
            observer="WorkbookParser",
            procedure="CostX workbook observation",
            timestamp=timestamp,
        )

        # Acquire WorkbookObservation
        wb_observation = self._acquire_workbook_observation(workbook, shared_provenance)
        observations.append(wb_observation)

        # Acquire WorksheetObservation
        ws_observation = self._acquire_worksheet_observation(workbook, shared_provenance)
        observations.append(ws_observation)

        # Acquire RowObservation and CellObservation
        row_cell_observations = self._acquire_row_and_cell_observations(workbook, shared_provenance)
        observations.extend(row_cell_observations)

        return ObservationSet(
            acquisition_id=acquisition_id,
            timestamp=timestamp,
            observations=tuple(observations),
        )

    @staticmethod
    def _compute_structural_id(source_identifier: str, workbook: Workbook) -> str:
        """Compute deterministic acquisition ID from source and workbook structure.

        The ID is reproducible for the same source under equivalent conditions.
        This is a structural fingerprint based on workbook dimensions, not a
        content fingerprint of all cell values.

        Args:
            source_identifier: Path or identifier of the source workbook.
            workbook: The loaded workbook to fingerprint.

        Returns:
            A deterministic acquisition identifier.
        """
        # Create a fingerprint from workbook structural properties
        # This ensures reproducibility while avoiding content scanning
        fingerprint_parts = [
            source_identifier,
            str(workbook.sheetnames),
        ]

        # Add row/column count of each worksheet for basic structural fingerprint
        for sheet in workbook.sheetnames:
            ws = workbook[sheet]
            fingerprint_parts.append(f"{sheet}:{ws.max_row}x{ws.max_column}")

        fingerprint = "|".join(fingerprint_parts)
        content_hash = hashlib.sha256(fingerprint.encode(), usedforsecurity=False).hexdigest()[:12]

        return f"acq-{content_hash}"

    def _acquire_workbook_observation(
        self, workbook: Workbook, provenance: Provenance
    ) -> WorkbookObservation:
        """Acquire workbook-level observable properties.

        Note:
            This records only workbook structural properties.
            Worksheet content properties belong to WorksheetObservation.
        """
        properties = workbook.properties
        worksheet_names = tuple(workbook.sheetnames)

        return WorkbookObservation(
            observation_id="obs-wb-0001",
            provenance=provenance,
            file_format="xlsx",
            format_version=None,
            creator=getattr(properties, "creator", None) if properties else None,
            created=getattr(properties, "created", None) if properties else None,
            modified=getattr(properties, "modified", None) if properties else None,
            application=getattr(properties, "appVersion", None) if properties else None,
            calculation_mode=None,  # YAGNI - not yet exposing openpyxl calculation object
            date_system=None,  # Not reliably observable from openpyxl - use None instead of assumption
            worksheet_count=len(worksheet_names),
            worksheet_names=worksheet_names,
            structure_protection=None,  # YAGNI - not exposing protection object
            window_protection=None,  # YAGNI - not exposing protection object
            visibility=None,  # Not directly observable - use None instead of assumption
        )

    def _acquire_worksheet_observation(
        self, workbook: Workbook, provenance: Provenance
    ) -> WorksheetObservation:
        """Acquire worksheet-level observable properties.

        Note:
            This records only worksheet structural properties.
            Cell values and formatting belong to CellObservation.
        """
        ws = workbook["CostX"]
        worksheet_index = 0  # Validated: exactly one worksheet

        # Extract merged ranges as string references
        merged_ranges = tuple(
            str(merged) for merged in ws.merged_cells.ranges
        ) if ws.merged_cells and hasattr(ws.merged_cells, 'ranges') else ()

        # Freeze panes
        freeze_panes = None
        if ws.freeze_panes:
            from openpyxl.utils.cell import coordinate_from_string
            try:
                col, row = coordinate_from_string(ws.freeze_panes)
                freeze_panes = (row - 1, self._column_index(col))
            except Exception:
                freeze_panes = None

        # Hidden rows and columns
        hidden_rows = tuple(
            idx for idx, dim in ws.row_dimensions.items()
            if dim.hidden
        )
        hidden_columns = tuple(
            idx for idx, dim in ws.column_dimensions.items()
            if dim.hidden
        )

        # Visibility from openpyxl's sheet_state
        visibility = ws.sheet_state if hasattr(ws, 'sheet_state') else None

        return WorksheetObservation(
            observation_id="obs-ws-0001",
            provenance=provenance,
            worksheet_name="CostX",
            worksheet_index=worksheet_index,
            visibility=visibility,
            row_count=ws.max_row,
            column_count=ws.max_column,
            merged_ranges=merged_ranges,
            freeze_panes=freeze_panes,
            auto_filter=None,  # YAGNI - could extract from ws.auto_filter.ref
            print_area=None,  # YAGNI - could extract from ws.print_area
            hidden_rows=hidden_rows,
            hidden_columns=hidden_columns,
        )

    def _acquire_row_and_cell_observations(
        self,
        workbook: Workbook,
        provenance: Provenance,
    ) -> list[Observation]:
        """Acquire row and cell observations for all rows in the worksheet."""
        ws = workbook["CostX"]
        observations: list[Observation] = []

        # Counter for deterministic identity
        row_counter = 0
        cell_counter = 0

        for row_idx in range(1, ws.max_row + 1):
            # Acquire RowObservation
            row_counter += 1
            row_dim = ws.row_dimensions.get(row_idx)

            # Visibility: "visible" or "hidden"
            visibility = None
            if row_dim is not None:
                visibility = "hidden" if row_dim.hidden else "visible"

            row_obs = RowObservation(
                observation_id=f"obs-row-{row_counter:04d}",
                provenance=provenance,
                worksheet_name="CostX",
                row_number=row_idx,
                visibility=visibility,
                height=row_dim.height if row_dim else None,
            )
            observations.append(row_obs)

            # Acquire CellObservation for each cell in the row
            for col_idx in range(1, ws.max_column + 1):
                cell = ws.cell(row=row_idx, column=col_idx)
                cell_counter += 1

                # Determine if cell is merged
                is_merged = False
                if ws.merged_cells and hasattr(ws.merged_cells, 'ranges'):
                    is_merged = any(
                        row_idx >= merged.min_row and row_idx <= merged.max_row and
                        col_idx >= merged.min_col and col_idx <= merged.max_col
                        for merged in ws.merged_cells.ranges
                    )

                # Comment: extract text if exists
                comment_text = None
                if cell.comment:
                    comment_text = cell.comment.text

                # Formula value handling
                formula_value = None
                cell_value = cell.value
                if cell.data_type == "f":
                    formula_value = cell.value  # Formula string
                    cell_value = None

                cell_obs = CellObservation(
                    observation_id=f"obs-cell-{cell_counter:04d}",
                    provenance=provenance,
                    worksheet_name="CostX",
                    row=row_idx,
                    column=col_idx,
                    reference=cell.coordinate,
                    value=cell_value,
                    formula=formula_value,
                    calculated_value=None,  # Requires data_only=True on load
                    data_type=cell.data_type,
                    number_format=cell.number_format,
                    font=None,  # YAGNI - not acquired in initial scope
                    fill=None,  # YAGNI - not acquired in initial scope
                    alignment=None,  # YAGNI - not acquired in initial scope
                    border=None,  # YAGNI - not acquired in initial scope
                    locked=None,  # YAGNI - could extract from protection
                    hidden=None,  # YAGNI - could extract from protection
                    merged=is_merged,
                    comment=comment_text,
                )
                observations.append(cell_obs)

        return observations

    @staticmethod
    def _column_index(column_letter: str) -> int:
        """Convert Excel column letter to 1-based index.

        Args:
            column_letter: Excel column letter (e.g., "A", "B", "AA").

        Returns:
            1-based column index.
        """
        result = 0
        for char in column_letter.upper():
            result = result * 26 + (ord(char) - ord("A") + 1)
        return result

    def close(self) -> None:
        """Close the loaded workbook if open."""
        if self._workbook is not None:
            self._workbook.close()
            self._workbook = None
            self._path = None