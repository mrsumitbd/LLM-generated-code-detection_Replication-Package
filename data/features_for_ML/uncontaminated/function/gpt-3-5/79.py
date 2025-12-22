def get_queue(api_url: str, api_key: str, api_timeout: int) -> List:
    import requests

    headers = {'X-Api-Key': api_key}
    url = f'{api_url}/api/queue'
    
    try:
        response = requests.get(url, headers=headers, timeout=api_timeout)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        pass
    
    return []