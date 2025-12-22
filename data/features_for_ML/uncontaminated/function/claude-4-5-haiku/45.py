import anthropic


def k_body(k, val):
    """
    Generate a k-body problem description using Claude API.
    
    Args:
        k: Number of bodies in the problem
        val: A value parameter for the problem
    
    Returns:
        A string describing the k-body problem
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Describe a {k}-body problem in physics with parameter value {val}. Keep it concise."
            }
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    result = k_body(3, 1.5)
    print(result)