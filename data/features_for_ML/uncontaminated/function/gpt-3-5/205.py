from typing import Union, Optional
from agent_acp_descriptor import AgentACPDescriptor
from agent_manifest import AgentManifest

def generate_agent_oapi(
    agent_source: Union[AgentACPDescriptor, AgentManifest],
    spec_path: Optional[str] = None,
):
    if isinstance(agent_source, AgentACPDescriptor):
        agent_name = agent_source.name
    elif isinstance(agent_source, AgentManifest):
        agent_name = agent_source.agent.name
    else:
        raise ValueError("Invalid agent source type")

    if spec_path is None:
        spec_path = f"{agent_name}_oapi.json"

    # Generate OpenAPI specification for the agent
    # Code for generating OpenAPI specification goes here

    return spec_path