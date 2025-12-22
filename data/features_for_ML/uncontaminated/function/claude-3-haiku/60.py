def get_version_from_url(download_url):
    """Extracts the version from the download URL.

    Args:
        download_url (str): The Bedrock server download URL.

    Returns:
        str: The version string (e.g., "1.20.1.2"), or None on error.
    """
    try:
        version_start = download_url.rfind('/') + 1
        version_end = download_url.rfind('.')
        version = download_url[version_start:version_end]
        return version
    except (ValueError, IndexError):
        return None