import requests

def _get_github_api(
    endpoint: str, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, Optional[Dict]]:
    """Make a GET request to GitHub API and return (success, response)."""
    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, None