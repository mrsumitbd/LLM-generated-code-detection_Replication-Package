import os
from pathlib import Path
from typing import Dict

def prepare_agent_artifacts(agent_factory_outputs: Dict[str, str]) -> Dict[str, str]:
    """
    Prepares the agent outputs (based on AgentFactoryOutputs)
    for saving by filling in the code generation templates
    and gathering (Python) tool files.

    Parameters
    ----------
    agent_factory_outputs : dict[str, str]
        Dictionary containing keys such as:
        - 'agent_template': a string template for the agent code.
        - 'tool_files': a list of file paths (as a comma‑separated string)
          pointing to Python tool files.
        - 'tool_code': optional pre‑generated tool code string.

    Returns
    -------
    dict[str, str]
        Mapping from file names to their content ready for saving.
    """
    # Result dictionary to hold file names and their contents
    artifacts: Dict[str, str] = {}

    # Retrieve the agent template if present
    agent_template = agent_factory_outputs.get("agent_template")
    if not agent_template:
        # Nothing to do if no template is provided
        return artifacts

    # Gather tool file paths
    tool_files_raw = agent_factory_outputs.get("tool_files", "")
    # Accept both list and comma‑separated string
    if isinstance(tool_files_raw, str):
        # Split on commas and strip whitespace
        tool_file_paths = [p.strip() for p in tool_files_raw.split(",") if p.strip()]
    else:
        # Assume iterable of paths
        tool_file_paths = list(tool_files_raw)

    # Read each tool file and store its content
    tool_code_parts = []
    for path in tool_file_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Store the tool file content in the artifacts dict
            artifacts[Path(path).name] = content
            tool_code_parts.append(content)
        except Exception:
            # Skip files that cannot be read
            continue

    # If a pre‑generated tool code string is provided, use it
    pre_tool_code = agent_factory_outputs.get("tool_code")
    if pre_tool_code:
        tool_code = pre_tool_code
    else:
        # Join all tool code parts with a newline separator
        tool_code = "\n\n".join(tool_code_parts)

    # Replace placeholder in the agent template
    # The placeholder is expected to be {tool_code}
    filled_agent = agent_template.replace("{tool_code}", tool_code)

    # Add the agent code to the artifacts dict
    artifacts["agent.py"] = filled_agent

    return artifacts