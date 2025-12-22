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
    import requests
    
    try:
        # Construct the API endpoint URL
        endpoint = f"{api_url}/api/v3/movie"
        
        # Set up headers with API key
        headers = {
            "X-Api-Key": api_key
        }
        
        # Make the API request
        response = requests.get(
            endpoint,
            headers=headers,
            timeout=api_timeout
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the JSON response
        movies = response.json()
        
        # Filter for movies with missing files
        missing_movies = [movie for movie in movies if not movie.get("hasFile", False)]
        
        # Filter for monitored movies if requested
        if monitored_only:
            missing_movies = [movie for movie in missing_movies if movie.get("monitored", False)]
        
        return missing_movies
        
    except requests.exceptions.RequestException:
        return None
    except (ValueError, KeyError):
        return None