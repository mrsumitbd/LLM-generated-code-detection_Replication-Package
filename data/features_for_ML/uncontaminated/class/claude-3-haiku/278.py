from googleapiclient.discovery import build
from google.oauth2 import service_account

class SpreadsheetContext:
    """Context for Google Spreadsheet service"""

    def __init__(self, credentials_file, scopes=None):
        self.credentials_file = credentials_file
        self.scopes = scopes or ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials = None
        self.service = None

    def __enter__(self):
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file, scopes=self.scopes)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        return self.service

    def __exit__(self, exc_type, exc_value, traceback):
        self.service = None
        self.credentials = None