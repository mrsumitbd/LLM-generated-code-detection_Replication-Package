from typing import List, Dict, Optional
import requests


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
    # Build the request URL and parameters
    endpoint = f"{api_url.rstrip('/')}/api/movie"
    params = {}
    if monitored_only:
        params["monitored"] = "true"

    headers = {"X-Api-Key": api_key}

    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=api_timeout)
        response.raise_for_status()
    except (requests.RequestException, ValueError):
        return None

    try:
        movies = response.json()
    except ValueError:
        return None

    # Filter movies that have no file information (missing files)
    missing_movies = [movie for movie in movies if not movie.get("file")]

    return missing_movies