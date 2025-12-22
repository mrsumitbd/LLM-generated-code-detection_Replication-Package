import anthropic
import os


def http_get(url, path):
    """
    Downloads a URL to a given path on disc
    """
    client = anthropic.Anthropic()
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=[
            {
                "name": "http_get",
                "description": "Downloads a URL to a given path on disc",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to download from"
                        },
                        "path": {
                            "type": "string",
                            "description": "The file path where the content should be saved"
                        }
                    },
                    "required": ["url", "path"]
                }
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Please download the content from {url} and save it to {path}"
            }
        ]
    )
    
    # Process tool use if the model decides to use it
    for content_block in response.content:
        if content_block.type == "tool_use":
            if content_block.name == "http_get":
                # Extract the tool input
                tool_input = content_block.input
                download_url = tool_input.get("url")
                download_path = tool_input.get("path")
                
                # Perform the actual download
                import urllib.request
                os.makedirs(os.path.dirname(download_path), exist_ok=True)
                urllib.request.urlretrieve(download_url, download_path)
                
                return download_path
    
    # Fallback: perform direct download if tool wasn't used
    import urllib.request
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
    urllib.request.urlretrieve(url, path)
    return path