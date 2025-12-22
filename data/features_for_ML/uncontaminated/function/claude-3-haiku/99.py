import requests
from typing import Optional

def send_claude_session_log(session_id: str, log_entry: dict, org_id: Optional[int] = None) -> bool:
    """Send a log entry to the Claude Code session log endpoint.

    Args:
        session_id: The session ID
        log_entry: The log entry to send (dict)
        org_id: Organization ID (will be resolved if None)

    Returns:
        True if successful, False if failed
    """
    url = f"https://api.claude.ai/v1/sessions/{session_id}/logs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_access_token(org_id)}"
    }
    try:
        response = requests.post(url, json=log_entry, headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending log entry: {e}")
        return False

def get_access_token(org_id: Optional[int] = None) -> str:
    """Retrieve the access token for the specified organization."""
    # Implement the logic to retrieve the access token
    # This is a placeholder implementation
    return "your_access_token"