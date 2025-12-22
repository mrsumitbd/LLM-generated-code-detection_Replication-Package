import random
from typing import List, Dict
import requests

def get_wanted_missing_books_random_page(
    api_url: str,
    api_key: str,
    api_timeout: int,
    monitored_only: bool,
    count: int
) -> List[Dict]:
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
    # Build the base endpoint
    endpoint = f"{api_url.rstrip('/')}/api/v1/missing"

    # Common headers
    headers = {
        "Accept": "application/json",
        "X-Api-Key": api_key
    }

    # Helper to perform a GET request
    def _get(params: dict) -> dict:
        try:
            resp = requests.get(
                endpoint,
                headers=headers,
                params=params,
                timeout=api_timeout
            )
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return {}

    # 1. Get total pages (request a single item)
    params = {
        "page": 1,
        "pageSize": 1,
        "monitored": str(monitored_only).lower()
    }
    first_page = _get(params)
    total_pages = first_page.get("totalPages", 1)

    # 2. Pick a random page
    random_page = random.randint(1, total_pages)

    # 3. Request the random page with desired pageSize
    params = {
        "page": random_page,
        "pageSize": count,
        "monitored": str(monitored_only).lower()
    }
    page_data = _get(params)

    # 4. Return the list of books
    return page_data.get("data", []) if isinstance(page_data, dict) else []