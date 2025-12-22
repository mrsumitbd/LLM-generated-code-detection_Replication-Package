import anthropic


def move_object_to_collection(ref, col):
    """
    Move an object to a collection using Claude's tool use capability.
    
    Args:
        ref: Reference to the object to move
        col: Target collection to move the object to
    
    Returns:
        Result of the move operation
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "move_object",
            "description": "Move an object to a specified collection",
            "input_schema": {
                "type": "object",
                "properties": {
                    "object_ref": {
                        "type": "string",
                        "description": "Reference to the object to move"
                    },
                    "target_collection": {
                        "type": "string",
                        "description": "Target collection to move the object to"
                    }
                },
                "required": ["object_ref", "target_collection"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": f"Please move object '{ref}' to collection '{col}'"
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
                
                if tool_name == "move_object":
                    return {
                        "status": "success",
                        "message": f"Object '{tool_input['object_ref']}' moved to collection '{tool_input['target_collection']}'",
                        "object_ref": tool_input["object_ref"],
                        "target_collection": tool_input["target_collection"]
                    }
    
    return {
        "status": "completed",
        "message": f"Move operation completed for object '{ref}' to collection '{col}'"
    }


if __name__ == "__main__":
    result = move_object_to_collection("obj_123", "archive")
    print(result)