def __series_to_media(series_info: dict) -> MediaInfo:
    media_info = MediaInfo()
    media_info.title = series_info.get('title', '')
    media_info.year = series_info.get('year', '')
    media_info.genre = series_info.get('genre', '')
    media_info.director = series_info.get('director', '')
    media_info.cast = series_info.get('cast', [])
    media_info.rating = series_info.get('rating', '')
    media_info.duration = series_info.get('duration', '')
    return media_info