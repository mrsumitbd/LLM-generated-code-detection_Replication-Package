import anthropic
import json


def extract_required(schema, prefix=""):
    """
    Extracts required fields from a JSON schema recursively.
    
    Args:
        schema: A JSON schema dictionary
        prefix: A prefix to add to field names (for nested fields)
    
    Returns:
        A list of required field paths
    """
    required_fields = []
    
    if not isinstance(schema, dict):
        return required_fields
    
    # Get the required fields at this level
    required = schema.get("required", [])
    
    # Get the properties
    properties = schema.get("properties", {})
    
    # Add required fields with prefix
    for field in required:
        if prefix:
            required_fields.append(f"{prefix}.{field}")
        else:
            required_fields.append(field)
    
    # Recursively process nested objects
    for prop_name, prop_schema in properties.items():
        if isinstance(prop_schema, dict):
            # Check if this property is an object with nested properties
            if prop_schema.get("type") == "object" and "properties" in prop_schema:
                new_prefix = f"{prefix}.{prop_name}" if prefix else prop_name
                nested_required = extract_required(prop_schema, new_prefix)
                required_fields.extend(nested_required)
            # Handle arrays of objects
            elif prop_schema.get("type") == "array":
                items = prop_schema.get("items", {})
                if isinstance(items, dict) and items.get("type") == "object" and "properties" in items:
                    new_prefix = f"{prefix}.{prop_name}" if prefix else prop_name
                    nested_required = extract_required(items, new_prefix)
                    required_fields.extend(nested_required)
    
    return required_fields


def main():
    # Example usage with Claude API
    client = anthropic.Anthropic()
    
    # Define a complex schema with nested objects
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string"},
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "country": {"type": "string"}
                },
                "required": ["street", "city"]
            },
            "phone_numbers": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "number": {"type": "string"}
                    },
                    "required": ["type", "number"]
                }
            }
        },
        "required": ["name", "email", "address"]
    }
    
    # Extract required fields
    required_fields = extract_required(schema)
    print("Required fields:", required_fields)
    
    # Use Claude to validate the schema
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Given this JSON schema:
{json.dumps(schema, indent=2)}

And these extracted required fields:
{json.dumps(required_fields, indent=2)}

Please verify if the extraction is correct and explain what required fields should be present in any valid JSON object conforming to this schema."""
            }
        ]
    )
    
    print("\nClaude's verification:")
    print(message.content[0].text)


if __name__ == "__main__":
    main()