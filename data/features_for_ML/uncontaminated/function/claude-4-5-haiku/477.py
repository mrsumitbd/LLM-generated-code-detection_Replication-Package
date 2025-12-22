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
    import requests
    
    try:
        # Get the series first
        get_url = f"{api_url}/api/v3/series/{series_id}"
        headers = {"X-Api-Key": api_key}
        
        response = requests.get(get_url, headers=headers, timeout=api_timeout)
        response.raise_for_status()
        
        series_data = response.json()
        
        # Add the tag to the series tags list if not already present
        if "tags" not in series_data:
            series_data["tags"] = []
        
        if tag_id not in series_data["tags"]:
            series_data["tags"].append(tag_id)
        
        # Update the series with the new tags
        put_url = f"{api_url}/api/v3/series/{series_id}"
        response = requests.put(put_url, json=series_data, headers=headers, timeout=api_timeout)
        response.raise_for_status()
        
        return True
    except Exception:
        return False