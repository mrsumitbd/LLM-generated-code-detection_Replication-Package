import anthropic


def is_valid_numpy_dtype_string(dtype_str: str) -> bool:
    """
    Return True if a given string can be converted to a numpy dtype.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Determine if the following string is a valid numpy dtype string. 
A valid numpy dtype string is one that can be used with numpy.dtype() without raising an error.

Examples of valid dtype strings:
- 'int32'
- 'float64'
- 'bool'
- 'complex128'
- 'U10' (unicode string of length 10)
- 'S5' (byte string of length 5)
- 'datetime64'
- 'timedelta64'
- 'object'
- 'void'

Examples of invalid dtype strings:
- 'invalid_type'
- 'int33'
- 'float'
- 'my_custom_type'
- ''
- 'int32x'

The string to check is: '{dtype_str}'

Respond with only 'True' if it's a valid numpy dtype string, or 'False' if it's not. No other text."""
            }
        ]
    )
    
    response_text = message.content[0].text.strip()
    return response_text.lower() == 'true'