from typing import Annotated
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io

def avatar_tool(
    description: Annotated[str, "Description of the AI avatar, including features, style, and personality."],
):
    """Generates an avatar/image for an AI agent. Creates a suitable AI image based on the provided description."""
    # Basic image parameters
    size = (256, 256)
    bg_color = (240, 240, 240)
    text_color = (0, 0, 0)

    # Create a blank image
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    # Try to load a truetype font; fall back to default if unavailable
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()

    # Wrap the description to fit within the image width
    max_width = size[0] - 20
    lines = []
    for paragraph in description.splitlines():
        wrapped = textwrap.wrap(paragraph, width=40)
        lines.extend(wrapped if wrapped else [""])

    # Calculate total text height
    line_height = font.getsize("Ay")[1] + 4
    total_height = line_height * len(lines)

    # Start drawing from vertical center
    y = (size[1] - total_height) // 2

    for line in lines:
        w, h = draw.textsize(line, font=font)
        x = (size[0] - w) // 2
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height

    # Return the image object
    return img