import requests

def http_get(url, path):
    """
    Downloads a URL to a given path on disc
    """
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)