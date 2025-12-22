import os
import subprocess
from typing import Tuple

class VoiceInstance:
    """Manages a single Kokoro TTS voice instance"""

    def __init__(self, voice_id: str):
        self.voice_id = voice_id
        self.tts_engine_path = os.path.join(os.path.dirname(__file__), "kokoro_tts_engine")

    def generate_audio(self, text: str, output_path: str) -> bool:
        try:
            subprocess.run(
                [self.tts_engine_path, self.voice_id, text, output_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error generating audio: {e}")
            return False