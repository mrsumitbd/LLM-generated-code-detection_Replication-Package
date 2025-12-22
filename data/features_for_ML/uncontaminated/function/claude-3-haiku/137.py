import openai
import os

def avatar_tool(
    description: Annotated[str, "Description of the AI avatar, including features, style, and personality."],
):
    """Generates an avatar/image for an AI agent. Creates a suitable AI image based on the provided description."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.Image.create(
        prompt=description,
        n=1,
        size="256x256",
        response_format="url",
    )

    image_url = response["data"][0]["url"]
    return image_url