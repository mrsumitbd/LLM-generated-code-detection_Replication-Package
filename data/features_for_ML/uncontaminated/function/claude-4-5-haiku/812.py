import anthropic


def system_prompt(natural=False, sab=False, **kwargs):
    """
    Generate a system prompt for Claude based on the given parameters.
    
    Args:
        natural: If True, use natural language style
        sab: If True, use SAB (Synthetic Ability Benchmark) style
        **kwargs: Additional parameters to pass to the API
    
    Returns:
        The system prompt string
    """
    client = anthropic.Anthropic()
    
    # Build the prompt based on parameters
    prompt_parts = []
    
    if natural:
        prompt_parts.append("Use natural, conversational language.")
    
    if sab:
        prompt_parts.append("Follow SAB (Synthetic Ability Benchmark) guidelines.")
    
    # Add any additional instructions from kwargs
    for key, value in kwargs.items():
        if isinstance(value, str):
            prompt_parts.append(f"{key}: {value}")
    
    # Create a message to get the system prompt
    user_message = "Generate a system prompt" + (" with the following characteristics: " + " ".join(prompt_parts) if prompt_parts else ".")
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    
    return message.content[0].text