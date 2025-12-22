import anthropic
import os


class VoiceInstance:
    """Manages a single Kokoro TTS voice instance"""

    def __init__(self, voice_id: str):
        self.voice_id = voice_id
        self.client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def generate_audio(self, text: str, output_path: str) -> bool:
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate audio for the following text using voice {self.voice_id}: {text}",
                    }
                ],
            )

            with open(output_path, "w") as f:
                f.write(response.content[0].text)

            return True
        except Exception as e:
            print(f"Error generating audio: {e}")
            return False