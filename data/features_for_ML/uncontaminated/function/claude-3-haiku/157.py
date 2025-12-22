from typing import List

def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int) -> List[str]:
    """
    Wraps the given text to fit within the specified line length using the provided font.

    Args:
        text (str): The input text to be wrapped.
        font (ImageFont.ImageFont): The font to be used for text measurement.
        line_length (int): The maximum length of each line in pixels.

    Returns:
        List[str]: A list of strings, where each string represents a line of the wrapped text.
    """
    lines = []
    current_line = ""
    words = text.split()

    for word in words:
        if font.getsize(current_line + word)[0] <= line_length:
            current_line += f"{word} "
        else:
            lines.append(current_line.strip())
            current_line = f"{word} "

    if current_line:
        lines.append(current_line.strip())

    return lines