def _get_domain_name_for_file(url: str) -> str:
    """
    Generate a unique filename prefix from the URL.
    
    Args:
        url: URL to generate filename from
        
    Returns:
        A string with the domain name formatted for a filename
    """
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split('/')[0]
    
    # Remove 'www.' prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Replace dots and hyphens with underscores for filename safety
    domain = domain.replace('.', '_').replace('-', '_')
    
    return domain