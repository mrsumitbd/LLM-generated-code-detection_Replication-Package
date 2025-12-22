import anthropic


def get_route_handler() -> dict[str, str]:
    """
    Returns a dictionary mapping route paths to their handler descriptions.
    Uses Claude to generate route handlers for a simple web application.
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Generate a JSON dictionary with 3 simple web application routes as keys (like '/home', '/about', '/contact') and their handler descriptions as values. Return only valid JSON, no other text."
            }
        ]
    )
    
    response_text = message.content[0].text
    
    import json
    routes = json.loads(response_text)
    
    return routes


if __name__ == "__main__":
    routes = get_route_handler()
    print("Generated Routes:")
    for route, handler in routes.items():
        print(f"  {route}: {handler}")