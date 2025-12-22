from urllib.parse import urlparse

def is_localhost_url(url: str) -> bool:
    """Check if a URL uses localhost-style hostname that should be replaced.

    Args:
        url: The URL to check

    Returns:
        bool: True if URL uses localhost/127.0.0.1/0.0.0.0, False for domains/external IPs
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)
        return parsed.hostname in ("localhost", "127.0.0.1", "0.0.0.0")
    except Exception:
        return False