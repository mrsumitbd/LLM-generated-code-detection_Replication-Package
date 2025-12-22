import requests

def retrieve_page_data(
    url: str, retries: int = 3, timeout: int = 60 * 5
) -> requests.Response:
    """
    Retrieves data from the given URL.
    :param url: URL
    :param retries: Number of retries
    :param timeout: Timeout (in seconds)
    :return: URL data
    """
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving data from {url}: {e}")
    raise Exception(f"Failed to retrieve data from {url} after {retries} retries.")