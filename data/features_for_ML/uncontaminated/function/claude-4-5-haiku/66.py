def _get_file_content(
    file_path: str,
    headers: Dict[str, str],
    org: str,
    repo: str = "build-your-own-x",
    ref: str = "master",
) -> Optional[str]:
    """Get the content of a file from the repository."""
    import requests
    import base64
    
    url = f"https://api.github.com/repos/{org}/{repo}/contents/{file_path}"
    params = {"ref": ref}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if "content" in data:
            content = data["content"]
            if data.get("encoding") == "base64":
                content = base64.b64decode(content).decode("utf-8")
            return content
        
        return None
    except Exception:
        return None