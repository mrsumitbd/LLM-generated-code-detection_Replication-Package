def http_get(url, path):
    import requests
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)