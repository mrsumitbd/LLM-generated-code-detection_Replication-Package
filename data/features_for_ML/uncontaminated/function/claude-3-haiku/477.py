import requests

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
    headers = {
        "X-Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "seriesId": series_id,
        "tagIds": [tag_id]
    }
    
    try:
        response = requests.post(f"{api_url}/api/v3/series/{series_id}/tags", headers=headers, json=data, timeout=api_timeout)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error adding tag to series: {e}")
        return False