import urllib.parse
import urllib.parse

def _get_domain_name_for_file(url: str) -> str:
    """
    Generate a unique filename prefix from the URL.
    
    Args:
        url: URL to generate filename from
        
    Returns:
        A string with the domain name formatted for a filename
    """
    # This is a simplified version of the Go code's getDomainNameForFile function
    import urllib.parse
    
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc.replace(".", "_")
        path = parsed_url.path.strip("/")
        
        if not path:
            return domain
        
        path = path.replace("/", "_")
        return f"{domain}_{path}"
    except Exception:
        return "unknown"