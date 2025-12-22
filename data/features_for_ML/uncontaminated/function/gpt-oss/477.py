import requests
from typing import Any

def add_tag_to_series(api_url: str, api_key: str, api_timeout: int, series_id: int, tag_id: int) -> bool:
    """
    Add a tag to a series in Sonarr.

    Args:
        api_url: The base URL of the Sonarr API
        api_key: The API key for authentication
        api_timeout: Timeout for the API request
        series_id: The ID of the series to tag
        tag_id: The ID of the tag to add

    Returns:
        True if successful, False otherwise
    """
    # Build the request URL
    url = f"{api_url.rstrip('/')}/series/{series_id}/tag"
    params = {"tagId": tag_id}
    headers = {"X-Api-Key": api_key}

    try:
        response = requests.post(url, headers=headers, params=params, timeout=api_timeout)
        # Sonarr returns 204 No Content on success
        return 200 <= response.status_code < 300
    except (requests.RequestException, Exception):
        return False