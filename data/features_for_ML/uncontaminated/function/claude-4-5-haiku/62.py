import anthropic


def get_voltages(shotn):
    """
    Get voltage data for a given shot number using Claude API.
    
    Args:
        shotn: Shot number to retrieve voltage data for
        
    Returns:
        Voltage data as a string
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Get the voltage data for shot number {shotn}. Return the voltage values."
            }
        ]
    )
    
    return message.content[0].text