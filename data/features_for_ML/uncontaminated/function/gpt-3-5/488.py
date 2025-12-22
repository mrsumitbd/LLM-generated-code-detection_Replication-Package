def is_localhost_url(url: str) -> bool:
    return any(hostname in url for hostname in ['localhost', '127.0.0.1', '0.0.0.0'])