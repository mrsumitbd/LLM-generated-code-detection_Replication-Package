import anthropic
import json


def config_content(config):
    """
    Generate configuration content using Claude API with streaming.
    
    Args:
        config: A dictionary containing configuration parameters
        
    Returns:
        A string containing the generated configuration content
    """
    client = anthropic.Anthropic()
    
    # Convert config to a formatted string for the prompt
    config_str = json.dumps(config, indent=2)
    
    prompt = f"""Based on the following configuration parameters, generate appropriate configuration content:

{config_str}

Please generate a detailed configuration file or content that matches these parameters."""
    
    # Use streaming to collect the response
    full_response = ""
    
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    ) as stream:
        for text in stream.text_stream:
            full_response += text
    
    return full_response


if __name__ == "__main__":
    # Example usage
    sample_config = {
        "app_name": "MyApp",
        "version": "1.0.0",
        "debug": True,
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp_db"
        },
        "features": ["authentication", "logging", "caching"]
    }
    
    result = config_content(sample_config)
    print(result)