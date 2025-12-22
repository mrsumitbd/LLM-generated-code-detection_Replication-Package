import anthropic


def generate_dynamic_class_name(base_name: str) -> str:
    """
    Generate a dynamic class name based on a base name using Claude API.
    
    Args:
        base_name: The base name to generate a class name from
        
    Returns:
        A generated class name as a string
    """
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Generate a single Python class name based on the base name '{base_name}'. The class name should follow Python naming conventions (PascalCase). Return only the class name, nothing else."
            }
        ]
    )
    
    class_name = message.content[0].text.strip()
    return class_name


if __name__ == "__main__":
    test_names = ["user", "data_processor", "api_client"]
    
    for base_name in test_names:
        generated_name = generate_dynamic_class_name(base_name)
        print(f"Base name: {base_name} -> Generated class name: {generated_name}")