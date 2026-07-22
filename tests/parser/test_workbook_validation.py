"""Tests for M6.2 WorkbookParser validation.

Verifies:
- valid workbook validates successfully
- workbook not loaded raises RuntimeError
- missing worksheet raises ValueError
- multiple worksheets raises ValueError
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jarvis.parsers.costx.workbook_parser import WorkbookParser


class TestWorkbookValidation:
    """Test workbook validation behavior."""

    def test_valid_workbook_validates_successfully(self) -> None:
        """Valid CostX BOQ workbook passes validation."""
        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/full_boq.xlsx")

        parser.load(workbook_path)
        parser.validate()  # Should not raise

        parser.close()

    def test_workbook_not_loaded_raises_runtime_error(self) -> None:
        """Validation raises RuntimeError when no workbook loaded."""
        parser = WorkbookParser()

        with pytest.raises(RuntimeError, match="Cannot validate: no workbook loaded"):
            parser.validate()

    def test_missing_worksheet_raises_value_error(self) -> None:
        """Validation raises ValueError when worksheet 'CostX' is missing."""
        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/formula_workbook.xlsx")

        parser.load(workbook_path)

        with pytest.raises(ValueError, match="Expected worksheet named 'CostX'"):
            parser.validate()

        parser.close()

    def test_multiple_worksheets_raises_value_error(self) -> None:
        """Validation raises ValueError when workbook has multiple worksheets."""
        parser = WorkbookParser()
        workbook_path = Path("tests/fixtures/costx/dimensions_export.xlsx")

        parser.load(workbook_path)

        with pytest.raises(ValueError, match="Expected exactly 1 worksheet"):
            parser.validate()

        parser.close()