def add_tag_to_series(api_url: str, api_key: str, api_timeout: int, series_id: int, tag_id: int) -> bool:
    import requests

    headers = {
        'X-Api-Key': api_key,
        'Content-Type': 'application/json'
    }

    data = {
        'seriesId': series_id,
        'tagId': tag_id
    }

    try:
        response = requests.post(f'{api_url}/api/v3/series/{series_id}/tag', headers=headers, json=data, timeout=api_timeout)
        if response.status_code == 201:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False