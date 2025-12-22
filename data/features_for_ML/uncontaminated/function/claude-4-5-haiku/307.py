import anthropic
import re


def validate_regex(value: str | None) -> str | None:
    """
    Validates if a string is a valid regex pattern using Claude API.
    
    Args:
        value: A string that may or may not be a valid regex pattern, or None
        
    Returns:
        The input string if it's a valid regex pattern, None otherwise
    """
    if value is None:
        return None
    
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Determine if the following string is a valid regular expression pattern. 
                
String to validate: {value}

Respond with only "VALID" if it's a valid regex pattern, or "INVALID" if it's not. Do not include any other text."""
            }
        ]
    )
    
    response_text = message.content[0].text.strip().upper()
    
    if response_text == "VALID":
        try:
            re.compile(value)
            return value
        except re.error:
            return None
    else:
        return None