import anthropic
import json
import re


class AudioMetadata:
    """Complete metadata for an audio recording."""

    def __init__(self, audio_file_path: str):
        """Initialize AudioMetadata with an audio file path."""
        self.audio_file_path = audio_file_path
        self.client = anthropic.Anthropic()
        self.metadata = None

    def extract_metadata(self) -> dict:
        """Extract metadata from an audio file using Claude's vision capabilities."""
        with open(self.audio_file_path, "rb") as audio_file:
            audio_data = audio_file.read()

        import base64

        audio_base64 = base64.standard_b64encode(audio_data).decode("utf-8")

        file_extension = self.audio_file_path.split(".")[-1].lower()
        media_type_map = {
            "mp3": "audio/mpeg",
            "wav": "audio/wav",
            "m4a": "audio/mp4",
            "flac": "audio/flac",
            "ogg": "audio/ogg",
            "aac": "audio/aac",
        }
        media_type = media_type_map.get(file_extension, "audio/mpeg")

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this audio file and extract comprehensive metadata. 
                            Provide the following information in JSON format:
                            {
                                "title": "song/content title if identifiable",
                                "artist": "artist name if identifiable",
                                "genre": "music genre or content type",
                                "duration_estimate": "estimated duration in seconds",
                                "language": "primary language spoken/sung",
                                "audio_quality": "quality assessment (low/medium/high)",
                                "content_type": "type of audio (music/speech/podcast/ambient/mixed)",
                                "mood": "mood or tone of the audio",
                                "instruments": ["list of identifiable instruments"],
                                "key_features": ["notable characteristics or features"],
                                "production_notes": "any notable production aspects"
                            }
                            
                            If you cannot determine certain fields, use null or best estimate based on audio characteristics.""",
                        },
                        {
                            "type": "audio",
                            "media_type": media_type,
                            "data": audio_base64,
                        },
                    ],
                }
            ],
        )

        response_text = message.content[0].text

        json_match = re.search(r"\{[\s\S]*\}", response_text)
        if json_match:
            json_str = json_match.group()
            self.metadata = json.loads(json_str)
        else:
            self.metadata = {"raw_response": response_text}

        return self.metadata

    def get_metadata(self) -> dict:
        """Get the extracted metadata."""
        if self.metadata is None:
            return self.extract_metadata()
        return self.metadata

    def get_title(self) -> str:
        """Get the title from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("title", "Unknown")

    def get_artist(self) -> str:
        """Get the artist from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("artist", "Unknown")

    def get_genre(self) -> str:
        """Get the genre from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("genre", "Unknown")

    def get_duration(self) -> int:
        """Get the duration estimate from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        duration = self.metadata.get("duration_estimate")
        if isinstance(duration, int):
            return duration
        elif isinstance(duration, str):
            try:
                return int(duration)
            except ValueError:
                return 0
        return 0

    def get_language(self) -> str:
        """Get the language from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("language", "Unknown")

    def get_audio_quality(self) -> str:
        """Get the audio quality from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("audio_quality", "Unknown")

    def get_content_type(self) -> str:
        """Get the content type from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("content_type", "Unknown")

    def get_mood(self) -> str:
        """Get the mood from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("mood", "Unknown")

    def get_instruments(self) -> list:
        """Get the list of instruments from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        instruments = self.metadata.get("instruments", [])
        return instruments if isinstance(instruments, list) else []

    def get_key_features(self) -> list:
        """Get the key features from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        features = self.metadata.get("key_features", [])
        return features if isinstance(features, list) else []

    def get_production_notes(self) -> str:
        """Get the production notes from metadata."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata.get("production_notes", "")

    def to_dict(self) -> dict:
        """Convert metadata to dictionary."""
        if self.metadata is None:
            self.extract_metadata()
        return self.metadata

    def to_json(self) -> str:
        """Convert metadata to JSON string."""
        if self.metadata is None:
            self.extract_metadata()
        return json.dumps(self.metadata, indent=2)