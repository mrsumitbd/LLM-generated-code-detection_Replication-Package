from typing import List, Dict, Any, Optional

class SpreadsheetContext:
    """Context for Google Spreadsheet service"""
    sheets_service: Any
    drive_service: Any
    folder_id: Optional[str] = None