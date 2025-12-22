import anthropic


def extract_categories_from_openapi(openapi_spec: dict) -> dict[str, list[dict]]:
    """Extract categories and their routes from OpenAPI spec.

    Args:
        openapi_spec: OpenAPI specification dictionary

    Returns:
        Dictionary mapping category names to lists of route info
    """
    client = anthropic.Anthropic()
    
    # Convert the OpenAPI spec to a string for the prompt
    spec_str = str(openapi_spec)
    
    # Create a prompt for Claude to extract categories and routes
    prompt = f"""Analyze the following OpenAPI specification and extract categories (tags) and their associated routes.

OpenAPI Spec:
{spec_str}

Please extract the information in the following format:
For each category/tag, list all the routes that belong to it with their:
- path
- method (GET, POST, PUT, DELETE, etc.)
- summary or description
- operationId (if available)

Return the result as a Python dictionary where:
- Keys are category names (strings)
- Values are lists of dictionaries, where each dictionary contains:
  - 'path': the route path
  - 'method': the HTTP method
  - 'summary': the operation summary
  - 'operationId': the operation ID (if available)

Only return the Python dictionary, no other text."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the response text
    response_text = message.content[0].text
    
    # Parse the response as a Python dictionary
    # Remove any markdown code blocks if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("python"):
            response_text = response_text[6:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]
    
    response_text = response_text.strip()
    
    # Evaluate the response as Python code
    result = eval(response_text)
    
    return result