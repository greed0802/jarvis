"""Deterministic CostX workbook parser.

This module provides the initial implementation of the CostX workbook parser.

M6.1 establishes the parser lifecycle only:
- load a workbook
- retain a workbook reference
- release workbook resources

Workbook validation, worksheet discovery, row iteration,
and data extraction are implemented in later milestones.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl.workbook.workbook import Workbook

from jarvis.parsers.costx.loader import load_workbook


class WorkbookParser:
    """Deterministic CostX workbook parser.

    Loads and holds a reference to a CostX BOQ workbook for subsequent parsing.
    This class performs no worksheet reading, row iteration, or cell inspection.
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

    def close(self) -> None:
        """Close the loaded workbook if open."""
        if self._workbook is not None:
            self._workbook.close()
            self._workbook = None
            self._path = None