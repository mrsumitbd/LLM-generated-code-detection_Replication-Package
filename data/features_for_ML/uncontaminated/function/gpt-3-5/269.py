def write_data(
    filepath: str,
    sheet_name: str | None,
    data: list[dict[str, Any]] | None,
    start_cell: str = "A1",
) -> dict[str, str]:
    
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    import pandas as pd
    
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name if sheet_name else "Sheet1"
    
    if data:
        df = pd.DataFrame(data)
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
    
    wb.save(filepath)
    
    return {"status": "success", "message": f"Data written to {sheet_name} in {filepath}"}