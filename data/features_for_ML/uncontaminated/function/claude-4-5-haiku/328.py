import anthropic
from typing import Any


def get_middleware_info() -> dict[str, Any]:
    """
    Get middleware information using Claude API with tool use.
    Returns a dictionary containing middleware details.
    """
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "get_middleware_details",
            "description": "Get detailed information about middleware components and their configurations",
            "input_schema": {
                "type": "object",
                "properties": {
                    "component": {
                        "type": "string",
                        "description": "The middleware component to get information about"
                    }
                },
                "required": ["component"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": "Please provide information about common middleware components used in web applications, including authentication, logging, and error handling middleware."
        }
    ]
    
    middleware_info = {}
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    while response.stop_reason == "tool_use":
        tool_use_block = None
        for block in response.content:
            if block.type == "tool_use":
                tool_use_block = block
                break
        
        if tool_use_block:
            component = tool_use_block.input.get("component", "unknown")
            
            middleware_details = {
                "name": component,
                "type": "middleware",
                "description": f"Information about {component} middleware",
                "features": ["request processing", "response handling", "error management"],
                "status": "active"
            }
            
            middleware_info[component] = middleware_details
            
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": f"Retrieved details for {component} middleware: {middleware_details}"
                    }
                ]
            })
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                tools=tools,
                messages=messages
            )
    
    if not middleware_info:
        middleware_info = {
            "authentication": {
                "name": "Authentication Middleware",
                "type": "middleware",
                "description": "Handles user authentication and authorization",
                "features": ["token validation", "session management", "permission checking"],
                "status": "active"
            },
            "logging": {
                "name": "Logging Middleware",
                "type": "middleware",
                "description": "Logs HTTP requests and responses",
                "features": ["request logging", "response logging", "performance metrics"],
                "status": "active"
            },
            "error_handling": {
                "name": "Error Handling Middleware",
                "type": "middleware",
                "description": "Handles and formats error responses",
                "features": ["error catching", "error formatting", "error logging"],
                "status": "active"
            }
        }
    
    return middleware_info


if __name__ == "__main__":
    result = get_middleware_info()
    print("Middleware Information:")
    for key, value in result.items():
        print(f"\n{key}:")
        for k, v in value.items():
            print(f"  {k}: {v}")