import anthropic
import json
import re


def generate_uuid(ua_type: str):
    """
    Generate a UUID using Claude API with tool use.
    
    Args:
        ua_type: The type of UUID to generate (e.g., "v4", "v5", etc.)
    
    Returns:
        A generated UUID string
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "generate_uuid_tool",
            "description": "Generate a UUID of the specified type",
            "input_schema": {
                "type": "object",
                "properties": {
                    "uuid_type": {
                        "type": "string",
                        "description": "The type of UUID to generate (v1, v4, v5, etc.)"
                    }
                },
                "required": ["uuid_type"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": f"Please generate a UUID of type {ua_type} for me."
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    if response.stop_reason == "tool_use":
        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_name = content_block.name
                tool_input = content_block.input
                
                if tool_name == "generate_uuid_tool":
                    uuid_type = tool_input.get("uuid_type", ua_type)
                    
                    import uuid
                    if uuid_type.lower() == "v4":
                        generated_uuid = str(uuid.uuid4())
                    elif uuid_type.lower() == "v1":
                        generated_uuid = str(uuid.uuid1())
                    else:
                        generated_uuid = str(uuid.uuid4())
                    
                    return generated_uuid
    
    import uuid
    return str(uuid.uuid4())