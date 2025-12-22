import anthropic


def _extract_param_type(docstring, param_name):
    """
    Extracts the parameter type from the function's docstring.
    """
    if not docstring or not param_name:
        return None
    
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Extract the type of the parameter '{param_name}' from the following docstring.
Return only the type (e.g., 'str', 'int', 'list', 'dict', etc.) or 'None' if the type cannot be determined.
Do not include any explanation, just the type.

Docstring:
{docstring}"""
            }
        ]
    )
    
    response_text = message.content[0].text.strip()
    
    if response_text.lower() == 'none':
        return None
    
    return response_text