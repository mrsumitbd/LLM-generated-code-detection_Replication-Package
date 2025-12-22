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
    try:
        # First get the current series data
        series_data = arr_request(api_url, api_key, api_timeout, f"series/{series_id}", count_api=False)
        if not series_data:
            sonarr_logger.error(f"Failed to get series data for ID: {series_id}")
            return False
        
        # Check if the tag is already present
        current_tags = series_data.get('tags', [])
        if tag_id in current_tags:
            sonarr_logger.debug(f"Tag {tag_id} already exists on series {series_id}")
            return True
        
        # Add the new tag to the list
        current_tags.append(tag_id)
        series_data['tags'] = current_tags
        
        # Update the series with the new tags
        response = arr_request(api_url, api_key, api_timeout, f"series/{series_id}", method="PUT", data=series_data, count_api=False)
        if response:
            sonarr_logger.debug(f"Successfully added tag {tag_id} to series {series_id}")
            return True
        else:
            sonarr_logger.error(f"Failed to update series {series_id} with tag {tag_id}")
            return False
            
    except Exception as e:
        sonarr_logger.error(f"Error adding tag {tag_id} to series {series_id}: {e}")
        return False