def get_version_from_url(download_url):
    """Extracts the version from the download URL.

    Args:
        download_url (str): The Bedrock server download URL.

    Returns:
        str: The version string (e.g., "1.20.1.2"), or None on error.
    """
    import re
    
    if not download_url or not isinstance(download_url, str):
        return None
    
    # Pattern to match version numbers like 1.20.1.2
    pattern = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, download_url)
    
    if match:
        return match.group(1)
    
    return None