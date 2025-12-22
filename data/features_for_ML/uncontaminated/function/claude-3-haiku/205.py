from typing import Union, Optional
from .agent_descriptor import AgentACPDescriptor
from .agent_manifest import AgentManifest

def generate_agent_oapi(
    agent_source: Union[AgentACPDescriptor, AgentManifest],
    spec_path: Optional[str] = None,
):
    if isinstance(agent_source, AgentACPDescriptor):
        return agent_source.generate_oapi_spec(spec_path)
    elif isinstance(agent_source, AgentManifest):
        return agent_source.generate_oapi_spec(spec_path)
    else:
        raise ValueError("agent_source must be either AgentACPDescriptor or AgentManifest")