import datetime
from typing import Any

def generate_concise_prompt(
    current_date_time: str,
    available_tools: dict[str, list[dict[str, Any]]],
    episodic_memory: list[dict[str, Any]] = None,
) -> str:
    """Generate a concise system prompt for LLMs that accept tools in input"""
    current_datetime = datetime.datetime.strptime(current_date_time, "%Y-%m-%d %H:%M:%S")
    prompt = f"The current date and time is {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}.\n\n"

    if episodic_memory:
        prompt += "Based on my episodic memory, the relevant information is:\n"
        for memory in episodic_memory:
            prompt += f"- {memory['content']}\n"
        prompt += "\n"

    prompt += "The available tools are:\n"
    for tool_name, tool_info in available_tools.items():
        prompt += f"- {tool_name}:\n"
        for tool_capability in tool_info:
            prompt += f"  - {tool_capability['description']}\n"
        prompt += "\n"

    prompt += "Please provide a concise response using the available tools."
    return prompt