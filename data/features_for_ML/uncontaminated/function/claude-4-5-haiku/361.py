import anthropic


def process(s):
    """
    Process a string using Claude API and return the response.
    """
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": s}
        ]
    )
    return message.content[0].text