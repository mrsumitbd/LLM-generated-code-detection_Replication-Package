import anthropic
import json


def make_2d_mask(mask):
    """
    Convert a 1D mask to a 2D mask using Claude API.
    
    Args:
        mask: A 1D list/array of boolean or binary values
        
    Returns:
        A 2D list representing the mask in a 2D grid format
    """
    client = anthropic.Anthropic()
    
    # Convert mask to string representation if needed
    mask_str = str(mask)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Convert this 1D mask into a 2D mask (2D grid representation).
The input mask is: {mask_str}

Please return ONLY a valid JSON array representing a 2D grid where:
- The total number of elements equals the length of the input mask
- The grid should be as square as possible (or close to square)
- Each element should maintain its value from the input mask

Return ONLY the JSON array, no other text."""
            }
        ]
    )
    
    # Extract the response text
    response_text = message.content[0].text.strip()
    
    # Parse the JSON response
    result = json.loads(response_text)
    
    return result


if __name__ == "__main__":
    # Test with a simple 1D mask
    test_mask = [1, 0, 1, 0, 1, 0, 1, 0, 1]
    result = make_2d_mask(test_mask)
    print("Input mask:", test_mask)
    print("2D mask:")
    for row in result:
        print(row)