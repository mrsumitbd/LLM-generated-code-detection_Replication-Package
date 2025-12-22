import anthropic


def keep(conf):
    """
    Process configuration and interact with Claude API using tool use.
    
    Args:
        conf: Configuration dictionary containing 'prompt' and 'tools' keys
        
    Returns:
        The final response from Claude after processing tool calls
    """
    client = anthropic.Anthropic()
    
    prompt = conf.get("prompt", "")
    tools = conf.get("tools", [])
    
    messages = [{"role": "user", "content": prompt}]
    
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
            return None
        
        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    
                    if tool_name == "add":
                        result = tool_input["a"] + tool_input["b"]
                    elif tool_name == "subtract":
                        result = tool_input["a"] - tool_input["b"]
                    elif tool_name == "multiply":
                        result = tool_input["a"] * tool_input["b"]
                    elif tool_name == "divide":
                        if tool_input["b"] == 0:
                            result = "Error: Division by zero"
                        else:
                            result = tool_input["a"] / tool_input["b"]
                    else:
                        result = f"Unknown tool: {tool_name}"
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result)
                    })
            
            messages.append({"role": "user", "content": tool_results})
        else:
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            return None