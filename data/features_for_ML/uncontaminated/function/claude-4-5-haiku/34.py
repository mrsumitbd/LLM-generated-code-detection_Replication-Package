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
    import requests
    
    try:
        url = f"{api_url}/movie/{movie_id}/tag/{tag_id}"
        headers = {
            "X-API-Key": api_key
        }
        response = requests.post(url, headers=headers, timeout=api_timeout)
        return response.status_code in (200, 201)
    except Exception:
        return False