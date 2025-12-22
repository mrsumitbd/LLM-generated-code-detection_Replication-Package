def _get_file_content(
    file_path: str,
    headers: Dict[str, str],
    org: str,
    repo: str = "build-your-own-x",
    ref: str = "master",
) -> Optional[str]:
    import requests
    from typing import Dict, Optional

    url = f"https://api.github.com/repos/{org}/{repo}/contents/{file_path}?ref={ref}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.json().get('content')
        if content:
            return base64.b64decode(content).decode('utf-8')
    
    return None