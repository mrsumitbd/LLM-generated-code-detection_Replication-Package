def prepare_agent_artifacts(agent_factory_outputs: dict[str, str]) -> dict[str, str]:
    """Prepares the agent outputs (based on AgentFactoryOutputs)
    for saving by filling in the code generation templates
    and gathering (Python) tool files.
    """
    agent_artifacts = {}

    for agent_id, agent_output in agent_factory_outputs.items():
        # Fill in the code generation templates
        agent_code = fill_code_templates(agent_output)

        # Gather the Python tool files
        agent_tools = gather_tool_files(agent_output)

        agent_artifacts[agent_id] = {
            'code': agent_code,
            'tools': agent_tools
        }

    return agent_artifacts

def fill_code_templates(agent_output: str) -> str:
    # Implementation to fill in the code generation templates
    # based on the provided agent_output
    return processed_code

def gather_tool_files(agent_output: str) -> dict[str, str]:
    # Implementation to gather the Python tool files
    # based on the provided agent_output
    return tool_files