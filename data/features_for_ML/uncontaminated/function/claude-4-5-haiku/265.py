import anthropic
import json


def _format_json_to_markdown(json_str):
    """
    Converts JSON string to a more readable markdown format.
    
    Args:
        json_str (str): JSON string to format.
    
    Returns:
        str: Formatted markdown string.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Convert the following JSON string to a readable markdown format. 
                
The markdown should:
- Use headers for top-level keys
- Use bullet points or tables for nested structures
- Format arrays as lists
- Make it easy to read and understand

JSON to convert:
{json_str}

Return only the markdown formatted output, no explanations."""
            }
        ]
    )
    
    return message.content[0].text


if __name__ == "__main__":
    # Test with sample JSON
    sample_json = json.dumps({
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "zip": "10001"
        },
        "hobbies": ["reading", "gaming", "cooking"],
        "employment": {
            "company": "Tech Corp",
            "position": "Software Engineer",
            "years": 5
        }
    })
    
    markdown_output = _format_json_to_markdown(sample_json)
    print(markdown_output)