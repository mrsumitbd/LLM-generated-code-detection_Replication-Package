import requests

def retrieve_page_data(url: str, retries: int = 3, timeout: int = 60 * 5) -> requests.Response:
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return response
        except requests.RequestException:
            pass
    return requests.Response()