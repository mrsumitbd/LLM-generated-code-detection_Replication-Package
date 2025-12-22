import re

def get_soundcloud_track_id(url):
    pattern = r'https?://(?:www\.)?soundcloud\.com/[^/]+/([^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None