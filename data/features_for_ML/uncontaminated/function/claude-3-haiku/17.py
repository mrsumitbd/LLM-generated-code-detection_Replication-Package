import requests
from typing import Optional, List, Dict

def get_movies_with_missing(api_url: str, api_key: str, api_timeout: int, monitored_only: bool) -> Optional[List[Dict]]:
    """
    Get a list of movies with missing files (not downloaded/available).

    Args:
        api_url: The base URL of the Radarr API
        api_key: The API key for authentication
        api_timeout: Timeout for the API request
        monitored_only: If True, only return monitored movies.

    Returns:
        A list of movie objects with missing files, or None if the request failed.
    """
    headers = {
        "X-Api-Key": api_key
    }

    params = {
        "monitored": monitored_only,
        "sortDirection": "asc",
        "sortKey": "title"
    }

    try:
        response = requests.get(f"{api_url}/api/v3/movie", headers=headers, params=params, timeout=api_timeout)
        response.raise_for_status()
        movies = response.json()

        missing_movies = [movie for movie in movies if movie["hasFile"] is False]
        return missing_movies
    except requests.exceptions.RequestException as e:
        return None