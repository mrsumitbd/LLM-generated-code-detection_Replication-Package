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
    try:
        # First get the current movie data
        movie_data = arr_request(api_url, api_key, api_timeout, f"movie/{movie_id}", count_api=False)
        if not movie_data:
            eros_logger.error(f"Failed to get movie data for ID: {movie_id}")
            return False
        
        # Check if the tag is already present
        current_tags = movie_data.get('tags', [])
        if tag_id in current_tags:
            eros_logger.debug(f"Tag {tag_id} already exists on movie {movie_id}")
            return True
        
        # Add the new tag to the list
        current_tags.append(tag_id)
        movie_data['tags'] = current_tags
        
        # Update the movie with the new tags
        response = arr_request(api_url, api_key, api_timeout, f"movie/{movie_id}", method="PUT", data=movie_data, count_api=False)
        if response:
            eros_logger.debug(f"Successfully added tag {tag_id} to movie {movie_id}")
            return True
        else:
            eros_logger.error(f"Failed to update movie {movie_id} with tag {tag_id}")
            return False
            
    except Exception as e:
        eros_logger.error(f"Error adding tag {tag_id} to movie {movie_id}: {e}")
        return False