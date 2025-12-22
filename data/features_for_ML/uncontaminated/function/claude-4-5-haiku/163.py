import json
import os
from pathlib import Path
from anthropic import Anthropic

def extract_openai_agents_graph(scan_path: str, output_file: str):
    """
    Extract OpenAI agents graph from a scan path using Claude AI.
    
    Args:
        scan_path: Path to the directory or file to scan
        output_file: Path to write the extracted graph JSON
    """
    client = Anthropic()
    conversation_history = []
    
    # Read the scan path content
    scan_content = ""
    if os.path.isfile(scan_path):
        with open(scan_path, 'r') as f:
            scan_content = f.read()
    elif os.path.isdir(scan_path):
        for root, dirs, files in os.walk(scan_path):
            for file in files:
                if file.endswith(('.py', '.json', '.yaml', '.yml', '.txt')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            scan_content += f"\n--- File: {file_path} ---\n"
                            scan_content += f.read()
                    except:
                        pass
    
    if not scan_content:
        raise ValueError(f"No readable content found at {scan_path}")
    
    # First turn: Ask Claude to analyze the content
    initial_message = f"""I have the following code/configuration that may contain OpenAI agents graph information:

{scan_content[:10000]}  # Limit to first 10000 chars for initial analysis

Please analyze this content and identify:
1. Any OpenAI agents or agent definitions
2. The structure and relationships between agents
3. Any graph or workflow definitions
4. Tool definitions and their connections

What do you find?"""
    
    conversation_history.append({
        "role": "user",
        "content": initial_message
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2048,
        messages=conversation_history
    )
    
    assistant_response = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })
    
    # Second turn: Ask for structured extraction
    extraction_message = """Based on your analysis, please extract the agents graph in the following JSON format:
{
    "agents": [
        {
            "id": "agent_id",
            "name": "agent_name",
            "type": "agent_type",
            "description": "description",
            "tools": ["tool1", "tool2"],
            "model": "model_name"
        }
    ],
    "tools": [
        {
            "id": "tool_id",
            "name": "tool_name",
            "description": "description",
            "parameters": {}
        }
    ],
    "connections": [
        {
            "from": "agent_or_tool_id",
            "to": "agent_or_tool_id",
            "type": "connection_type"
        }
    ],
    "workflows": [
        {
            "id": "workflow_id",
            "name": "workflow_name",
            "steps": ["agent_id1", "agent_id2"],
            "description": "description"
        }
    ]
}

Please provide the complete extracted graph as valid JSON."""
    
    conversation_history.append({
        "role": "user",
        "content": extraction_message
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=conversation_history
    )
    
    extraction_response = response.content[0].text
    conversation_history.append({
        "role": "assistant",
        "content": extraction_response
    })
    
    # Third turn: Validate and refine
    validation_message = """Please review the JSON you provided and ensure:
1. All required fields are present
2. The JSON is valid and properly formatted
3. All connections reference valid agent/tool IDs
4. No circular dependencies exist (unless intentional)

If there are any issues, provide a corrected version. Otherwise, confirm the JSON is correct."""
    
    conversation_history.append({
        "role": "user",
        "content": validation_message
    })
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        messages=conversation_history
    )
    
    final_response = response.content[0].text
    
    # Extract JSON from the response
    json_str = ""
    in_json = False
    for line in final_response.split('\n'):
        if line.strip().startswith('{'):
            in_json = True
        if in_json:
            json_str += line + '\n'
        if line.strip().endswith('}') and in_json:
            break
    
    # Parse and validate JSON
    try:
        graph_data = json.loads(json_str)
    except json.JSONDecodeError:
        # If JSON extraction fails, create a basic structure
        graph_data = {
            "agents": [],
            "tools": [],
            "connections": [],
            "workflows": [],
            "analysis": final_response
        }
    
    # Write to output file
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(graph_data, f, indent=2)
    
    return graph_data


if __name__ == "__main__":
    # Example usage
    import tempfile
    
    # Create a sample file to scan
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("""
# Sample OpenAI agents configuration
agents = {
    "agent1": {
        "name": "Research Agent",
        "model": "gpt-4",
        "tools": ["search", "summarize"]
    },
    "agent2": {
        "name": "Writing Agent", 
        "model": "gpt-4",
        "tools": ["write", "edit"]
    }
}

tools = {
    "search": {"description": "Search the web"},
    "summarize": {"description": "Summarize text"},
    "write": {"description": "Write content"},
    "edit": {"description": "Edit content"}
}
""")
        temp_file = f.name
    
    try:
        # Extract the graph
        result = extract_openai_agents_graph(temp_file, "agents_graph.json")
        print("Extraction complete. Graph saved to agents_graph.json")
        print(json.dumps(result, indent=2))
    finally:
        os.unlink(temp_file)