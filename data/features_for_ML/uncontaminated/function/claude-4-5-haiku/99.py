def send_claude_session_log(session_id: str, log_entry: dict, org_id: Optional[int] = None) -> bool:
    """Send a log entry to the Claude Code session log endpoint.

    Args:
        session_id: The session ID
        log_entry: The log entry to send (dict)
        org_id: Organization ID (will be resolved if None)

    Returns:
        True if successful, False if failed
    """
    import requests
    from typing import Optional
    
    try:
        # Resolve org_id if not provided
        if org_id is None:
            # Attempt to get org_id from environment or configuration
            import os
            org_id = os.getenv('ORG_ID')
            if org_id is None:
                return False
            try:
                org_id = int(org_id)
            except (ValueError, TypeError):
                return False
        
        # Construct the endpoint URL
        base_url = os.getenv('CLAUDE_API_BASE_URL', 'https://api.anthropic.com')
        endpoint = f"{base_url}/v1/claude-code/sessions/{session_id}/logs"
        
        # Get API key from environment
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            return False
        
        # Prepare headers
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'X-Organization-ID': str(org_id)
        }
        
        # Send the request
        response = requests.post(
            endpoint,
            json=log_entry,
            headers=headers,
            timeout=10
        )
        
        # Check if the request was successful
        return response.status_code in (200, 201, 204)
        
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return False