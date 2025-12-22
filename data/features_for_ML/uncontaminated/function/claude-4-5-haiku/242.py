import subprocess
import anthropic


def run_command(cmd, description=None):
    """
    Run a shell command and return its output.
    
    Args:
        cmd: The command to run as a string
        description: Optional description of what the command does
        
    Returns:
        A dictionary with 'stdout', 'stderr', and 'returncode' keys
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'stdout': '',
            'stderr': 'Command timed out after 30 seconds',
            'returncode': -1
        }
    except Exception as e:
        return {
            'stdout': '',
            'stderr': str(e),
            'returncode': -1
        }


def process_tool_call(tool_name, tool_input):
    """Process a tool call from Claude."""
    if tool_name == "run_command":
        return run_command(
            tool_input.get("cmd"),
            tool_input.get("description")
        )
    return {"error": f"Unknown tool: {tool_name}"}


def main():
    """Main function to demonstrate the tool use."""
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "run_command",
            "description": "Run a shell command and get its output",
            "input_schema": {
                "type": "object",
                "properties": {
                    "cmd": {
                        "type": "string",
                        "description": "The shell command to run"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of what the command does"
                    }
                },
                "required": ["cmd"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": "What is the current date and time? Also, list the files in the current directory."
        }
    ]
    
    print("User: What is the current date and time? Also, list the files in the current directory.")
    print()
    
    while True:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        if response.stop_reason == "tool_use":
            tool_results = []
            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_input = content_block.input
                    tool_use_id = content_block.id
                    
                    print(f"Claude is calling tool: {tool_name}")
                    print(f"With input: {tool_input}")
                    print()
                    
                    result = process_tool_call(tool_name, tool_input)
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": str(result)
                    })
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            for content_block in response.content:
                if hasattr(content_block, 'text'):
                    print("Claude:", content_block.text)
            break
    
    return response


if __name__ == "__main__":
    main()