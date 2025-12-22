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
    import os
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/calendar.readonly",
    ]
    
    creds = None
    
    if os.path.exists(user_storage) and not force:
        creds = Credentials.from_authorized_user_file(user_storage, SCOPES)
        typer.echo(f"✓ Loaded existing credentials from {user_storage}")
    
    if creds is None or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            typer.echo("✓ Refreshed existing credentials")
        else:
            if not os.path.exists(credentials_file):
                typer.echo(
                    f"✗ Credentials file not found: {credentials_file}",
                    err=True,
                )
                typer.echo(
                    "Please download OAuth 2.0 credentials from Google Cloud Console",
                    err=True,
                )
                raise typer.Exit(code=1)
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES
            )
            creds = flow.run_local_server(port=0)
            typer.echo("✓ Successfully authenticated with Google")
        
        with open(user_storage, "w") as token:
            token.write(creds.to_json())
        typer.echo(f"✓ Saved credentials to {user_storage}")
    
    typer.echo("✓ Google authentication setup complete")