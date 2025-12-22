import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import google.oauth2.credentials

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
    scopes = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly']

    if os.path.exists(user_storage) and not force:
        print(f"Using existing credentials from {user_storage}")
        creds = google.oauth2.credentials.Credentials.from_authorized_user_info(
            info=json.load(open(user_storage, 'r')))
    else:
        print(f"Authenticating using credentials from {credentials_file}")
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_file, scopes)
        creds = flow.run_console()
        with open(user_storage, 'w') as token:
            token.write(creds.to_json())

    gmail_service = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
    calendar_service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

    return gmail_service, calendar_service