import anthropic
import json


def load_validator(resource_type_name: str, resource_schema: dict):
    """
    Load a validator for a given resource type using Claude.
    
    Args:
        resource_type_name: The name of the resource type (e.g., "User", "Product")
        resource_schema: A dictionary describing the schema of the resource
    
    Returns:
        A validator function that can validate instances of the resource
    """
    client = anthropic.Anthropic()
    
    schema_str = json.dumps(resource_schema, indent=2)
    
    prompt = f"""You are a JSON schema validator. I need you to create a validation function for the following resource type.

Resource Type: {resource_type_name}
Schema:
{schema_str}

Please analyze this schema and provide validation logic. When I give you a JSON object to validate, check if it conforms to this schema and return a JSON response with:
- "valid": true/false
- "errors": list of validation errors (empty if valid)

Be strict about type checking, required fields, and any constraints implied by the schema."""

    def validator(data: dict) -> dict:
        """Validate data against the resource schema using Claude."""
        validation_prompt = f"""Validate the following JSON object against the {resource_type_name} schema:

Object to validate:
{json.dumps(data, indent=2)}

Return a JSON response with:
- "valid": true/false
- "errors": list of validation errors (empty if valid)"""
        
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=prompt,
            messages=[
                {"role": "user", "content": validation_prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        try:
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
            else:
                result = {"valid": False, "errors": ["Could not parse validation response"]}
        except json.JSONDecodeError:
            result = {"valid": False, "errors": ["Invalid JSON in response"]}
        
        return result
    
    return validator