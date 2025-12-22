import inspect
from typing import Any, Dict

# Assume MediaInfo is defined elsewhere in the project.
# Import it here; if it is not available, this function will raise an ImportError.
try:
    from media_library.models import MediaInfo  # Adjust the import path as needed
except Exception:
    # Fallback: define a minimal MediaInfo for type checking purposes
    class MediaInfo:
        def __init__(self, **kwargs: Any):
            for k, v in kwargs.items():
                setattr(self, k, v)

def __series_to_media(series_info: Dict[str, Any]) -> MediaInfo:
    """
    Convert a dictionary containing series information into a MediaInfo instance.

    The function attempts to map keys from the input dictionary to the constructor
    parameters of MediaInfo. Keys that do not match constructor parameters are
    ignored. If the media type is not specified, it defaults to 'series'.

    Parameters
    ----------
    series_info : dict
        Dictionary containing series metadata. Expected keys include, but are not
        limited to: 'title', 'year', 'season', 'episode', 'id', 'url',
        'description', 'poster', and 'media_type'.

    Returns
    -------
    MediaInfo
        An instance of MediaInfo populated with the provided data.
    """
    # Determine the constructor signature of MediaInfo
    try:
        sig = inspect.signature(MediaInfo)
    except (ValueError, TypeError):
        # If MediaInfo is not a proper callable, fall back to passing all kwargs
        return MediaInfo(**series_info)

    # Filter series_info keys that match constructor parameters
    filtered: Dict[str, Any] = {
        k: v for k, v in series_info.items() if k in sig.parameters
    }

    # Ensure season and episode are integers if present
    for key in ("season", "episode"):
        if key in filtered:
            try:
                filtered[key] = int(filtered[key])
            except (TypeError, ValueError):
                # Leave as is if conversion fails
                pass

    # Default media_type to 'series' if not provided
    if "media_type" not in filtered:
        filtered["media_type"] = "series"

    return MediaInfo(**filtered)