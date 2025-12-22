from PIL import ImageFont, ImageDraw, Image

def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    """
    Wraps text to fit within a specified line length using the given font.
    
    Args:
        text: The text to wrap
        font: PIL ImageFont object
        line_length: Maximum width in pixels for each line
    
    Returns:
        A string with newlines inserted to wrap the text
    """
    lines = []
    current_line = ""
    
    for word in text.split():
        test_line = current_line + (" " if current_line else "") + word
        
        # Create a temporary image to measure text width
        temp_img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(temp_img)
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= line_length:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return "\n".join(lines)