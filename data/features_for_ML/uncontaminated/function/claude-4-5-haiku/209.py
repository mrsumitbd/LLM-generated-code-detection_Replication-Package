import anthropic
import json
import os


def configure_server_properties(server_name, base_dir):
    """Configures common server properties interactively.

    Args:
        server_name (str): The name of the server.
        base_dir (str): The base directory where servers are stored.
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "get_server_config",
            "description": "Retrieves the current configuration of a server",
            "input_schema": {
                "type": "object",
                "properties": {
                    "server_name": {
                        "type": "string",
                        "description": "The name of the server"
                    }
                },
                "required": ["server_name"]
            }
        },
        {
            "name": "set_server_property",
            "description": "Sets a property on the server",
            "input_schema": {
                "type": "object",
                "properties": {
                    "server_name": {
                        "type": "string",
                        "description": "The name of the server"
                    },
                    "property_name": {
                        "type": "string",
                        "description": "The name of the property to set"
                    },
                    "property_value": {
                        "type": "string",
                        "description": "The value to set for the property"
                    }
                },
                "required": ["server_name", "property_name", "property_value"]
            }
        },
        {
            "name": "list_available_properties",
            "description": "Lists all available properties that can be configured for a server",
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
        {
            "name": "save_configuration",
            "description": "Saves the current server configuration to disk",
            "input_schema": {
                "type": "object",
                "properties": {
                    "server_name": {
                        "type": "string",
                        "description": "The name of the server"
                    }
                },
                "required": ["server_name"]
            }
        }
    ]
    
    server_config = {
        "name": server_name,
        "port": 8080,
        "host": "localhost",
        "debug": False,
        "max_connections": 100,
        "timeout": 30,
        "ssl_enabled": False,
        "log_level": "INFO"
    }
    
    def get_server_config(server_name):
        return json.dumps(server_config)
    
    def set_server_property(server_name, property_name, property_value):
        if property_name in server_config:
            if property_name in ["port", "max_connections", "timeout"]:
                server_config[property_name] = int(property_value)
            elif property_name in ["debug", "ssl_enabled"]:
                server_config[property_name] = property_value.lower() in ["true", "yes", "1"]
            else:
                server_config[property_name] = property_value
            return json.dumps({"status": "success", "message": f"Property '{property_name}' set to '{property_value}'"})
        else:
            return json.dumps({"status": "error", "message": f"Unknown property '{property_name}'"})
    
    def list_available_properties():
        properties = {
            "port": "Server port number (integer)",
            "host": "Server host address (string)",
            "debug": "Debug mode (boolean)",
            "max_connections": "Maximum number of connections (integer)",
            "timeout": "Connection timeout in seconds (integer)",
            "ssl_enabled": "Enable SSL/TLS (boolean)",
            "log_level": "Logging level (DEBUG, INFO, WARNING, ERROR)"
        }
        return json.dumps(properties)
    
    def save_configuration(server_name):
        config_dir = os.path.join(base_dir, server_name)
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, "config.json")
        with open(config_file, 'w') as f:
            json.dump(server_config, f, indent=2)
        return json.dumps({"status": "success", "message": f"Configuration saved to {config_file}"})
    
    messages = [
        {
            "role": "user",
            "content": f"Please help me configure the server '{server_name}'. Start by showing me the current configuration, then help me set up common properties like port, host, debug mode, and other important settings. After we're done configuring, save the configuration."
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
            break
        
        if response.stop_reason == "tool_use":
            tool_results = []
            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_input = content_block.input
                    tool_use_id = content_block.id
                    
                    if tool_name == "get_server_config":
                        result = get_server_config(tool_input.get("server_name", server_name))
                    elif tool_name == "set_server_property":
                        result = set_server_property(
                            tool_input.get("server_name", server_name),
                            tool_input.get("property_name"),
                            tool_input.get("property_value")
                        )
                    elif tool_name == "list_available_properties":
                        result = list_available_properties()
                    elif tool_name == "save_configuration":
                        result = save_configuration(tool_input.get("server_name", server_name))
                    else:
                        result = json.dumps({"error": f"Unknown tool: {tool_name}"})
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result
                    })
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break
    
    return server_config


if __name__ == "__main__":
    base_directory = "/tmp/servers"
    server_name = "my_server"
    
    config = configure_server_properties(server_name, base_directory)
    print(f"\nFinal configuration for {server_name}:")
    print(json.dumps(config, indent=2))