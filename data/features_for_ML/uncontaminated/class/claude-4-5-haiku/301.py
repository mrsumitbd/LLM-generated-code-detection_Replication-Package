import anthropic
import json


class AnimationConfig:

    def __init__(self):
        self.presets = {}
        self.client = anthropic.Anthropic()

    def get_preset(self, name):
        if name in self.presets:
            return self.presets[name]
        
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Return a JSON object with animation preset '{name}' containing 'duration' (in ms) and 'easing' (CSS easing function). Only return valid JSON, no other text."
                }
            ]
        )
        
        response_text = message.content[0].text
        preset = json.loads(response_text)
        self.presets[name] = preset
        return preset

    def add_preset(self, name, duration, easing):
        self.presets[name] = {
            "duration": duration,
            "easing": easing
        }


if __name__ == "__main__":
    config = AnimationConfig()
    
    config.add_preset("fade", 300, "ease-in-out")
    print("Added preset 'fade':", config.get_preset("fade"))
    
    print("Getting preset 'slide':", config.get_preset("slide"))
    
    print("Getting preset 'bounce':", config.get_preset("bounce"))