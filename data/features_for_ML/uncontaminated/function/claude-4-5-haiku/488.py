def is_localhost_url(url: str) -> bool:
    """Check if a URL uses localhost-style hostname that should be replaced.

    Args:
        url: The URL to check

    Returns:
        bool: True if URL uses localhost/127.0.0.1/0.0.0.0, False for domains/external IPs
    """
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        
        if hostname is None:
            return False
        
        hostname_lower = hostname.lower()
        
        # Check for localhost, 127.0.0.1, and 0.0.0.0
        if hostname_lower in ('localhost', '127.0.0.1', '0.0.0.0', '::1'):
            return True
        
        # Check for 127.x.x.x range
        if hostname_lower.startswith('127.'):
            return True
        
        return False
    except Exception:
        return False