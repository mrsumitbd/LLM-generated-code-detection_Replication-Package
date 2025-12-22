from typing import List, Dict, Any, Optional, Union

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
    # Use the updated arr_request with passed arguments
    # Use arr_request with count_api=False for data fetching (doesn't count toward API tally)
    movies = arr_request(api_url, api_key, api_timeout, "movie", count_api=False)
    if movies is None: # Check for None explicitly, as an empty list is valid
        radarr_logger.error("Failed to retrieve movies from Radarr API.")
        return None
    
    missing_movies = []
    for movie in movies:
        is_monitored = movie.get("monitored", False)
        has_file = movie.get("hasFile", False)
        # Apply monitored_only filter if requested
        if not has_file and (not monitored_only or is_monitored):
            missing_movies.append(movie)
    
    radarr_logger.debug(f"Found {len(missing_movies)} missing movies (monitored_only={monitored_only}).")
    return missing_movies