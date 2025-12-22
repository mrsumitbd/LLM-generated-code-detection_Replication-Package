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
    import os
    from pathlib import Path
    
    audio_path_env = os.getenv('AUDIO_PATH')
    
    if audio_path_env is None:
        raise ValueError("Audio path environment variable 'AUDIO_PATH' is not set.")
    
    audio_path = Path(audio_path_env)
    
    if not audio_path.exists():
        raise ValueError(f"Audio path does not exist: {audio_path}")
    
    return audio_path