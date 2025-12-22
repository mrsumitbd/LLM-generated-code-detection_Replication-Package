import os
from pathlib import Path

def check_and_get_audio_path() -> Path:
    audio_path = os.getenv('AUDIO_PATH')
    if not audio_path:
        raise ValueError("Audio path environment variable is not set.")
    
    audio_path = Path(audio_path)
    if not audio_path.exists():
        raise ValueError("Audio path does not exist.")
    
    return audio_path