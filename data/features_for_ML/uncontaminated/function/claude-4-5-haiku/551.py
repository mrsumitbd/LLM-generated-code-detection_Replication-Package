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
    import requests
    import random
    
    headers = {"X-Api-Key": api_key}
    
    # First, get the total count of missing books
    params = {
        "status": "missing",
        "pageSize": 1,
        "page": 1
    }
    
    if monitored_only:
        params["monitored"] = "true"
    
    try:
        response = requests.get(
            f"{api_url}/api/v1/book",
            headers=headers,
            params=params,
            timeout=api_timeout
        )
        response.raise_for_status()
        data = response.json()
        
        total_records = data.get("totalRecords", 0)
        
        if total_records == 0:
            return []
        
        # Calculate page size and total pages
        page_size = 50
        total_pages = (total_records + page_size - 1) // page_size
        
        # Collect books from random pages
        collected_books = []
        pages_to_fetch = min(count, total_pages)
        random_pages = random.sample(range(1, total_pages + 1), pages_to_fetch)
        
        for page in random_pages:
            params = {
                "status": "missing",
                "pageSize": page_size,
                "page": page
            }
            
            if monitored_only:
                params["monitored"] = "true"
            
            response = requests.get(
                f"{api_url}/api/v1/book",
                headers=headers,
                params=params,
                timeout=api_timeout
            )
            response.raise_for_status()
            data = response.json()
            
            books = data.get("records", [])
            collected_books.extend(books)
            
            if len(collected_books) >= count:
                break
        
        # Randomly shuffle and return the requested count
        random.shuffle(collected_books)
        return collected_books[:count]
        
    except requests.exceptions.RequestException:
        return []