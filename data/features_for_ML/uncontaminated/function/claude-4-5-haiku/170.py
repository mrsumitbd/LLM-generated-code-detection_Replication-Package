import anthropic
import json


def serialize_config(config):
    """
    Serialize a configuration object using Claude AI to generate a JSON representation.
    
    Args:
        config: A configuration object (dict, list, or other serializable type)
    
    Returns:
        A JSON string representation of the configuration
    """
    client = anthropic.Anthropic()
    
    # Convert config to string representation for Claude to analyze
    config_str = str(config)
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Convert the following configuration object into a valid JSON string. 
Return ONLY the JSON string, no other text or explanation.

Configuration object:
{config_str}

Return the JSON representation:"""
            }
        ]
    )
    
    # Extract the JSON string from Claude's response
    json_str = message.content[0].text.strip()
    
    # Validate that it's valid JSON
    try:
        json.loads(json_str)
    except json.JSONDecodeError:
        # If Claude's output isn't valid JSON, try to parse the original config
        json_str = json.dumps(config)
    
    return json_str


if __name__ == "__main__":
    # Test the function
    test_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "mydb"
        },
        "api": {
            "timeout": 30,
            "retries": 3
        },
        "features": ["auth", "logging", "caching"]
    }
    
    result = serialize_config(test_config)
    print("Serialized config:")
    print(result)
    
    # Verify it's valid JSON
    parsed = json.loads(result)
    print("\nParsed back:")
    print(json.dumps(parsed, indent=2))