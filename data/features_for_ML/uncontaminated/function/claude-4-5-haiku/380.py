import anthropic


def rounded_corners(corner_string):
    """
    Takes a string describing corner values and returns a string with rounded corners.
    Uses Claude to process the corner string and return the result.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Process this corner string and return the result with rounded corners: {corner_string}"
            }
        ]
    )
    
    return message.content[0].text