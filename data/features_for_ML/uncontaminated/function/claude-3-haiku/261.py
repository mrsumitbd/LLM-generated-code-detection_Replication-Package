import requests
import os
import sys
import smtplib
from email.mime.text import MIMEText

def check_and_notify():
    """Check for updates and notify user if available.

    This is the main entry point for version checking.
    """
    # Check for updates
    current_version = get_current_version()
    latest_version = get_latest_version()

    if latest_version > current_version:
        # Notify user
        send_update_notification(latest_version)

def get_current_version():
    """Retrieve the current version of the application."""
    return float(os.environ.get("APP_VERSION", "1.0"))

def get_latest_version():
    """Fetch the latest version of the application from a remote source."""
    response = requests.get("https://example.com/latest_version.txt")
    return float(response.text.strip())

def send_update_notification(latest_version):
    """Send an email notification to the user about the available update."""
    msg = MIMEText(f"A new version of the application (v{latest_version}) is available. Please update.")
    msg["Subject"] = "Application Update Available"
    msg["From"] = "updates@example.com"
    msg["To"] = os.environ.get("USER_EMAIL", "user@example.com")

    with smtplib.SMTP("localhost") as smtp:
        smtp.send_message(msg)