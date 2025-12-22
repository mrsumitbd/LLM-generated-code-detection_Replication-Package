from urllib.parse import urlparse

def is_localhost_url(url: str) -> bool:
    """
    Check if a URL uses localhost-style hostname that should be replaced.

    Args:
        url: The URL to check

    Returns:
        bool: True if URL uses localhost/127.0.0.1/0.0.0.0, False for domains/external IPs
    """
    if not isinstance(url, str):
        return False

    # Strip whitespace
    url = url.strip()
    if not url:
        return False

    # Parse the URL
    parsed = urlparse(url)

    # If no hostname is present, it's not a full URL
    hostname = parsed.hostname
    if hostname is None:
        return False

    # Normalize hostname for comparison
    hostname = hostname.lower()

    # Check against known localhost identifiers
    return hostname in {"localhost", "127.0.0.1", "0.0.0.0"}