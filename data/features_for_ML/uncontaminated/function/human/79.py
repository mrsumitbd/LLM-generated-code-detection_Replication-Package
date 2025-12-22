from typing import List, Dict, Any, Optional, Union, Callable

def get_queue(api_url: str, api_key: str, api_timeout: int) -> List:
    """
    Get the current queue from Sonarr.
    
    Args:
        api_url: The base URL of the Sonarr API
        api_key: The API key for authentication
        api_timeout: Timeout for the API request
    
    Returns:
        Queue information or empty list if request failed
    """
    response = arr_request(api_url, api_key, api_timeout, "queue", count_api=False)
    if not response or "records" not in response:
        return []
    
    return response.get("records", [])