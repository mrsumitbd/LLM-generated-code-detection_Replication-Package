import requests
from typing import Any

def add_tag_to_movie(api_url: str, api_key: str, api_timeout: int, movie_id: int, tag_id: int) -> bool:
    """
    Add a tag to a movie in Eros.

    Args:
        api_url: The base URL of the Eros API
        api_key: The API key for authentication
        api_timeout: Timeout for the API request
        movie_id: The ID of the movie to tag
        tag_id: The ID of the tag to add

    Returns:
        True if successful, False otherwise
    """
    # Build the endpoint URL
    endpoint = f"{api_url.rstrip('/')}/movies/{movie_id}/tags"

    # Prepare headers and payload
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {"tag_id": tag_id}

    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=api_timeout,
        )
        # Consider any 2xx status code as success
        return 200 <= response.status_code < 300
    except (requests.RequestException, ValueError):
        # Log or handle errors as needed; for now just return False
        return False