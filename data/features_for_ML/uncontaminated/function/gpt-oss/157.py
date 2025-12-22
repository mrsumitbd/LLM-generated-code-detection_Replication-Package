from PIL import ImageFont
from typing import List

def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int) -> str:
    """
    Wraps the given text so that each line does not exceed `line_length` pixels
    when rendered with the provided `font`. Returns the wrapped text as a single
    string with newline characters separating the lines.
    """
    # Helper to measure width of a string using the font
    def width_of(s: str) -> int:
        # Use getbbox for more accurate measurement
        bbox = font.getbbox(s)
        return bbox[2] - bbox[0]

    # Split the text into paragraphs (preserve existing newlines)
    paragraphs: List[str] = text.splitlines()

    wrapped_lines: List[str] = []

    for para in paragraphs:
        # If the paragraph is empty, preserve the blank line
        if not para.strip():
            wrapped_lines.append("")
            continue

        words = para.split()
        current_line = ""
        for word in words:
            # If adding the word exceeds the limit, start a new line
            test_line = f"{current_line} {word}".strip() if current_line else word
            if width_of(test_line) <= line_length:
                current_line = test_line
            else:
                # If the current line is empty, the word itself is too long
                if not current_line:
                    # Break the word into smaller chunks
                    chunk = ""
                    for char in word:
                        test_chunk = chunk + char
                        if width_of(test_chunk) <= line_length:
                            chunk = test_chunk
                        else:
                            if chunk:
                                wrapped_lines.append(chunk)
                            chunk = char
                    if chunk:
                        current_line = chunk
                    else:
                        current_line = ""
                else:
                    wrapped_lines.append(current_line)
                    current_line = word
        if current_line:
            wrapped_lines.append(current_line)

    return "\n".join(wrapped_lines)