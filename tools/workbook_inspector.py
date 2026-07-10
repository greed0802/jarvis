#!/usr/bin/env python3
"""
Workbook Inspector — engineering utility for analyzing Excel workbook structure.

Inspects arbitrary Excel workbooks and reports observable facts only.
Does not infer business meaning (no BOQ/heading/trade identification).

Not part of the Jarvis runtime. Lives under tools/ with no Kernel,
Application, Context, Planner, or Skill dependencies.

Usage:
    python tools/workbook_inspector.py workbook.xlsx
    python tools/workbook_inspector.py workbook.xlsx --verbose
    python tools/workbook_inspector.py workbook.xlsx --verbose --formulas
    python tools/workbook_inspector.py a.xlsx b.xlsx --formulas

Output tags:
    [META]     Workbook metadata
    [SHEET]    Sheet information
    [CELL]     Non-empty cell (with --verbose)
    [FORMULA]  Formula cell (with --formulas)
    [VALUE]    Calculated value for a formula cell
    [FORMAT]   Cell formatting details (with --verbose)
    [MERGE]    Merged cell ranges
    [HIDDEN]   Hidden rows/columns/sheets
    [FREEZE]   Freeze pane configuration
    [FILTER]   Auto-filter settings
    [OUTLINE]  Outline/grouping levels
    [NAMED]    Named ranges
    [STAT]     Column statistics
    [WARNING]  Anomalies or load issues

Future (not implemented):
    --json, --csv, --compare, structured collect/emit separation
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.styles.named_styles import _NamedCellStyle
from openpyxl.utils import get_column_letter


# ---------------------------------------------------------------------------
# CostX compatibility
# ---------------------------------------------------------------------------

_NAMED_STYLE_PATCH_APPLIED = False


def _apply_named_style_none_name_patch() -> None:
    """
    CostX exports can contain cellXfs / named style entries with a missing name.

    openpyxl 3.1.x raises:
        TypeError: _NamedCellStyle.name should be <class 'str'> but value is <class 'NoneType'>

    Coerce None -> '' so the workbook can still be inspected. This is a load
    fallback only; it does not invent style semantics.
    """
    global _NAMED_STYLE_PATCH_APPLIED
    if _NAMED_STYLE_PATCH_APPLIED:
        return

    original_init = _NamedCellStyle.__init__

    def patched_init(
        self,
        name=None,
        xfId=None,
        builtinId=None,
        iLevel=None,
        hidden=None,
        customBuiltin=None,
        extLst=None,
    ):
        if name is None:
            name = ""
        original_init(
            self,
            name=name,
            xfId=xfId,
            builtinId=builtinId,
            iLevel=iLevel,
            hidden=hidden,
            customBuiltin=customBuiltin,
            extLst=extLst,
        )

    _NamedCellStyle.__init__ = patched_init  # type: ignore[method-assign]
    _NAMED_STYLE_PATCH_APPLIED = True


def _load_workbook(path: str, *, data_only: bool) -> Any:
    """
    Load a workbook, applying a CostX-compatible named-style fallback if needed.

    Returns the workbook. Emits [WARNING] if the fallback path is used.
    """
    try:
        return openpyxl.load_workbook(path, data_only=data_only)
    except TypeError as e:
        msg = str(e)
        if "NamedCellStyle" in msg and "NoneType" in msg:
            emit(
                "WARNING",
                "openpyxl rejected workbook due to named style with name=None "
                f"(data_only={data_only})",
            )
            emit(
                "WARNING",
                "Applying named-style None-name fallback and retrying load",
            )
            _apply_named_style_none_name_patch()
            try:
                wb = openpyxl.load_workbook(path, data_only=data_only)
                emit(
                    "WARNING",
                    "Workbook loaded via named-style fallback "
                    f"(data_only={data_only})",
                )
                return wb
            except Exception as e2:
                emit(
                    "WARNING",
                    f"Fallback load also failed (data_only={data_only}): {e2}",
                )
                raise
        raise


# ---------------------------------------------------------------------------
# Output helper — single place for formatting; enables future --json
# ---------------------------------------------------------------------------

def emit(tag: str, message: str) -> None:
    """Emit a tagged observation line."""
    print(f"[{tag}] {message}")


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def _safe_rgb(color: Any) -> str | None:
    """Extract an RGB/theme color string if available."""
    if color is None:
        return None
    try:
        if getattr(color, "type", None) == "rgb" and color.rgb:
            return str(color.rgb)
        if getattr(color, "type", None) == "theme":
            return f"theme:{color.theme}"
        if getattr(color, "type", None) == "indexed":
            return f"indexed:{color.indexed}"
    except Exception:
        return None
    return None


def _cell_type_label(cell: Any) -> str:
    """Map openpyxl cell data_type / value to an observational type label."""
    if cell.value is None:
        return "blank"
    dt = cell.data_type
    if dt == "f":
        return "formula"
    if dt == "n":
        if cell.is_date:
            return "date"
        return "numeric"
    if dt == "b":
        return "boolean"
    if dt == "d":
        return "date"
    if dt == "e":
        return "error"
    return "text"


def _format_summary(cell: Any) -> list[str]:
    """Collect observable formatting attributes for a cell."""
    parts: list[str] = []
    font = cell.font
    if font is not None:
        if font.bold:
            parts.append("bold")
        if font.italic:
            parts.append("italic")
        if font.underline and font.underline != "none":
            parts.append(f"underline={font.underline}")
        rgb = _safe_rgb(font.color)
        if rgb:
            parts.append(f"font_color={rgb}")
        if font.size:
            parts.append(f"size={font.size}")
        if font.name:
            parts.append(f"font={font.name}")

    fill = cell.fill
    if fill is not None and fill.fill_type and fill.fill_type != "none":
        fg = _safe_rgb(fill.fgColor)
        parts.append(f"fill={fg or fill.fill_type}")

    if cell.number_format and cell.number_format != "General":
        parts.append(f"numfmt={cell.number_format}")

    align = cell.alignment
    if align is not None:
        if align.horizontal:
            parts.append(f"align_h={align.horizontal}")
        if align.vertical:
            parts.append(f"align_v={align.vertical}")
        if align.indent:
            parts.append(f"indent={align.indent}")
        if align.wrap_text:
            parts.append("wrap")

    border = cell.border
    if border is not None:
        sides = []
        for side_name in ("left", "right", "top", "bottom"):
            side = getattr(border, side_name, None)
            if side is not None and side.style:
                sides.append(f"{side_name}={side.style}")
        if sides:
            parts.append(f"border({','.join(sides)})")

    return parts


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

def inspect_metadata(path: Path, wb: Any) -> None:
    """Report workbook-level observable metadata."""
    emit("META", f"File: {path.name}")
    emit("META", f"Path: {path.resolve()}")

    try:
        size = path.stat().st_size
        emit("META", f"File size: {size} bytes")
    except OSError as e:
        emit("WARNING", f"Could not read file size: {e}")

    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        emit("META", f"Modified: {mtime.isoformat(sep=' ', timespec='seconds')}")
    except OSError as e:
        emit("WARNING", f"Could not read modified time: {e}")

    emit("META", f"Sheets: {wb.sheetnames}")
    emit("META", f"Sheet count: {len(wb.sheetnames)}")

    props = wb.properties
    if props is not None:
        if props.creator:
            emit("META", f"Creator: {props.creator}")
        if props.lastModifiedBy:
            emit("META", f"Last modified by: {props.lastModifiedBy}")
        if props.created:
            emit("META", f"Created: {props.created}")
        if props.modified:
            emit("META", f"Document modified: {props.modified}")
        if props.title:
            emit("META", f"Title: {props.title}")
        if props.subject:
            emit("META", f"Subject: {props.subject}")
        if props.description:
            emit("META", f"Description: {props.description}")
        if props.keywords:
            emit("META", f"Keywords: {props.keywords}")
        if props.category:
            emit("META", f"Category: {props.category}")
        if props.version:
            emit("META", f"Version: {props.version}")

    try:
        calc = wb.calculation
        if calc is not None:
            if calc.calcMode is not None:
                emit("META", f"Calculation mode: {calc.calcMode}")
            if calc.fullCalcOnLoad is not None:
                emit("META", f"Full calc on load: {calc.fullCalcOnLoad}")
    except Exception as e:
        emit("WARNING", f"Could not read calculation properties: {e}")

    try:
        if hasattr(wb, "excel_base_date"):
            emit("META", f"Excel base date: {wb.excel_base_date}")
    except Exception:
        pass

    hidden_sheets = [
        sn for sn in wb.sheetnames if wb[sn].sheet_state != "visible"
    ]
    if hidden_sheets:
        emit("WARNING", f"Hidden sheets detected: {hidden_sheets}")
        for sn in hidden_sheets:
            emit("HIDDEN", f"Sheet '{sn}' state={wb[sn].sheet_state}")

    if wb.defined_names:
        emit("META", f"Named ranges defined: {len(list(wb.defined_names))}")
        for defn in wb.defined_names.values():
            try:
                destinations = []
                for title, coord in defn.destinations:
                    destinations.append(f"{title}!{coord}")
                emit("NAMED", f"{defn.name}: {', '.join(destinations)}")
            except Exception as e:
                emit("WARNING", f"Could not resolve named range '{defn.name}': {e}")

    try:
        if getattr(wb.security, "workbookPassword", None) or getattr(
            wb.security, "lockStructure", False
        ):
            emit("WARNING", "Workbook has protection/security settings")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Column statistics
# ---------------------------------------------------------------------------

def inspect_statistics(ws: Any) -> None:
    """Report per-column observational statistics."""
    emit("STAT", f"Sheet '{ws.title}' column statistics:")

    max_col = ws.max_column or 0
    max_row = ws.max_row or 0

    counters: dict[int, dict[str, int]] = {}
    for col_idx in range(1, max_col + 1):
        counters[col_idx] = {
            "non_empty": 0,
            "blank": 0,
            "text": 0,
            "numeric": 0,
            "formula": 0,
            "date": 0,
            "boolean": 0,
            "error": 0,
        }

    for row in ws.iter_rows(
        min_row=1, max_row=max_row, min_col=1, max_col=max_col
    ):
        for cell in row:
            c = counters[cell.column]
            label = _cell_type_label(cell)
            if label == "blank":
                c["blank"] += 1
            else:
                c["non_empty"] += 1
                if label in c:
                    c[label] += 1
                else:
                    c["text"] += 1

    for col_idx in range(1, max_col + 1):
        c = counters[col_idx]
        if c["non_empty"] == 0:
            continue
        letter = get_column_letter(col_idx)
        parts = [
            f"non_empty={c['non_empty']}",
            f"blank={c['blank']}",
            f"text={c['text']}",
            f"numeric={c['numeric']}",
            f"formula={c['formula']}",
            f"date={c['date']}",
            f"boolean={c['boolean']}",
            f"error={c['error']}",
        ]
        emit("STAT", f"  {letter}: {', '.join(parts)}")


# ---------------------------------------------------------------------------
# Cell dump (verbose mode)
# ---------------------------------------------------------------------------

def dump_cells(ws_f: Any, ws_v: Any | None, formulas: bool) -> None:
    """Emit every non-empty cell with type, value, and formatting."""
    emit("CELL", f"Non-empty cells for sheet '{ws_f.title}':")

    max_col = ws_f.max_column or 0
    max_row = ws_f.max_row or 0

    for row in ws_f.iter_rows(
        min_row=1, max_row=max_row, min_col=1, max_col=max_col
    ):
        for cell in row:
            if cell.value is None:
                continue

            addr = f"{get_column_letter(cell.column)}{cell.row}"
            label = _cell_type_label(cell)
            fmt = _format_summary(cell)
            fmt_str = f" style=[{', '.join(fmt)}]" if fmt else ""

            if formulas and cell.data_type == "f":
                # Handle ArrayFormula objects (CostX XGET formulas)
                formula_text = getattr(cell.value, "formula", None)
                if formula_text is None:
                    formula_text = repr(cell.value)
                emit(
                    "FORMULA",
                    f"{addr} type=formula value={formula_text}{fmt_str}",
                )
                if ws_v is not None:
                    calc = ws_v.cell(row=cell.row, column=cell.column).value
                    emit("VALUE", f"{addr} calculated={calc!r}")
            else:
                emit(
                    "CELL",
                    f"{addr} type={label} value={cell.value!r}{fmt_str}",
                )


# ---------------------------------------------------------------------------
# Sheet inspection
# ---------------------------------------------------------------------------

def inspect_sheet(
    ws_f: Any,
    ws_v: Any | None,
    *,
    verbose: bool,
    formulas: bool,
) -> None:
    """Report all observable facts for a single worksheet."""
    emit("SHEET", f"'{ws_f.title}'")
    emit(
        "SHEET",
        f"  Dimensions: {ws_f.max_row} rows x {ws_f.max_column} columns",
    )
    emit("SHEET", f"  State: {ws_f.sheet_state}")

    try:
        if ws_f.protection and ws_f.protection.sheet:
            emit("WARNING", f"Sheet '{ws_f.title}' is protected")
    except Exception:
        pass

    if ws_f.freeze_panes:
        emit("FREEZE", f"Freeze panes: {ws_f.freeze_panes}")
    else:
        emit("FREEZE", "No freeze panes set")

    if ws_f.auto_filter and ws_f.auto_filter.ref:
        emit("FILTER", f"Auto-filter range: {ws_f.auto_filter.ref}")
    else:
        emit("FILTER", "No auto-filter set")

    if ws_f.merged_cells:
        merged = [str(m) for m in ws_f.merged_cells.ranges]
        if merged:
            emit("MERGE", f"Count: {len(merged)}")
            for m in merged:
                emit("MERGE", f"  {m}")

    hidden_rows = [
        r for r, dim in ws_f.row_dimensions.items() if dim.hidden
    ]
    hidden_cols = [
        c for c, dim in ws_f.column_dimensions.items() if dim.hidden
    ]
    if hidden_rows:
        shown = hidden_rows[:20]
        suffix = "..." if len(hidden_rows) > 20 else ""
        emit("HIDDEN", f"Hidden rows ({len(hidden_rows)}): {shown}{suffix}")
    if hidden_cols:
        shown = hidden_cols[:20]
        suffix = "..." if len(hidden_cols) > 20 else ""
        emit("HIDDEN", f"Hidden columns ({len(hidden_cols)}): {shown}{suffix}")

    col_outlines = {
        dim.outlineLevel
        for dim in ws_f.column_dimensions.values()
        if dim.outlineLevel and dim.outlineLevel > 0
    }
    row_outlines = {
        dim.outlineLevel
        for dim in ws_f.row_dimensions.values()
        if dim.outlineLevel and dim.outlineLevel > 0
    }
    if col_outlines:
        emit("OUTLINE", f"Column outline levels: {sorted(col_outlines)}")
    if row_outlines:
        emit("OUTLINE", f"Row outline levels: {sorted(row_outlines)}")

    custom_widths = {
        letter: dim.width
        for letter, dim in ws_f.column_dimensions.items()
        if dim.width is not None
    }
    if custom_widths:
        emit("STAT", f"Custom column widths: {custom_widths}")

    inspect_statistics(ws_f)

    if verbose:
        dump_cells(ws_f, ws_v, formulas)


# ---------------------------------------------------------------------------
# Workbook inspection
# ---------------------------------------------------------------------------

def inspect_workbook(
    path: str,
    *,
    verbose: bool = False,
    formulas: bool = False,
) -> None:
    """Inspect a single workbook and emit observable facts."""
    p = Path(path)
    if not p.exists():
        emit("WARNING", f"File does not exist: {p}")
        return
    if not p.is_file():
        emit("WARNING", f"Path is not a file: {p}")
        return

    wb_formulas = _load_workbook(path, data_only=False)
    if wb_formulas is None:
        return

    wb_values = None
    if formulas:
        wb_vals = _load_workbook(path, data_only=True)
        if wb_vals is None:
            emit("WARNING", "Falling back to formula workbook for value reads")
            wb_values = wb_formulas
        else:
            wb_values = wb_vals

    try:
        inspect_metadata(p, wb_formulas)

        for sn in wb_formulas.sheetnames:
            ws_f = wb_formulas[sn]
            ws_v = wb_values[sn] if wb_values is not None else None
            inspect_sheet(ws_f, ws_v, verbose=verbose, formulas=formulas)
    finally:
        wb_formulas.close()
        if wb_values is not None and wb_values is not wb_formulas:
            wb_values.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect Excel workbook structure for engineering analysis. "
            "Reports observable facts only; does not infer business meaning."
        )
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more workbook paths to inspect",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Emit every non-empty cell (type, value, style)",
    )
    parser.add_argument(
        "--formulas",
        action="store_true",
        help=(
            "Load twice (data_only=False and data_only=True) and report "
            "formula strings alongside calculated values"
        ),
    )
    # Reserved for future use — not implemented yet:
    # --json, --csv, --compare

    args = parser.parse_args(argv)

    for path in args.paths:
        inspect_workbook(path, verbose=args.verbose, formulas=args.formulas)

    return 0


if __name__ == "__main__":
    sys.exit(main())
