from typing import Optional
import requests
from codegen.cli.api.endpoints import API_ENDPOINT
from codegen.cli.auth.token_manager import get_current_token
from codegen.cli.utils.org import resolve_org_id
from .quiet_console import console

def send_claude_session_log(session_id: str, log_entry: dict, org_id: Optional[int] = None) -> bool:
    """Send a log entry to the Claude Code session log endpoint.

    Args:
        session_id: The session ID
        log_entry: The log entry to send (dict)
        org_id: Organization ID (will be resolved if None)

    Returns:
        True if successful, False if failed
    """
    try:
        # Resolve org_id
        resolved_org_id = resolve_org_id(org_id)
        if resolved_org_id is None:
            console.print("⚠️  Could not resolve organization ID for log sending", style="yellow")
            return False

        # Get authentication token
        token = get_current_token()
        if not token:
            console.print("⚠️  No authentication token found for log sending", style="yellow")
            return False

        # Prepare API request
        url = f"{API_ENDPOINT.rstrip('/')}/v1/organizations/{resolved_org_id}/claude_code/session/{session_id}/log"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"log": log_entry}

        # Make API request
        response = requests.post(url, json=payload, headers=headers, timeout=30)

        if response.status_code == 200:
            return True
        else:
            error_msg = f"HTTP {response.status_code}"
            try:
                error_detail = response.json().get("detail", response.text)
                error_msg = f"{error_msg}: {error_detail}"
            except Exception:
                error_msg = f"{error_msg}: {response.text}"

            console.print(f"⚠️  Failed to send log entry: {error_msg}", style="yellow")
            return False

    except requests.RequestException as e:
        console.print(f"⚠️  Network error sending log entry: {e}", style="yellow")
        return False
    except Exception as e:
        console.print(f"⚠️  Unexpected error sending log entry: {e}", style="yellow")
        return False