import os
import requests
from typing import Optional


class VoiceInstance:
    """Manages a single Kokoro TTS voice instance"""

    # Base URL for the Kokoro TTS API (adjust if the real endpoint differs)
    _BASE_URL = "https://api.kokoro.ai/v1/tts"

    def __init__(self, voice_id: str):
        """
        Initialize a VoiceInstance with a specific voice ID.

        Parameters
        ----------
        voice_id : str
            The identifier of the Kokoro TTS voice to use.
        """
        if not isinstance(voice_id, str) or not voice_id.strip():
            raise ValueError("voice_id must be a non-empty string")
        self.voice_id = voice_id.strip()

        # Retrieve the API key from the environment; raise if missing
        self.api_key: str = os.getenv("KOKORO_API_KEY", "").strip()
        if not self.api_key:
            raise RuntimeError(
                "KOKORO_API_KEY environment variable is required for TTS requests"
            )

    def generate_audio(self, text: str, output_path: str) -> bool:
        """
        Generate an audio file from the provided text using the configured voice.

        Parameters
        ----------
        text : str
            The text to synthesize.
        output_path : str
            Path where the resulting audio file will be written.

        Returns
        -------
        bool
            True if the audio was successfully generated and written; False otherwise.
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        if not isinstance(output_path, str) or not output_path.strip():
            raise ValueError("output_path must be a non-empty string")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "voice_id": self.voice_id,
            "text": text,
        }

        try:
            response = requests.post(
                self._BASE_URL,
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            # Log the exception if a logger is available; otherwise ignore
            # Example: logging.error("TTS request failed: %s", exc)
            return False

        # The API is expected to return raw audio bytes in the response body.
        # Some APIs may return a JSON object with a URL or base64 data; adjust accordingly.
        audio_bytes: Optional[bytes] = None
        content_type = response.headers.get("Content-Type", "")

        if "audio" in content_type:
            audio_bytes = response.content
        else:
            # Attempt to parse JSON for a base64-encoded audio field
            try:
                data = response.json()
                import base64

                audio_b64 = data.get("audio_base64") or data.get("audio")
                if audio_b64:
                    audio_bytes = base64.b64decode(audio_b64)
            except Exception:
                pass

        if not audio_bytes:
            return False

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
        except OSError:
            return False

        return True