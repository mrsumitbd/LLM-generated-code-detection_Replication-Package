def _get_domain_name_for_file(url: str) -> str:
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    domain_parts = domain.split('.')
    if len(domain_parts) > 2:
        domain = '.'.join(domain_parts[-2:])
    return domain.replace('.', '_')