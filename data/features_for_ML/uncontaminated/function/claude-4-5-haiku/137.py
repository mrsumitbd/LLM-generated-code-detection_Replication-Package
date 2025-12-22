import anthropic
import base64
from typing import Annotated


def avatar_tool(
    description: Annotated[str, "Description of the AI avatar, including features, style, and personality."],
):
    """Generates an avatar/image for an AI agent. Creates a suitable AI image based on the provided description."""
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate a detailed image prompt for creating an AI avatar based on this description: {description}\n\nProvide only the image prompt, no additional text."
                    }
                ]
            }
        ]
    )
    
    image_prompt = message.content[0].text
    
    image_message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Create an image based on this prompt: {image_prompt}"
                    }
                ]
            }
        ]
    )
    
    result = {
        "description": description,
        "image_prompt": image_prompt,
        "status": "Avatar generation requested",
        "model_used": "claude-3-5-sonnet-20241022",
        "message": "Image generation would require integration with an image generation API like DALL-E, Midjourney, or Stable Diffusion. The prompt has been generated and is ready to be sent to an image generation service."
    }
    
    return result