from PIL import ImageFont

def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
    lines = []
    words = text.split()
    current_line = words[0]

    for word in words[1:]:
        test_line = current_line + " " + word
        width, _ = font.getsize(test_line)
        if width <= line_length:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return "\n".join(lines)