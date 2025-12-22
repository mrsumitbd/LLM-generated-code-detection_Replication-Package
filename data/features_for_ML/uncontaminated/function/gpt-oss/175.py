import json
import os
from pathlib import Path

import typer
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes for Gmail and Calendar
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
]


def setup_google(
    credentials_file: str = typer.Option(
        "credentials.json",
        "--credentials-file",
        "-c",
        help="Path to Google OAuth credentials JSON file",
    ),
    user_storage: str = typer.Option(
        "credentials.my_google_account.json",
        "--user-storage",
        "-u",
        help="Where to save user credentials",
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Force re-authentication even if credentials exist"
    ),
):
    """Set up Google authentication for Gmail and Calendar access."""
    # Resolve paths
    cred_path = Path(credentials_file).expanduser().resolve()
    storage_path = Path(user_storage).expanduser().resolve()

    # Load existing credentials if available and not forcing re-auth
    creds = None
    if storage_path.exists() and not force:
        try:
            creds = Credentials.from_authorized_user_file(str(storage_path), SCOPES)
        except Exception:
            creds = None

    # If no valid credentials, start OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
        if not creds:
            if not cred_path.exists():
                typer.echo(f"Credentials file not found: {cred_path}")
                raise FileNotFoundError(str(cred_path))
            flow = InstalledAppFlow.from_client_secrets_file(
                str(cred_path), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(storage_path, "w") as token_file:
            token_file.write(creds.to_json())

    typer.echo(f"Google credentials set up successfully. Stored at {storage_path}")