import anthropic
import json
from datetime import datetime
from typing import Any


def generate_concise_prompt(
    current_date_time: str,
    available_tools: dict[str, list[dict[str, Any]]],
    episodic_memory: list[dict[str, Any]] = None,
) -> str:
    """Generate a concise system prompt for LLMs that accept tools in input"""
    
    prompt_parts = []
    
    # Add current date/time information
    prompt_parts.append(f"Current date and time: {current_date_time}")
    
    # Add available tools information
    if available_tools:
        prompt_parts.append("\nAvailable tools:")
        for category, tools in available_tools.items():
            prompt_parts.append(f"\n{category}:")
            for tool in tools:
                tool_name = tool.get("name", "Unknown")
                tool_description = tool.get("description", "No description")
                prompt_parts.append(f"  - {tool_name}: {tool_description}")
    
    # Add episodic memory if provided
    if episodic_memory:
        prompt_parts.append("\nRecent context from memory:")
        for memory_item in episodic_memory:
            if isinstance(memory_item, dict):
                # Format memory item concisely
                if "event" in memory_item:
                    prompt_parts.append(f"  - {memory_item['event']}")
                elif "content" in memory_item:
                    prompt_parts.append(f"  - {memory_item['content']}")
                else:
                    # Generic formatting for other memory structures
                    prompt_parts.append(f"  - {json.dumps(memory_item)}")
    
    # Add instructions for tool usage
    prompt_parts.append("\nInstructions:")
    prompt_parts.append("- Use available tools to accomplish tasks when appropriate")
    prompt_parts.append("- Provide clear and concise responses")
    prompt_parts.append("- Consider the current context and recent memory when making decisions")
    
    return "\n".join(prompt_parts)


def main():
    # Example usage
    current_date_time = "2024-01-15 14:30:00"
    
    available_tools = {
        "search": [
            {
                "name": "web_search",
                "description": "Search the web for information"
            },
            {
                "name": "local_search",
                "description": "Search local documents and files"
            }
        ],
        "communication": [
            {
                "name": "send_email",
                "description": "Send an email to specified recipients"
            },
            {
                "name": "send_message",
                "description": "Send a message to a user or group"
            }
        ]
    }
    
    episodic_memory = [
        {"event": "User asked about weather in New York"},
        {"event": "System provided weather forecast"},
        {"content": "User preferences: prefers concise responses"}
    ]
    
    prompt = generate_concise_prompt(current_date_time, available_tools, episodic_memory)
    print("Generated Prompt:")
    print("=" * 50)
    print(prompt)
    print("=" * 50)
    
    # Test with Claude API
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": "What tools are available to me?"
            }
        ]
    )
    
    print("\nClaude's Response:")
    print(message.content[0].text)


if __name__ == "__main__":
    main()