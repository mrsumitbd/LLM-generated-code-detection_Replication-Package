import re

def get_version_from_url(download_url):
    """Extracts the version from the download URL.

    Args:
        download_url (str): The Bedrock server download URL.

    Returns:
        str: The version string (e.g., "1.20.1.2"), or None on error.
    """
    action = "get version from url"
    if not download_url:
        msg_error("download_url is empty.")
        handle_error(2, action)
        return None

    match = re.search(r"bedrock-server-([0-9.]+)", download_url)
    if match:
        version = match.group(1)
        return version.rstrip(".")  # Remove trailing dot if present
    else:
        msg_error("Failed to extract version from URL.")
        return None