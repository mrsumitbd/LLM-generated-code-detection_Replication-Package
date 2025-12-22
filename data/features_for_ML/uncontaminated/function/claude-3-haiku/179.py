from dataclasses import dataclass

@dataclass
class MediaInfo:
    title: str
    description: str
    duration: int
    genres: list[str]

def __series_to_media(series_info: dict) -> MediaInfo:
    title = series_info['title']
    description = series_info['description']
    duration = series_info['duration']
    genres = series_info['genres']

    return MediaInfo(
        title=title,
        description=description,
        duration=duration,
        genres=genres
    )