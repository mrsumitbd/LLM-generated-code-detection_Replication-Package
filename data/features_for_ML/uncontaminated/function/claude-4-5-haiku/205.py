import json
import os
from typing import Union, Optional
from anthropic import Anthropic

# Define the data classes for type hints
class AgentACPDescriptor:
    def __init__(self, data: dict):
        self.data = data

class AgentManifest:
    def __init__(self, data: dict):
        self.data = data

def generate_agent_oapi(
    agent_source: Union[AgentACPDescriptor, AgentManifest],
    spec_path: Optional[str] = None,
):
    """
    Generate an OpenAPI specification for an agent using Claude.
    
    Args:
        agent_source: Either an AgentACPDescriptor or AgentManifest containing agent information
        spec_path: Optional path to save the generated OpenAPI spec
    
    Returns:
        The generated OpenAPI specification as a dictionary
    """
    client = Anthropic()
    
    # Extract the data from the agent source
    if isinstance(agent_source, AgentACPDescriptor):
        agent_data = agent_source.data
        source_type = "ACP Descriptor"
    elif isinstance(agent_source, AgentManifest):
        agent_data = agent_source.data
        source_type = "Agent Manifest"
    else:
        # Handle dict input for flexibility
        agent_data = agent_source
        source_type = "Agent Data"
    
    # Convert agent data to JSON string for the prompt
    agent_json = json.dumps(agent_data, indent=2)
    
    # Create a conversation with Claude to generate the OpenAPI spec
    conversation_history = []
    
    # First message: ask Claude to analyze the agent and generate OpenAPI spec
    initial_prompt = f"""I have an agent defined as a {source_type}. Please analyze this agent and generate a complete OpenAPI 3.0.0 specification for it.

Agent Data:
{agent_json}

Please generate a valid OpenAPI 3.0.0 specification that:
1. Describes all the agent's capabilities and endpoints
2. Includes proper schemas for request/response bodies
3. Has appropriate security definitions if needed
4. Includes descriptions for all operations
5. Returns ONLY valid JSON that can be parsed

Return the OpenAPI specification as a valid JSON object."""
    
    conversation_history.append({
        "role": "user",
        "content": initial_prompt
    })
    
    # Get Claude's response
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=conversation_history
    )
    
    assistant_message = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })
    
    # Try to parse the OpenAPI spec from the response
    openapi_spec = None
    
    # First, try to find JSON in the response
    try:
        # Look for JSON block in the response
        if "```json" in assistant_message:
            json_start = assistant_message.find("```json") + 7
            json_end = assistant_message.find("```", json_start)
            json_str = assistant_message[json_start:json_end].strip()
            openapi_spec = json.loads(json_str)
        elif "```" in assistant_message:
            json_start = assistant_message.find("```") + 3
            json_end = assistant_message.find("```", json_start)
            json_str = assistant_message[json_start:json_end].strip()
            openapi_spec = json.loads(json_str)
        else:
            # Try to parse the entire response as JSON
            openapi_spec = json.loads(assistant_message)
    except (json.JSONDecodeError, ValueError):
        # If parsing fails, ask Claude to fix it
        conversation_history.append({
            "role": "user",
            "content": "The response doesn't appear to be valid JSON. Please provide ONLY the OpenAPI specification as a valid JSON object, without any markdown formatting or additional text."
        })
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=conversation_history
        )
        
        assistant_message = response.content[0].text
        
        try:
            # Try to extract JSON from the corrected response
            if "```json" in assistant_message:
                json_start = assistant_message.find("```json") + 7
                json_end = assistant_message.find("```", json_start)
                json_str = assistant_message[json_start:json_end].strip()
                openapi_spec = json.loads(json_str)
            elif "```" in assistant_message:
                json_start = assistant_message.find("```") + 3
                json_end = assistant_message.find("```", json_start)
                json_str = assistant_message[json_start:json_end].strip()
                openapi_spec = json.loads(json_str)
            else:
                openapi_spec = json.loads(assistant_message)
        except (json.JSONDecodeError, ValueError):
            # Last resort: create a basic OpenAPI spec
            openapi_spec = {
                "openapi": "3.0.0",
                "info": {
                    "title": "Generated Agent API",
                    "version": "1.0.0"
                },
                "paths": {}
            }
    
    # Save the spec if a path is provided
    if spec_path:
        os.makedirs(os.path.dirname(spec_path) if os.path.dirname(spec_path) else ".", exist_ok=True)
        with open(spec_path, 'w') as f:
            json.dump(openapi_spec, f, indent=2)
    
    return openapi_spec


# Example usage and testing
if __name__ == "__main__":
    # Create sample agent data
    sample_agent_manifest = AgentManifest({
        "name": "Weather Agent",
        "description": "An agent that provides weather information",
        "capabilities": [
            {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "parameters": {
                    "location": "string",
                    "units": "string (celsius or fahrenheit)"
                }
            },
            {
                "name": "get_forecast",
                "description": "Get weather forecast for a location",
                "parameters": {
                    "location": "string",
                    "days": "integer (1-10)"
                }
            }
        ]
    })
    
    # Generate OpenAPI spec
    spec = generate_agent_oapi(sample_agent_manifest)
    
    # Print the generated spec
    print("Generated OpenAPI Specification:")
    print(json.dumps(spec, indent=2))