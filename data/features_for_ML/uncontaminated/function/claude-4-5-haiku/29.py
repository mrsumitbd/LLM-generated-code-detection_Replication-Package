import anthropic


def masked_max(*args, **kwargs):
    """
    Find the maximum value among the arguments using Claude as an AI backbone.
    
    Args:
        *args: Variable length argument list of numbers to compare
        **kwargs: Optional keyword arguments (e.g., model specification)
    
    Returns:
        The maximum value among the arguments
    """
    if not args:
        raise ValueError("masked_max expected at least 1 argument, got 0")
    
    # Extract model from kwargs if provided, otherwise use default
    model = kwargs.get('model', 'claude-3-5-sonnet-20241022')
    
    # Create the prompt for Claude
    numbers_str = ", ".join(str(arg) for arg in args)
    prompt = f"Find the maximum value among these numbers: {numbers_str}. Reply with only the maximum number, nothing else."
    
    # Initialize the Anthropic client
    client = anthropic.Anthropic()
    
    # Call Claude API
    message = client.messages.create(
        model=model,
        max_tokens=100,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response
    response_text = message.content[0].text.strip()
    
    # Parse the response to get the maximum value
    try:
        max_value = float(response_text)
        # Try to convert to int if it's a whole number
        if max_value == int(max_value):
            max_value = int(max_value)
        return max_value
    except ValueError:
        # If Claude returns something unexpected, fall back to Python's max
        return max(args)