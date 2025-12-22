import click
import json
import sys
from pathlib import Path
from anthropic import Anthropic

# Initialize the Anthropic client
client = Anthropic()

# Store conversation history
conversation_history = []

# Store available tools
available_tools = []

def load_tools_from_file(file_path: str) -> list:
    """Load tool definitions from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        click.echo(f"Error: Tool file '{file_path}' not found.", err=True)
        sys.exit(1)
    except json.JSONDecodeError:
        click.echo(f"Error: Invalid JSON in tool file '{file_path}'.", err=True)
        sys.exit(1)

def format_tool_for_claude(tool: dict) -> dict:
    """Format a tool definition for Claude's tool_use feature."""
    return {
        "name": tool.get("name", ""),
        "description": tool.get("description", ""),
        "input_schema": tool.get("input_schema", {
            "type": "object",
            "properties": {},
            "required": []
        })
    }

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """Process a tool call and return the result."""
    # Find the tool in available_tools
    tool = next((t for t in available_tools if t.get("name") == tool_name), None)
    
    if not tool:
        return json.dumps({"error": f"Tool '{tool_name}' not found"})
    
    # For demonstration, we'll return a mock result
    # In a real implementation, this would execute the actual tool
    result = {
        "tool": tool_name,
        "input": tool_input,
        "result": f"Mock result for {tool_name} with input {tool_input}"
    }
    
    return json.dumps(result)

@click.group()
def mcp_client_command():
    """
    MCP client commands.
    """
    pass

@mcp_client_command.command()
@click.option('--tools', type=click.Path(exists=True), help='Path to tools JSON file')
@click.option('--model', default='claude-3-5-sonnet-20241022', help='Claude model to use')
def chat(tools: str, model: str):
    """Start an interactive chat session with Claude."""
    global available_tools, conversation_history
    
    # Load tools if provided
    if tools:
        available_tools = load_tools_from_file(tools)
        click.echo(f"Loaded {len(available_tools)} tools from {tools}")
    
    click.echo("Starting MCP client chat session. Type 'exit' to quit.")
    click.echo(f"Using model: {model}")
    if available_tools:
        click.echo(f"Available tools: {', '.join(t.get('name', '') for t in available_tools)}")
    click.echo()
    
    while True:
        try:
            user_input = click.prompt("You")
        except EOFError:
            break
        
        if user_input.lower() == 'exit':
            click.echo("Goodbye!")
            break
        
        # Add user message to history
        conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Prepare tools for Claude
        tools_for_claude = []
        if available_tools:
            tools_for_claude = [format_tool_for_claude(tool) for tool in available_tools]
        
        # Call Claude API
        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                tools=tools_for_claude if tools_for_claude else None,
                messages=conversation_history
            )
            
            # Process response
            assistant_message = ""
            tool_calls = []
            
            for block in response.content:
                if hasattr(block, 'text'):
                    assistant_message += block.text
                elif block.type == "tool_use":
                    tool_calls.append({
                        "id": block.id,
                        "name": block.name,
                        "input": block.input
                    })
            
            # Add assistant response to history
            if assistant_message:
                conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                click.echo(f"Claude: {assistant_message}")
            
            # Process tool calls if any
            if tool_calls:
                for tool_call in tool_calls:
                    click.echo(f"[Calling tool: {tool_call['name']}]")
                    result = process_tool_call(tool_call['name'], tool_call['input'])
                    
                    # Add tool result to history
                    conversation_history.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_call['id'],
                                "content": result
                            }
                        ]
                    })
                    
                    # Get follow-up response from Claude
                    follow_up = client.messages.create(
                        model=model,
                        max_tokens=1024,
                        tools=tools_for_claude if tools_for_claude else None,
                        messages=conversation_history
                    )
                    
                    for block in follow_up.content:
                        if hasattr(block, 'text'):
                            click.echo(f"Claude: {block.text}")
                            conversation_history.append({
                                "role": "assistant",
                                "content": block.text
                            })
            
            click.echo()
            
        except Exception as e:
            click.echo(f"Error: {str(e)}", err=True)
            # Remove the last user message if there was an error
            if conversation_history and conversation_history[-1]["role"] == "user":
                conversation_history.pop()

@mcp_client_command.command()
@click.option('--tools', type=click.Path(exists=True), help='Path to tools JSON file')
@click.option('--model', default='claude-3-5-sonnet-20241022', help='Claude model to use')
@click.argument('message')
def ask(tools: str, model: str, message: str):
    """Send a single message to Claude."""
    global available_tools
    
    # Load tools if provided
    if tools:
        available_tools = load_tools_from_file(tools)
    
    # Prepare tools for Claude
    tools_for_claude = []
    if available_tools:
        tools_for_claude = [format_tool_for_claude(tool) for tool in available_tools]
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            tools=tools_for_claude if tools_for_claude else None,
            messages=[{"role": "user", "content": message}]
        )
        
        # Process response
        for block in response.content:
            if hasattr(block, 'text'):
                click.echo(block.text)
            elif block.type == "tool_use":
                click.echo(f"[Tool call: {block.name}]")
                result = process_tool_call(block.name, block.input)
                click.echo(f"Result: {result}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@mcp_client_command.command()
@click.argument('file_path', type=click.Path(exists=True))
def validate_tools(file_path: str):
    """Validate a tools JSON file."""
    try:
        tools = load_tools_from_file(file_path)
        click.echo(f"✓ Valid tools file with {len(tools)} tools:")
        for tool in tools:
            click.echo(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
    except Exception as e:
        click.echo(f"✗ Invalid tools file: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    mcp_client_command()