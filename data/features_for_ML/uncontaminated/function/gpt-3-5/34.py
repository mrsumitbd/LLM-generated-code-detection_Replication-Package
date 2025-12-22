def add_tag_to_movie(api_url: str, api_key: str, api_timeout: int, movie_id: int, tag_id: int) -> bool:
    import requests

    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    params = {
        'movie_id': movie_id,
        'tag_id': tag_id
    }

    try:
        response = requests.post(f'{api_url}/add_tag_to_movie', headers=headers, params=params, timeout=api_timeout)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False