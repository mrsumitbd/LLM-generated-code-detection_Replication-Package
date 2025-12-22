import anthropic


def get_chained_entity_path(entity_name: str) -> str:
    """
    Get the chained entity path for a given entity name using Claude API with tool use.
    
    Args:
        entity_name: The name of the entity to get the path for
        
    Returns:
        The chained entity path as a string
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "get_entity_parent",
            "description": "Get the parent entity of a given entity",
            "input_schema": {
                "type": "object",
                "properties": {
                    "entity": {
                        "type": "string",
                        "description": "The entity name to get the parent of"
                    }
                },
                "required": ["entity"]
            }
        },
        {
            "name": "is_root_entity",
            "description": "Check if an entity is a root entity (has no parent)",
            "input_schema": {
                "type": "object",
                "properties": {
                    "entity": {
                        "type": "string",
                        "description": "The entity name to check"
                    }
                },
                "required": ["entity"]
            }
        }
    ]
    
    entity_hierarchy = {
        "user": "organization",
        "organization": "company",
        "company": "enterprise",
        "enterprise": None,
        "post": "user",
        "comment": "post",
        "like": "post"
    }
    
    def get_entity_parent(entity: str) -> str:
        parent = entity_hierarchy.get(entity.lower())
        if parent is None:
            return "No parent"
        return parent
    
    def is_root_entity(entity: str) -> bool:
        parent = entity_hierarchy.get(entity.lower())
        return parent is None
    
    messages = [
        {
            "role": "user",
            "content": f"Find the complete chained path from '{entity_name}' to the root entity by repeatedly getting the parent entity until you reach a root entity. Return the path as a comma-separated list starting from '{entity_name}' and ending at the root."
        }
    ]
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            return ""
        
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    
                    if tool_name == "get_entity_parent":
                        result = get_entity_parent(tool_input["entity"])
                    elif tool_name == "is_root_entity":
                        result = is_root_entity(tool_input["entity"])
                    else:
                        result = "Unknown tool"
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break
    
    return ""


if __name__ == "__main__":
    result = get_chained_entity_path("comment")
    print(f"Chained entity path for 'comment': {result}")
    
    result = get_chained_entity_path("user")
    print(f"Chained entity path for 'user': {result}")