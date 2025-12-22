from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import openpyxl
from openpyxl import Workbook
from openpyxl.utils import column_index_from_string, get_column_letter
from openpyxl.utils.cell import coordinate_from_string


def _parse_start_cell(cell: str) -> tuple[int, int]:
    """
    Convert a cell reference like 'A1' into (row, column) indices (1‑based).
    """
    col_str, row_str = coordinate_from_string(cell)
    return int(row_str), column_index_from_string(col_str)


def _ensure_sheet(
    wb: openpyxl.Workbook, sheet_name: Optional[str]
) -> openpyxl.worksheet.worksheet.Worksheet:
    """
    Return the worksheet with the given name, creating it if necessary.
    If sheet_name is None, return the active sheet.
    """
    if sheet_name is None:
        return wb.active
    if sheet_name in wb.sheetnames:
        return wb[sheet_name]
    return wb.create_sheet(title=sheet_name)


def _write_headers(ws: openpyxl.worksheet.worksheet.Worksheet, headers: List[str], start_row: int, start_col: int) -> None:
    """
    Write headers to the worksheet at the specified start position.
    """
    for idx, header in enumerate(headers, start=0):
        col = start_col + idx
        ws.cell(row=start_row, column=col, value=header)


def _write_rows(
    ws: openpyxl.worksheet.worksheet.Worksheet,
    data: List[Dict[str, Any]],
    headers: List[str],
    start_row: int,
    start_col: int,
) -> None:
    """
    Write data rows to the worksheet starting after the headers.
    """
    for row_offset, row_data in enumerate(data, start=0):
        for col_offset, header in enumerate(headers, start=0):
            col = start_col + col_offset
            ws.cell(row=start_row + 1 + row_offset, column=col, value=row_data.get(header))


def write_data(
    filepath: str,
    sheet_name: Optional[str],
    data: Optional[List[Dict[str, Any]]],
    start_cell: str = "A1",
) -> Dict[str, str]:
    """
    Write data to an Excel workbook.

    Parameters
    ----------
    filepath : str
        Path to the Excel file. If the file does not exist, it will be created.
    sheet_name : str | None
        Name of the sheet to write to. If None, the active sheet is used.
    data : list[dict[str, Any]] | None
        Data to write. Each dictionary represents a row. Keys are column headers.
        If None, the workbook/sheet will be created (or opened) but no data will be written.
    start_cell : str, default "A1"
        Cell reference where the data (including headers) should start.

    Returns
    -------
    dict[str, str]
        Mapping of sheet name to status message. The status is "written" if data
        was written, "created" if the workbook was created, or "skipped" if no
        data was provided.
    """
    # Load or create workbook
    if os.path.exists(filepath):
        try:
            wb = openpyxl.load_workbook(filepath)
        except Exception:
            # If the file exists but is not a valid workbook, create a new one
            wb = Workbook()
    else:
        wb = Workbook()

    ws = _ensure_sheet(wb, sheet_name)

    # Determine start position
    start_row, start_col = _parse_start_cell(start_cell)

    # If no data, just return status
    if not data:
        wb.save(filepath)
        return {sheet_name or "default": "skipped"}

    # Determine headers from data keys
    headers = list({k for row in data for k in row.keys()})

    # Check if headers already exist in the sheet
    existing_headers = None
    if ws.max_row >= start_row and ws.max_column >= start_col:
        existing_headers = [
            ws.cell(row=start_row, column=start_col + i).value
            for i in range(ws.max_column - start_col + 1)
        ]

    # Write headers if they are missing or differ
    if not existing_headers or existing_headers[: len(headers)] != headers:
        _write_headers(ws, headers, start_row, start_col)

    # Write data rows
    _write_rows(ws, data, headers, start_row, start_col)

    # Save workbook
    wb.save(filepath)

    return {sheet_name or "default": "written"}