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
    # Environment variable names used historically
    env_var_names = ("AUDIO_PATH", "AUDIO_DIR")

    audio_path_str = None
    for name in env_var_names:
        audio_path_str = os.getenv(name)
        if audio_path_str:
            break

    if not audio_path_str:
        raise ValueError(
            "Audio path environment variable not set. "
            f"Please set one of {env_var_names}."
        )

    audio_path = Path(audio_path_str).expanduser().resolve()

    if not audio_path.exists() or not audio_path.is_dir():
        raise ValueError(
            f"Audio path '{audio_path}' does not exist or is not a directory."
        )

    return audio_path