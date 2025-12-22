import anthropic


def convert_to_bytes(value, bytes, mock=False):
    """
    Convert a value to bytes using Claude API.
    
    Args:
        value: The value to convert
        bytes: The target byte size
        mock: If True, return a mock response without calling the API
    
    Returns:
        The converted value as bytes
    """
    if mock:
        # Return a mock response for testing
        return f"Mock conversion of {value} to {bytes} bytes"
    
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Convert the value '{value}' to {bytes} bytes. Return only the converted value."
            }
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Test with mock=True to avoid API calls
    result = convert_to_bytes("hello", 10, mock=True)
    print(f"Mock result: {result}")
    
    # Uncomment to test with actual API
    # result = convert_to_bytes("hello", 10, mock=False)
    # print(f"API result: {result}")