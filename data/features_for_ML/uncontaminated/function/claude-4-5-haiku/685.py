import anthropic
import json
import requests
from typing import Dict, Optional, Tuple


def _get_github_api(
    endpoint: str, headers: Dict[str, str], owner: str, repo: str
) -> Tuple[bool, Optional[Dict]]:
    """Make a GET request to GitHub API and return (success, response)."""
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making GitHub API request: {e}")
        return False, None


def process_tool_call(tool_name: str, tool_input: Dict) -> str:
    """Process tool calls from Claude."""
    if tool_name == "get_github_api":
        success, response = _get_github_api(
            endpoint=tool_input["endpoint"],
            headers=tool_input["headers"],
            owner=tool_input["owner"],
            repo=tool_input["repo"]
        )
        if success:
            return json.dumps(response)
        else:
            return json.dumps({"error": "Failed to fetch from GitHub API"})
    return json.dumps({"error": f"Unknown tool: {tool_name}"})


def main():
    """Main function to demonstrate the GitHub API integration with Claude."""
    client = anthropic.Anthropic()
    
    tools = [
        {
            "name": "get_github_api",
            "description": "Make a GET request to GitHub API",
            "input_schema": {
                "type": "object",
                "properties": {
                    "endpoint": {
                        "type": "string",
                        "description": "The GitHub API endpoint (e.g., 'issues', 'pulls')"
                    },
                    "headers": {
                        "type": "object",
                        "description": "HTTP headers for the request"
                    },
                    "owner": {
                        "type": "string",
                        "description": "Repository owner"
                    },
                    "repo": {
                        "type": "string",
                        "description": "Repository name"
                    }
                },
                "required": ["endpoint", "headers", "owner", "repo"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": "Can you help me get information about the anthropic-sdk-python repository? Please fetch the list of issues from the anthropic/anthropic-sdk-python repository."
        }
    ]
    
    print("User: Can you help me get information about the anthropic-sdk-python repository? Please fetch the list of issues from the anthropic/anthropic-sdk-python repository.")
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
                    print(f"Tool input: {json.dumps(tool_input, indent=2)}")
                    print()
                    
                    result = process_tool_call(tool_name, tool_input)
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result
                    })
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            for content_block in response.content:
                if hasattr(content_block, "text"):
                    print("Claude:", content_block.text)
            break
    
    return response


if __name__ == "__main__":
    main()