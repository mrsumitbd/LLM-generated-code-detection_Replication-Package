def prepare_agent_artifacts(agent_factory_outputs: dict[str, str]) -> dict[str, str]:
    """Prepares the agent outputs (based on AgentFactoryOutputs)
    for saving by filling in the code generation templates
    and gathering (Python) tool files.
    """
    artifacts = {}
    
    for key, value in agent_factory_outputs.items():
        if key.endswith('.py'):
            artifacts[key] = value
        elif key.endswith('.txt') or key.endswith('.md'):
            artifacts[key] = value
        elif key == 'agent_code':
            artifacts['agent.py'] = value
        elif key == 'tools_code':
            artifacts['tools.py'] = value
        elif key == 'requirements':
            artifacts['requirements.txt'] = value
        elif key == 'readme':
            artifacts['README.md'] = value
        else:
            artifacts[key] = value
    
    return artifacts