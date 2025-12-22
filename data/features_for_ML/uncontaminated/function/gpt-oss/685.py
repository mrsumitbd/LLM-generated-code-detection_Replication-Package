import requests
from typing import Dict, Tuple, Optional

def _get_github_api(
    endpoint: str, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, Optional[Dict]]:
    """
    Make a GET request to GitHub API and return (success, response).

    Parameters
    ----------
    endpoint : str
        The API endpoint path *after* the repository path. For example,
        ``"/commits"`` or ``"/issues?state=open"``.
    headers : Dict[str, str]
        HTTP headers to send with the request (e.g. authentication token).
    owner : str
        Repository owner.
    repo : str
        Repository name.

    Returns
    -------
    Tuple[bool, Optional[Dict]]
        ``(True, data)`` if the request succeeded (HTTP 200) and the body
        could be parsed as JSON. ``(False, None)`` otherwise.
    """
    base_url = "https://api.github.com"
    # Ensure the endpoint starts with a slash
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
    url = f"{base_url}/repos/{owner}/{repo}{endpoint}"

    try:
        resp = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        return False, None

    if resp.status_code != 200:
        return False, None

    try:
        data = resp.json()
    except ValueError:
        return False, None

    return True, data