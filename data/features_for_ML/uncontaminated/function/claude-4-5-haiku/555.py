import anthropic


def call_llm(prompt):
    """
    Call Claude LLM with the given prompt and return the response.
    
    Args:
        prompt: The prompt to send to the LLM
        
    Returns:
        The text response from Claude
    """
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text