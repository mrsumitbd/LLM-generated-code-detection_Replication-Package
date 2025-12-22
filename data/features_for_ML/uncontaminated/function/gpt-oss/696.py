import re
from urllib.parse import urlparse

def is_valid_url(url):
    """
    Return True if `url` is a syntactically valid URL, otherwise False.
    The function accepts URLs with schemes http, https, ftp, and file.
    """
    if not isinstance(url, str):
        return False

    # Basic scheme check: must start with a scheme followed by ://
    # Allow file:// or file: (no netloc)
    parsed = urlparse(url)

    # Scheme must be present and alphabetic
    if not parsed.scheme or not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*$', parsed.scheme):
        return False

    scheme = parsed.scheme.lower()

    # For http, https, ftp: netloc must be non-empty
    if scheme in {'http', 'https', 'ftp'}:
        if not parsed.netloc:
            return False
        # Basic host validation: at least one dot or a valid IP
        host = parsed.hostname
        if not host:
            return False
        # Allow IPv4 or IPv6 or domain names
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        ipv6_pattern = r'^\[([0-9a-fA-F:]+)\]$'
        if not (re.match(ipv4_pattern, host) or re.match(ipv6_pattern, host) or re.match(r'^[a-zA-Z0-9.-]+$', host)):
            return False

    # For file scheme: netloc can be empty, but path must be non-empty
    elif scheme == 'file':
        if not parsed.path:
            return False

    else:
        # Unsupported scheme
        return False

    # If we reach here, the URL passes basic checks
    return True