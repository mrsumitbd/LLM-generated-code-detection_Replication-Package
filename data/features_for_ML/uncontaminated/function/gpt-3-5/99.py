def send_claude_session_log(session_id: str, log_entry: dict, org_id: Optional[int] = None) -> bool:
    import requests

    url = f"https://claude-code.com/api/session/{session_id}/log"
    headers = {'Content-Type': 'application/json'}

    if org_id is not None:
        params = {'org_id': org_id}
    else:
        params = {}

    response = requests.post(url, json=log_entry, headers=headers, params=params)

    if response.status_code == 200:
        return True
    else:
        return False