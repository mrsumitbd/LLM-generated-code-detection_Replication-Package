import requests
import random

def get_wanted_missing_books_random_page(api_url: str, api_key: str, api_timeout: int, monitored_only: bool, count: int) -> List[Dict]:
    """
    Get a specified number of random missing books by selecting a random page.
    This is much more efficient for very large libraries.
    
    Args:
        api_url: The base URL of the Readarr API
        api_key: The API key for authentication
        api_timeout: Timeout for the API request
        monitored_only: Whether to include only monitored books
        count: How many books to return
        
    Returns:
        A list of randomly selected missing books, up to the requested count
    """
    headers = {
        "X-Api-Key": api_key
    }
    
    params = {
        "pageSize": 100,
        "monitored": monitored_only,
        "sortKey": "random",
        "sortDirection": "ascending"
    }
    
    missing_books = []
    
    while len(missing_books) < count:
        params["page"] = random.randint(1, 100)
        response = requests.get(f"{api_url}/api/v1/wanted/missing", headers=headers, params=params, timeout=api_timeout)
        response.raise_for_status()
        data = response.json()
        missing_books.extend(data["records"])
        
        if len(data["records"]) < 100:
            break
    
    return random.sample(missing_books, min(count, len(missing_books)))