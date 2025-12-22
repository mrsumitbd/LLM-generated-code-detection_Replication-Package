import anthropic


def get_str_len(text, fontSizeSet):
    """
    Get the length of a string when rendered with a specific font size.
    Uses Claude to estimate the visual length of text.
    
    Args:
        text: The text string to measure
        fontSizeSet: The font size to use for measurement
    
    Returns:
        The estimated visual length of the text
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Calculate the visual length in pixels of the text '{text}' when rendered with font size {fontSizeSet}pt. Assume a standard monospace font. Return only a single number representing the pixel width."
            }
        ]
    )
    
    response_text = message.content[0].text.strip()
    try:
        length = float(response_text.split()[0])
    except (ValueError, IndexError):
        length = len(text) * fontSizeSet * 0.6
    
    return length