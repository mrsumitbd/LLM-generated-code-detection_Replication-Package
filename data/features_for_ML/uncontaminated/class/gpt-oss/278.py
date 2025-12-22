import json
from pathlib import Path
from typing import Any, Iterable, List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SpreadsheetContext:
    """Context for Google Spreadsheet service"""

    DEFAULT_SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
    ]

    def __init__(
        self,
        credentials_path: str | Path,
        spreadsheet_id: str,
        scopes: Optional[Iterable[str]] = None,
    ) -> None:
        """
        Initialize the SpreadsheetContext.

        Args:
            credentials_path: Path to the service account JSON key file.
            spreadsheet_id: The ID of the spreadsheet to work with.
            scopes: Optional list of OAuth scopes. Defaults to the standard
                spreadsheet and drive scopes.
        """
        self.credentials_path = Path(credentials_path).expanduser()
        if not self.credentials_path.is_file():
            raise FileNotFoundError(f"Credentials file not found: {self.credentials_path}")

        self.spreadsheet_id = spreadsheet_id
        self.scopes = list(scopes) if scopes is not None else self.DEFAULT_SCOPES

        self._credentials: service_account.Credentials | None = None
        self._service: Any | None = None

    @property
    def credentials(self) -> service_account.Credentials:
        """Lazy load and return the service account credentials."""
        if self._credentials is None:
            self._credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=self.scopes
            )
        return self._credentials

    @property
    def service(self) -> Any:
        """Lazy build and return the Google Sheets API service."""
        if self._service is None:
            self._service = build("sheets", "v4", credentials=self.credentials)
        return self._service

    def get_values(self, range_name: str) -> List[List[Any]]:
        """
        Retrieve values from the specified range.

        Args:
            range_name: A string in A1 notation (e.g., "Sheet1!A1:C10").

        Returns:
            A list of rows, each row being a list of cell values.
        """
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=self.spreadsheet_id, range=range_name)
                .execute()
            )
            return result.get("values", [])
        except HttpError as e:
            raise RuntimeError(f"Error retrieving values from {range_name}: {e}") from e

    def update_values(
        self,
        range_name: str,
        values: List[List[Any]],
        major_dimension: str = "ROWS",
    ) -> None:
        """
        Update values in the specified range.

        Args:
            range_name: A string in A1 notation.
            values: A list of rows to write.
            major_dimension: "ROWS" or "COLUMNS" (default "ROWS").
        """
        body = {
            "values": values,
            "majorDimension": major_dimension,
        }
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body,
            ).execute()
        except HttpError as e:
            raise RuntimeError(f"Error updating values in {range_name}: {e}") from e

    def append_values(
        self,
        range_name: str,
        values: List[List[Any]],
        major_dimension: str = "ROWS",
    ) -> None:
        """
        Append values to the specified range.

        Args:
            range_name: A string in A1 notation (e.g., "Sheet1!A1").
            values: A list of rows to append.
            major_dimension: "ROWS" or "COLUMNS" (default "ROWS").
        """
        body = {
            "values": values,
            "majorDimension": major_dimension,
        }
        try:
            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body=body,
            ).execute()
        except HttpError as e:
            raise RuntimeError(f"Error appending values to {range_name}: {e}") from e

    def get_sheet_metadata(self) -> dict:
        """
        Retrieve metadata for the spreadsheet.

        Returns:
            A dictionary containing spreadsheet properties and sheet details.
        """
        try:
            result = (
                self.service.spreadsheets()
                .get(spreadsheetId=self.spreadsheet_id, fields="properties,sheets")
                .execute()
            )
            return result
        except HttpError as e:
            raise RuntimeError(f"Error retrieving spreadsheet metadata: {e}") from e

    def add_sheet(self, title: str, index: Optional[int] = None) -> str:
        """
        Add a new sheet to the spreadsheet.

        Args:
            title: The title of the new sheet.
            index: Optional index at which to insert the sheet.

        Returns:
            The ID of the newly created sheet.
        """
        request_body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {"title": title},
                        **({"index": index} if index is not None else {}),
                    }
                }
            ]
        }
        try:
            response = (
                self.service.spreadsheets()
                .batchUpdate(spreadsheetId=self.spreadsheet_id, body=request_body)
                .execute()
            )
            sheet_id = response["replies"][0]["addSheet"]["properties"]["sheetId"]
            return str(sheet_id)
        except HttpError as e:
            raise RuntimeError(f"Error adding sheet '{title}': {e}") from e

    def delete_sheet(self, sheet_id: int) -> None:
        """
        Delete a sheet by its ID.

        Args:
            sheet_id: The ID of the sheet to delete.
        """
        request_body = {
            "requests": [
                {"deleteSheet": {"sheetId": sheet_id}}
            ]
        }
        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id, body=request_body
            ).execute()
        except HttpError as e:
            raise RuntimeError(f"Error deleting sheet ID {sheet_id}: {e}") from e

    def __enter__(self) -> "SpreadsheetContext":
        """Support context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Support context manager exit. No special cleanup needed."""
        pass