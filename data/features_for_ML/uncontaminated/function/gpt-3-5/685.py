def _get_github_api(
    endpoint: str, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, Optional[Dict]]:
    import requests

    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False, None