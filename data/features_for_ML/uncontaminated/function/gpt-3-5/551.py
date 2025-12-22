from typing import List, Dict
import requests
import random

def get_wanted_missing_books_random_page(api_url: str, api_key: str, api_timeout: int, monitored_only: bool, count: int) -> List[Dict]:
    headers = {'X-Api-Key': api_key}
    params = {'monitored': str(monitored_only).lower()}
    response = requests.get(f'{api_url}/api/v1/wanted/missing', headers=headers, params=params, timeout=api_timeout)
    
    if response.status_code == 200:
        missing_books = response.json()
        random_missing_books = random.sample(missing_books, min(count, len(missing_books)))
        return random_missing_books
    else:
        return []

# Example usage:
# books = get_wanted_missing_books_random_page('https://example.com', 'your_api_key', 10, True, 5)
# print(books)