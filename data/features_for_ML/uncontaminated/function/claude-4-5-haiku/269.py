def write_data(
    filepath: str,
    sheet_name: str | None,
    data: list[dict[str, Any]] | None,
    start_cell: str = "A1",
) -> dict[str, str]:
    """Write data to Excel sheet with workbook handling
    
    Headers are handled intelligently based on context.
    """
    import openpyxl
    from openpyxl.utils import get_column_letter
    from openpyxl.utils.cell import coordinate_from_string
    
    if not filepath or not sheet_name or not data:
        return {"status": "error", "message": "Invalid input parameters"}
    
    try:
        # Load or create workbook
        try:
            workbook = openpyxl.load_workbook(filepath)
        except FileNotFoundError:
            workbook = openpyxl.Workbook()
            if workbook.sheetnames and workbook.sheetnames[0] == "Sheet":
                workbook.remove(workbook.active)
        
        # Get or create sheet
        if sheet_name in workbook.sheetnames:
            worksheet = workbook[sheet_name]
        else:
            worksheet = workbook.create_sheet(sheet_name)
        
        # Parse start cell
        col_letter, row_num = coordinate_from_string(start_cell)
        start_col = openpyxl.utils.column_index_from_string(col_letter)
        start_row = row_num
        
        if not data:
            return {"status": "success", "message": "No data to write"}
        
        # Get headers from first data item
        headers = list(data[0].keys())
        
        # Write headers
        for col_idx, header in enumerate(headers, start=start_col):
            cell = worksheet.cell(row=start_row, column=col_idx)
            cell.value = header
        
        # Write data rows
        for row_idx, row_data in enumerate(data, start=start_row + 1):
            for col_idx, header in enumerate(headers, start=start_col):
                cell = worksheet.cell(row=row_idx, column=col_idx)
                cell.value = row_data.get(header)
        
        # Save workbook
        workbook.save(filepath)
        
        return {
            "status": "success",
            "message": f"Data written to {sheet_name} starting at {start_cell}",
            "rows_written": str(len(data)),
            "columns_written": str(len(headers))
        }
    
    except Exception as e:
        return {"status": "error", "message": str(e)}