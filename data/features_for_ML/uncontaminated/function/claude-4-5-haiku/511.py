import anthropic


def flow_initial_velocity_toggle(value):
    """
    Toggle the initial velocity flow setting using Claude API with tool use.
    
    Args:
        value: The initial velocity value to toggle
        
    Returns:
        The result of toggling the initial velocity flow setting
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "toggle_flow_setting",
            "description": "Toggle the initial velocity flow setting",
            "input_schema": {
                "type": "object",
                "properties": {
                    "setting_name": {
                        "type": "string",
                        "description": "The name of the flow setting to toggle"
                    },
                    "current_value": {
                        "type": "number",
                        "description": "The current value of the setting"
                    },
                    "new_value": {
                        "type": "number",
                        "description": "The new value after toggling"
                    }
                },
                "required": ["setting_name", "current_value", "new_value"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": f"Toggle the initial velocity flow setting with value {value}. The new value should be the opposite or inverse of the current value."
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
                tool_input = content_block.input
                return {
                    "toggled": True,
                    "original_value": tool_input.get("current_value"),
                    "new_value": tool_input.get("new_value"),
                    "setting": tool_input.get("setting_name")
                }
    
    return {
        "toggled": False,
        "original_value": value,
        "message": "Could not toggle the setting"
    }


if __name__ == "__main__":
    result = flow_initial_velocity_toggle(10.5)
    print(f"Result: {result}")