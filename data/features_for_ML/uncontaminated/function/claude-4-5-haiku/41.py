import anthropic


def generate_path(duration, mask):
    """
    Generate a path using Claude API based on duration and mask parameters.
    
    Args:
        duration: The duration parameter for path generation
        mask: The mask parameter for path generation
    
    Returns:
        The generated path as a string
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Generate a path with duration={duration} and mask={mask}. Provide only the path without explanation."
            }
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Test the function
    result = generate_path(duration=10, mask="test_mask")
    print(result)