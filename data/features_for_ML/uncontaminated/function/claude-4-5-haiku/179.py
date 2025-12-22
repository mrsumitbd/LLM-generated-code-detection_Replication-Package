def __series_to_media(series_info: dict) -> MediaInfo:
    return MediaInfo(
        title=series_info.get('name', ''),
        year=series_info.get('year'),
        media_type='series',
        imdb_id=series_info.get('imdb_id'),
        tmdb_id=series_info.get('tmdb_id'),
        description=series_info.get('description', ''),
        poster_url=series_info.get('poster_url'),
        rating=series_info.get('rating'),
        genres=series_info.get('genres', []),
        cast=series_info.get('cast', []),
        seasons=series_info.get('seasons'),
        episodes=series_info.get('episodes'),
        status=series_info.get('status', ''),
        network=series_info.get('network', '')
    )