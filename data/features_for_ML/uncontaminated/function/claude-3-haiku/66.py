import requests

def _get_file_content(
    file_path: str,
    headers: Dict[str, str],
    org: str,
    repo: str = "build-your-own-x",
    ref: str = "master",
) -> Optional[str]:
    """Get the content of a file from the repository."""
    url = f"https://api.github.com/repos/{org}/{repo}/contents/{file_path}?ref={ref}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("content")
    return None