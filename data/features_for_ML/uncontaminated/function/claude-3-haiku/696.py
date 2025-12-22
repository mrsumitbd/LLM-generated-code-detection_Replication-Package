import re

def is_valid_url(url):
    try:
        result = re.match(
            r'^(https?://)?([\da-z\.-]+)\.([a-z\.]{2,6})([/\w \.-]*)*/?$', url)
        return bool(result)
    except (TypeError, ValueError):
        return False