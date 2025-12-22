import re
from urllib.parse import urlparse

def _get_domain_name_for_file(url: str) -> str:
    """
    Generate a unique filename prefix from the URL.

    Args:
        url: URL to generate filename from

    Returns:
        A string with the domain name formatted for a filename
    """
    if not url:
        return ""

    parsed = urlparse(url)
    netloc = parsed.netloc or url  # fallback if url is just a hostname

    # Strip port if present
    if ":" in netloc:
        if netloc.startswith("["):
            # IPv6 address: [::1]:port
            host = netloc.split("]")[0][1:]
        else:
            host = netloc.split(":")[0]
    else:
        host = netloc

    # Remove IPv6 brackets if any
    host = host.strip("[]")

    # Replace any non‑alphanumeric, dot, underscore or hyphen with underscore
    sanitized = re.sub(r"[^A-Za-z0-9._-]", "_", host)

    # Collapse consecutive underscores
    sanitized = re.sub(r"_+", "_", sanitized)

    return sanitized