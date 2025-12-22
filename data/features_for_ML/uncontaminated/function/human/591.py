import os
from pathlib import Path

def check_and_get_audio_path() -> Path:
    """Check if the audio path environment variable is set and exists.

    This function maintains backward compatibility with the original implementation.

    Returns
    -------
        Path: The validated audio files path.

    Raises
    ------
        ValueError: If the audio path is not set or doesn't exist.

    """
    audio_path_str = os.getenv("AUDIO_FILES_PATH")
    if not audio_path_str:
        raise ValueError("AUDIO_FILES_PATH environment variable not set")

    audio_path = Path(audio_path_str).resolve()
    if not audio_path.exists():
        raise ValueError(f"Audio path does not exist: {audio_path}")
    return audio_path