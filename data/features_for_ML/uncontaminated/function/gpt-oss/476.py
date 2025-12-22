import re

def get_soundcloud_track_id(url):
    """
    Extract the numeric track ID from a SoundCloud URL if present.
    Supports URLs that contain the pattern /tracks/<id>.
    Returns the ID as an integer, or None if not found.
    """
    if not isinstance(url, str):
        return None
    match = re.search(r"/tracks/(\d+)", url)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return None
    return None