import os
import json
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.oauth2.credentials import Credentials as UserCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SpreadsheetContext:
    """Context for Google Spreadsheet service"""

    def __init__(self, credentials_path: str = None, token_path: str = None, scopes: list = None):
        """
        Initialize SpreadsheetContext with credentials.
        
        Args:
            credentials_path: Path to service account JSON or OAuth2 credentials file
            token_path: Path to store/load OAuth2 token
            scopes: List of OAuth2 scopes to request
        """
        self.credentials_path = credentials_path
        self.token_path = token_path or "token.json"
        self.scopes = scopes or ["https://www.googleapis.com/auth/spreadsheets"]
        self.service = None
        self.credentials = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        if self.credentials_path:
            if self.credentials_path.endswith(".json"):
                with open(self.credentials_path, "r") as f:
                    creds_data = json.load(f)
                
                if "type" in creds_data and creds_data["type"] == "service_account":
                    self.credentials = Credentials.from_service_account_file(
                        self.credentials_path, scopes=self.scopes
                    )
                else:
                    self.credentials = self._oauth2_authenticate()
            else:
                self.credentials = self._oauth2_authenticate()
        else:
            self.credentials = self._oauth2_authenticate()
        
        self.service = build("sheets", "v4", credentials=self.credentials)

    def _oauth2_authenticate(self):
        """Handle OAuth2 authentication flow"""
        creds = None
        
        if os.path.exists(self.token_path):
            creds = UserCredentials.from_authorized_user_file(self.token_path, self.scopes)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    creds = None
            
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path or "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)
            
            with open(self.token_path, "w") as token:
                token.write(creds.to_json())
        
        return creds

    def get_service(self):
        """Get the Google Sheets service"""
        return self.service

    def create_spreadsheet(self, title: str, sheets: list = None) -> str:
        """
        Create a new spreadsheet.
        
        Args:
            title: Title of the spreadsheet
            sheets: List of sheet titles (optional)
        
        Returns:
            Spreadsheet ID
        """
        body = {
            "properties": {"title": title},
            "sheets": [{"properties": {"title": sheet}} for sheet in (sheets or ["Sheet1"])]
        }
        
        result = self.service.spreadsheets().create(body=body).execute()
        return result.get("spreadsheetId")

    def get_spreadsheet(self, spreadsheet_id: str) -> dict:
        """
        Get spreadsheet metadata.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
        
        Returns:
            Spreadsheet metadata
        """
        return self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()

    def read_range(self, spreadsheet_id: str, range_name: str) -> list:
        """
        Read values from a range in a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            range_name: Range in A1 notation (e.g., "Sheet1!A1:B2")
        
        Returns:
            List of rows
        """
        result = self.service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name
        ).execute()
        return result.get("values", [])

    def write_range(self, spreadsheet_id: str, range_name: str, values: list) -> dict:
        """
        Write values to a range in a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            range_name: Range in A1 notation
            values: List of rows to write
        
        Returns:
            Update result
        """
        body = {"values": values}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        return result

    def append_range(self, spreadsheet_id: str, range_name: str, values: list) -> dict:
        """
        Append values to a range in a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            range_name: Range in A1 notation
            values: List of rows to append
        
        Returns:
            Append result
        """
        body = {"values": values}
        result = self.service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        return result

    def clear_range(self, spreadsheet_id: str, range_name: str) -> dict:
        """
        Clear values from a range in a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            range_name: Range in A1 notation
        
        Returns:
            Clear result
        """
        result = self.service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        return result

    def batch_update(self, spreadsheet_id: str, requests: list) -> dict:
        """
        Perform batch updates on a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            requests: List of update requests
        
        Returns:
            Batch update result
        """
        body = {"requests": requests}
        result = self.service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body
        ).execute()
        return result

    def add_sheet(self, spreadsheet_id: str, title: str) -> int:
        """
        Add a new sheet to a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            title: Title of the new sheet
        
        Returns:
            Sheet ID
        """
        request = {
            "addSheet": {
                "properties": {"title": title}
            }
        }
        result = self.batch_update(spreadsheet_id, [request])
        return result["replies"][0]["addSheet"]["properties"]["sheetId"]

    def delete_sheet(self, spreadsheet_id: str, sheet_id: int) -> dict:
        """
        Delete a sheet from a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            sheet_id: ID of the sheet to delete
        
        Returns:
            Delete result
        """
        request = {
            "deleteSheet": {
                "sheetId": sheet_id
            }
        }
        return self.batch_update(spreadsheet_id, [request])

    def format_cells(self, spreadsheet_id: str, sheet_id: int, range_spec: dict, format_spec: dict) -> dict:
        """
        Format cells in a spreadsheet.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            sheet_id: ID of the sheet
            range_spec: Range specification
            format_spec: Format specification
        
        Returns:
            Format result
        """
        request = {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    **range_spec
                },
                "cell": {
                    "userEnteredFormat": format_spec
                },
                "fields": "userEnteredFormat"
            }
        }
        return self.batch_update(spreadsheet_id, [request])

    def share_spreadsheet(self, spreadsheet_id: str, email: str, role: str = "reader") -> dict:
        """
        Share a spreadsheet with another user.
        
        Args:
            spreadsheet_id: ID of the spreadsheet
            email: Email address to share with
            role: Role (reader, writer, owner)
        
        Returns:
            Share result
        """
        drive_service = build("drive", "v3", credentials=self.credentials)
        return drive_service.permissions().create(
            fileId=spreadsheet_id,
            body={
                "kind": "drive#permission",
                "type": "user",
                "role": role,
                "emailAddress": email
            },
            fields="id"
        ).execute()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.service:
            self.service.close()