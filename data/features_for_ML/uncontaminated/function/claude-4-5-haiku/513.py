def run(*args, **kwargs):
    import anthropic
    
    client = anthropic.Anthropic()
    
    # Extract parameters from kwargs
    model = kwargs.get('model', 'claude-3-5-sonnet-20241022')
    max_tokens = kwargs.get('max_tokens', 1024)
    system_prompt = kwargs.get('system', '')
    
    # Build messages from args
    messages = []
    
    # If args are provided, treat them as user messages
    if args:
        for arg in args:
            if isinstance(arg, dict):
                messages.append(arg)
            else:
                messages.append({"role": "user", "content": str(arg)})
    
    # If messages are provided in kwargs, use those instead
    if 'messages' in kwargs:
        messages = kwargs['messages']
    
    # If no messages provided, return empty response
    if not messages:
        return ""
    
    # Build the request
    request_kwargs = {
        'model': model,
        'max_tokens': max_tokens,
        'messages': messages,
    }
    
    if system_prompt:
        request_kwargs['system'] = system_prompt
    
    # Make the API call
    message = client.messages.create(**request_kwargs)
    
    # Extract and return the response text
    if message.content and len(message.content) > 0:
        return message.content[0].text
    
    return ""