import openpyxl
from openpyxl.utils import get_column_letter
from typing import Any

def write_data(
    filepath: str,
    sheet_name: str | None,
    data: list[dict[str, Any]] | None,
    start_cell: str = "A1",
) -> dict[str, str]:
    """Write data to Excel sheet with workbook handling

    Headers are handled intelligently based on context.
    """
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    if sheet_name:
        worksheet.title = sheet_name

    if data:
        # Write headers
        headers = list(data[0].keys())
        for col, header in enumerate(headers, 1):
            worksheet.cell(row=1, column=col, value=header)

        # Write data
        for row, row_data in enumerate(data, 2):
            for col, header in enumerate(headers, 1):
                worksheet.cell(row=row, column=col, value=row_data[header])

    workbook.save(filepath)

    return {"filepath": filepath, "sheet_name": worksheet.title}