import re

def get_version_from_url(download_url):
    """Extracts the version from the download URL.

    Args:
        download_url (str): The Bedrock server download URL.

    Returns:
        str: The version string (e.g., "1.20.1.2"), or None on error.
    """
    if not download_url:
        return None

    # Prefer a version that follows 'bedrock-server-'
    match = re.search(r'bedrock-server-(\d+\.\d+\.\d+\.\d+)', download_url)
    if match:
        return match.group(1)

    # General 4-part version pattern
    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', download_url)
    if match:
        return match.group(1)

    # Fallback to 3-part version pattern
    match = re.search(r'(\d+\.\d+\.\d+)', download_url)
    if match:
        return match.group(1)

    return None