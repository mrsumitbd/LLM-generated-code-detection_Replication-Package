import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD", "OPTIONS"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as exc:
        # If all retries fail, re-raise the last exception
        raise exc