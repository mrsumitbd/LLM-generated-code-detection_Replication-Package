from typing import List, Any
import requests

def get_queue(api_url: str, api_key: str, api_timeout: int) -> List[Any]:
    """
    Get the current queue from Sonarr.

    Args:
        api_url: The base URL of the Sonarr API
        api_key: The API key for authentication
        api_timeout: Timeout for the API request

    Returns:
        Queue information or empty list if request failed
    """
    # Ensure the base URL does not end with a slash
    base = api_url.rstrip("/")
    url = f"{base}/queue"

    headers = {
        "X-Api-Key": api_key,
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers, timeout=api_timeout)
        response.raise_for_status()
        data = response.json()
        # Sonarr returns a list of queue items
        if isinstance(data, list):
            return data
        # If the API returns a dict with a 'data' key, return that
        if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
            return data["data"]
        # Unexpected format, return empty list
        return []
    except (requests.RequestException, ValueError):
        # Any network error or JSON decoding error results in an empty list
        return []