import requests

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
    try:
        headers = {
            "X-Api-Key": api_key
        }
        response = requests.get(f"{api_url}/api/queue", headers=headers, timeout=api_timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return []