import anthropic
import json


def get_cfgs():
    """
    Retrieves configuration information using Claude API with tool use.
    Returns a dictionary containing system configurations.
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "get_system_config",
            "description": "Retrieves system configuration information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "config_type": {
                        "type": "string",
                        "description": "Type of configuration to retrieve (e.g., 'database', 'api', 'cache')"
                    }
                },
                "required": ["config_type"]
            }
        },
        {
            "name": "get_all_configs",
            "description": "Retrieves all available configurations",
            "input_schema": {
                "type": "object",
                "properties": {}
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": "Please retrieve all system configurations for me."
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    configs = {}
    
    while response.stop_reason == "tool_use":
        tool_use_block = None
        for block in response.content:
            if block.type == "tool_use":
                tool_use_block = block
                break
        
        if not tool_use_block:
            break
        
        tool_name = tool_use_block.name
        tool_input = tool_use_block.input
        
        if tool_name == "get_system_config":
            config_type = tool_input.get("config_type", "unknown")
            configs[config_type] = {
                "status": "configured",
                "type": config_type
            }
        elif tool_name == "get_all_configs":
            configs = {
                "database": {
                    "host": "localhost",
                    "port": 5432,
                    "name": "main_db"
                },
                "api": {
                    "endpoint": "https://api.example.com",
                    "version": "v1",
                    "timeout": 30
                },
                "cache": {
                    "type": "redis",
                    "host": "localhost",
                    "port": 6379,
                    "ttl": 3600
                },
                "logging": {
                    "level": "INFO",
                    "format": "json",
                    "output": "stdout"
                }
            }
        
        messages.append({"role": "assistant", "content": response.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_use_block.id,
                    "content": json.dumps(configs)
                }
            ]
        })
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
    
    return configs


if __name__ == "__main__":
    result = get_cfgs()
    print("Configuration retrieved:")
    print(json.dumps(result, indent=2))