import anthropic


def load_section(section_number):
    """
    Load a section of text using Claude API with streaming.
    
    Args:
        section_number: The section number to load
        
    Returns:
        The complete text of the requested section
    """
    client = anthropic.Anthropic()
    
    prompt = f"Please provide section {section_number} of a comprehensive guide on Python programming. Make it detailed and informative."
    
    full_response = ""
    
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            full_response += text
    
    return full_response


if __name__ == "__main__":
    section_text = load_section(1)
    print("Section 1:")
    print(section_text)