def get_movies_with_missing(api_url: str, api_key: str, api_timeout: int, monitored_only: bool) -> Optional[List[Dict]]:
    import requests

    headers = {
        'X-Api-Key': api_key
    }

    params = {
        'apikey': api_key,
        'monitored': monitored_only
    }

    try:
        response = requests.get(f'{api_url}/movie', headers=headers, params=params, timeout=api_timeout)
        response.raise_for_status()
        movies = response.json()
        return [movie for movie in movies if movie.get('hasFile') is False]
    except requests.exceptions.RequestException:
        return None