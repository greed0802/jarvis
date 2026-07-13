"""Deterministic CostX workbook parser.

This module provides the CostX workbook parser for loading and validating
CostX BOQ workbooks.

 Lifecycle:
- load a workbook
- retain a workbook reference
- release workbook resources via close()

Validation:
- validate loaded workbook matches the supported CostX BOQ format
"""

from __future__ import annotations

from pathlib import Path

from openpyxl.workbook.workbook import Workbook

from jarvis.parsers.costx.loader import load_workbook


class WorkbookParser:
    """Deterministic CostX workbook parser.

    WorkbookParser loads CostX BOQ workbooks and validates they match
    the supported format.
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
        """
        return self._workbook

    @property
    def path(self) -> Path | None:
        """Return the loaded workbook path.

        Returns:
            The Path of the loaded workbook if loaded, None otherwise.
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

    def close(self) -> None:
        """Close the loaded workbook if open."""
        if self._workbook is not None:
            self._workbook.close()
            self._workbook = None
            self._path = None