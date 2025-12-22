import anthropic


def masked_min(*args, **kwargs):
    """
    Find the minimum value among the arguments using Claude API with prompt caching.
    
    Args:
        *args: Variable number of numeric arguments
        **kwargs: Optional keyword arguments (currently unused)
    
    Returns:
        The minimum value among the arguments
    """
    if not args:
        raise ValueError("masked_min expected at least 1 argument, got 0")
    
    # Convert all arguments to numbers
    numbers = []
    for arg in args:
        try:
            numbers.append(float(arg))
        except (TypeError, ValueError):
            raise TypeError(f"Cannot convert {arg} to a number")
    
    # Create the prompt for Claude
    numbers_str = ", ".join(str(n) for n in numbers)
    
    client = anthropic.Anthropic()
    
    # Use prompt caching to efficiently find the minimum
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        system=[
            {
                "type": "text",
                "text": "You are a helpful assistant that finds the minimum value from a list of numbers. Always respond with just the minimum number, nothing else.",
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Find the minimum value among these numbers: {numbers_str}"
            }
        ]
    )
    
    # Extract the minimum value from the response
    result_text = response.content[0].text.strip()
    
    try:
        min_value = float(result_text)
        return min_value
    except ValueError:
        # Fallback to Python's built-in min if Claude's response is unexpected
        return min(numbers)