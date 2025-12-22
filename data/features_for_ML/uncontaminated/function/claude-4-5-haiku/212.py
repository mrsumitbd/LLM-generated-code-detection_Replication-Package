import anthropic


def quaternion_to_axis_angle(*args, **kwargs):
    """
    Convert a quaternion to axis-angle representation using Claude API.
    
    Args:
        *args: Positional arguments (quaternion components or array)
        **kwargs: Keyword arguments (may include 'model', 'api_key', etc.)
    
    Returns:
        dict: Contains 'axis' (3D unit vector) and 'angle' (in radians)
    """
    client = anthropic.Anthropic()
    
    # Format the input for Claude
    input_str = f"args: {args}, kwargs: {kwargs}"
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Convert the following quaternion to axis-angle representation.

Input: {input_str}

Please:
1. Parse the quaternion from the input (it could be in various formats like [w,x,y,z], [x,y,z,w], or separate arguments)
2. Convert it to axis-angle representation
3. Return the result as a Python dictionary with 'axis' (a 3D unit vector as a list) and 'angle' (in radians as a float)
4. Only return the Python dictionary, no other text

The conversion formula:
- angle = 2 * arccos(w) where w is the scalar part
- axis = [x, y, z] / sin(angle/2) where [x,y,z] is the vector part (normalized)
- Handle the special case where sin(angle/2) ≈ 0"""
            }
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text.strip()
    
    # Extract dictionary from response
    import ast
    result = ast.literal_eval(response_text)
    
    return result