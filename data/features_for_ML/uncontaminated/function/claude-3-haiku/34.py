import requests

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
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'movie_id': movie_id,
        'tag_id': tag_id
    }
    
    try:
        response = requests.post(f'{api_url}/movies/{movie_id}/tags', headers=headers, json=data, timeout=api_timeout)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f'Error adding tag to movie: {e}')
        return False