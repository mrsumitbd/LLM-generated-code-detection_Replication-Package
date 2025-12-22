from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

def generate_concise_prompt(
    current_date_time: str,
    available_tools: Dict[str, List[Dict[str, Any]]],
    episodic_memory: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Generate a concise system prompt for LLMs that accept tools in input.

    Parameters
    ----------
    current_date_time : str
        Current date and time string.
    available_tools : dict[str, list[dict[str, Any]]]
        Mapping from tool name to a list of tool definitions. Each tool definition
        should contain at least a 'name', 'description', and optionally
        'parameters' (a dict describing the JSON schema for arguments).
    episodic_memory : list[dict[str, Any]] | None, optional
        Optional list of memory entries that should be included in the prompt.

    Returns
    -------
    str
        A concise system prompt string.
    """
    # Header
    prompt_parts = [
        "You are an AI assistant.",
        f"Current date/time: {current_date_time}.",
        "",
        "You have access to the following tools:",
    ]

    # Format each tool
    for tool_name, tool_defs in available_tools.items():
        for tool_def in tool_defs:
            name = tool_def.get("name", tool_name)
            description = tool_def.get("description", "No description provided.")
            params = tool_def.get("parameters")
            prompt_parts.append(f"- {name}: {description}")
            if params:
                # Pretty‑print JSON schema for readability
                try:
                    params_str = json.dumps(params, indent=2, ensure_ascii=False)
                except Exception:
                    params_str = str(params)
                prompt_parts.append(f"  Parameters:\n{params_str}")

    # Include episodic memory if provided
    if episodic_memory:
        prompt_parts.append("")
        prompt_parts.append("Recent memory:")
        for idx, mem in enumerate(episodic_memory, start=1):
            # Convert each memory entry to a JSON string for clarity
            try:
                mem_str = json.dumps(mem, ensure_ascii=False)
            except Exception:
                mem_str = str(mem)
            prompt_parts.append(f"{idx}. {mem_str}")

    # Instruction for tool usage
    prompt_parts.append("")
    prompt_parts.append(
        "When you need to use a tool, respond with a JSON object in the following format:"
    )
    prompt_parts.append(
        "  {\"name\": \"tool_name\", \"arguments\": { ... }}\n"
        "If no tool is needed, simply provide the answer."
    )

    return "\n".join(prompt_parts)