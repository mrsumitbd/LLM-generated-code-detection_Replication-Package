import anthropic


def api_docs_put(item: str) -> dict:
    """
    Uses Claude to generate API documentation for a PUT endpoint.
    
    Args:
        item: The resource name for which to generate PUT documentation
        
    Returns:
        A dictionary containing the API documentation
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Generate API documentation for a PUT endpoint for the '{item}' resource. Include the endpoint path, request body schema, response schema, and example usage. Format the response as a JSON object."
            }
        ]
    )
    
    response_text = message.content[0].text
    
    import json
    try:
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        pass
    
    return {
        "endpoint": f"PUT /api/{item.lower()}",
        "description": response_text,
        "status": "success"
    }


if __name__ == "__main__":
    result = api_docs_put("user")
    print(result)