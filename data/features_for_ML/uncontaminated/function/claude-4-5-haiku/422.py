import anthropic


def log(msg: str, return_line=False, pre_return_line=False, *args, **kwargs):
    """
    Log a message using Claude API with streaming support.
    
    Args:
        msg: The message to log/process
        return_line: Whether to add a newline after the message
        pre_return_line: Whether to add a newline before the message
        *args: Additional positional arguments
        **kwargs: Additional keyword arguments (can include 'model', 'max_tokens', etc.)
    """
    client = anthropic.Anthropic()
    
    if pre_return_line:
        print()
    
    print(msg, end="")
    
    if return_line:
        print()
    
    # Process through Claude if there are additional arguments or kwargs
    if args or kwargs:
        # Build a prompt from the message and additional arguments
        prompt_parts = [msg]
        
        # Add positional arguments to the prompt
        for arg in args:
            prompt_parts.append(str(arg))
        
        # Add keyword arguments to the prompt
        for key, value in kwargs.items():
            if key not in ['model', 'max_tokens', 'temperature']:
                prompt_parts.append(f"{key}: {value}")
        
        full_prompt = " ".join(prompt_parts)
        
        # Extract model and other parameters from kwargs
        model = kwargs.get('model', 'claude-3-5-sonnet-20241022')
        max_tokens = kwargs.get('max_tokens', 1024)
        temperature = kwargs.get('temperature', 1.0)
        
        # Use streaming to process the message
        with client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
        
        if return_line:
            print()