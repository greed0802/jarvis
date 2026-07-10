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