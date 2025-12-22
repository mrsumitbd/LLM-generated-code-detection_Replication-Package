import anthropic


def display_as_textured(ref):
    """
    Display a reference as textured using Claude's vision capabilities.
    
    Args:
        ref: A reference object that can be displayed as textured
        
    Returns:
        The textured display result from Claude
    """
    client = anthropic.Anthropic()
    
    # Convert the reference to a string representation
    ref_str = str(ref)
    
    # Use Claude to process and display the reference as textured
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Display this reference as textured: {ref_str}"
            }
        ]
    )
    
    return message.content[0].text