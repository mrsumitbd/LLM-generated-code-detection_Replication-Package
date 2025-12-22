import requests
from typing import List, Dict, Any, Optional, Union
import json
import time
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
    endpoint = "wanted/missing"
    page_size = 100  # Smaller page size for better performance
    retries = 2
    retry_delay = 3
    
    # Ensure api_url is properly formatted
    if not (api_url.startswith('http://') or api_url.startswith('https://')):
        logger.error(f"Invalid URL format: {api_url}")
        return []
    base_url = api_url.rstrip('/')
    url = f"{base_url}/api/v1/{endpoint.lstrip('/')}"
    
    # Add User-Agent header to identify Huntarr
    headers = {
        "X-Api-Key": api_key,
        "User-Agent": "Huntarr/1.0 (https://github.com/plexguide/Huntarr.io)",
        "Content-Type": "application/json"
    }
    
    # First, make a request to get just the total record count (page 1 with size=1)
    params = {
        'page': 1,
        'pageSize': 1
    }
    
    for attempt in range(retries + 1):
        try:
            # Get total record count from a minimal query
            logger.debug(f"Getting missing books count (attempt {attempt+1}/{retries+1})")
            response = requests.get(url, headers=headers, params=params, timeout=api_timeout)
            response.raise_for_status()
            
            if not response.content:
                logger.warning(f"Empty response when getting missing count (attempt {attempt+1})")
                if attempt < retries:
                    time.sleep(retry_delay)
                    continue
                return []
                
            try:
                data = response.json()
                total_records = data.get('totalRecords', 0)
                
                if total_records == 0:
                    logger.info("No missing books found in Readarr.")
                    return []
                    
                # Calculate total pages with our desired page size
                total_pages = (total_records + page_size - 1) // page_size
                logger.info(f"Found {total_records} total missing books across {total_pages} pages")
                
                if total_pages == 0:
                    return []
                    
                # Select a random page
                random_page = random.randint(1, total_pages)
                logger.info(f"Selected random page {random_page} of {total_pages} for missing books")
                
                # Get books from the random page
                params = {
                    'page': random_page,
                    'pageSize': page_size
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=api_timeout)
                response.raise_for_status()
                
                if not response.content:
                    logger.warning(f"Empty response when getting missing books page {random_page}")
                    return []
                    
                try:
                    data = response.json()
                    records = data.get('records', [])
                    logger.info(f"Retrieved {len(records)} missing books from page {random_page}")
                    
                    # Apply monitored filter if requested (Readarr API may not support this directly)
                    if monitored_only:
                        filtered_records = [
                            book for book in records
                            if book.get('monitored', False)
                        ]
                        logger.debug(f"Filtered to {len(filtered_records)} monitored missing books")
                        records = filtered_records
                    
                    # Select random books from this page
                    if len(records) > count:
                        selected_records = random.sample(records, count)
                        logger.debug(f"Randomly selected {len(selected_records)} missing books from page {random_page}")
                        return selected_records
                    else:
                        # If we have fewer books than requested, return all of them
                        logger.debug(f"Returning all {len(records)} missing books from page {random_page} (fewer than requested {count})")
                        return records
                        
                except json.JSONDecodeError as jde:
                    logger.error(f"Failed to decode JSON response for missing books page {random_page}: {str(jde)}")
                    if attempt < retries:
                        time.sleep(retry_delay)
                        continue
                    return []
                    
            except json.JSONDecodeError as jde:
                logger.error(f"Failed to decode JSON response for missing books count: {str(jde)}")
                if attempt < retries:
                    time.sleep(retry_delay)
                    continue
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting missing books from Readarr (attempt {attempt+1}): {str(e)}")
            if attempt < retries:
                time.sleep(retry_delay)
                continue
            return []
            
        except Exception as e:
            logger.error(f"Unexpected error getting missing books (attempt {attempt+1}): {str(e)}", exc_info=True)
            if attempt < retries:
                time.sleep(retry_delay)
                continue
            return []
    
    # If we get here, all retries failed
    logger.error("All attempts to get missing books failed")
    return []