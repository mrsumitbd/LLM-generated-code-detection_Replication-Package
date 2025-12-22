def transpose(tensor):
    """
    Transpose a tensor by reversing the order of its dimensions.
    
    Args:
        tensor: A nested list representing a tensor of any rank
        
    Returns:
        A new tensor with dimensions reversed
    """
    import anthropic
    
    client = anthropic.Anthropic()
    
    # Convert tensor to string representation for Claude
    tensor_str = str(tensor)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Given a tensor represented as a nested list: {tensor_str}

Please transpose this tensor by reversing the order of its dimensions. 

For example:
- A 1D tensor [1, 2, 3] remains [1, 2, 3]
- A 2D tensor [[1, 2], [3, 4]] becomes [[1, 3], [2, 4]]
- A 3D tensor [[[1, 2], [3, 4]], [[5, 6], [7, 8]]] becomes [[[1, 5], [3, 7]], [[2, 6], [4, 8]]]

Return ONLY the transposed tensor as a Python nested list, with no additional text or explanation."""
            }
        ]
    )
    
    # Parse the response
    response_text = message.content[0].text.strip()
    
    # Evaluate the response as a Python literal
    transposed = eval(response_text)
    
    return transposed