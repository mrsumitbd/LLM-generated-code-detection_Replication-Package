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
    audio_path = os.getenv("AUDIO_PATH")
    if not audio_path:
        raise ValueError("AUDIO_PATH environment variable is not set.")

    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise ValueError(f"AUDIO_PATH '{audio_path}' does not exist.")

    return audio_path