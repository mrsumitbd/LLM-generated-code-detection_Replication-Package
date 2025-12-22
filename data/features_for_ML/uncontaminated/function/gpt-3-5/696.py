def is_valid_url(url):
    import re
    regex = r"^(http|https)://[a-zA-Z0-9-._~:/?#[\]@!$&'()*+,;=]+$"
    return re.match(regex, url) is not None