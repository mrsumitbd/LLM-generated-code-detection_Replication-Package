import os
import json
from typing import Optional
import requests

def send_claude_session_log(session_id: str, log_entry: dict, org_id: Optional[int] = None) -> bool:
    """
    Send a log entry to the Claude Code session log endpoint.

    Args:
        session_id: The session ID
        log_entry: The log entry to send (dict)
        org_id: Organization ID (will be resolved if None)

    Returns:
        True if successful, False if failed
    """
    # Base URL for the Claude Code session log endpoint
    base_url = "https://api.anthropic.com/v1/claude/code/session_logs"

    # Build the full URL with the session ID
    url = f"{base_url}/{session_id}"

    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Add organization header if provided
    if org_id is not None:
        headers["X-Organization-Id"] = str(org_id)

    # Add API key header if available
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.post(url, headers=headers, data=json.dumps(log_entry), timeout=10)
        response.raise_for_status()
        return True
    except (requests.RequestException, ValueError):
        return False