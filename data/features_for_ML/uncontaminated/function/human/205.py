import os
from typing import Optional, Union
from openapi_spec_validator import validate
from openapi_spec_validator.readers import read_from_filename
from ..agws_v0 import OASF_EXTENSION_NAME_MANIFEST, AgentManifest
from ..models import (
    AgentACPDescriptor,
    AgentACPSpec,
    StreamingMode,
)

def generate_agent_oapi(
    agent_source: Union[AgentACPDescriptor, AgentManifest],
    spec_path: Optional[str] = None,
):
    if spec_path is None:
        spec_path = os.getenv("ACP_SPEC_PATH", "acp-spec/openapi.json")
    spec_dict, _ = read_from_filename(spec_path)
    # If no exception is raised by validate(), the spec is valid.
    validate(spec_dict)

    agent_spec = None
    if isinstance(agent_source, AgentACPDescriptor):
        agent_spec = agent_source.specs
        agent_name = agent_source.metadata.ref.name
    elif isinstance(agent_source, AgentManifest):
        for ext in agent_source.extensions:
            if ext.name == OASF_EXTENSION_NAME_MANIFEST:
                agent_spec = ext.data.acp
                agent_name = agent_source.name
    else:
        raise ValueError("unknown object type for agent_source")

    spec_dict["info"]["title"] = f"ACP Spec for {agent_name}"

    spec_dict["components"]["schemas"]["InputSchema"] = _convert_acp_spec_schema(
        "InputSchema", agent_spec.input
    )
    spec_dict["components"]["schemas"]["OutputSchema"] = _convert_acp_spec_schema(
        "OutputSchema", agent_spec.output
    )
    spec_dict["components"]["schemas"]["ConfigSchema"] = _convert_acp_spec_schema(
        "ConfigSchema", agent_spec.config
    )

    _gen_oas_thread_runs(agent_spec, spec_dict)
    _gen_oas_interrupts(agent_spec, spec_dict)
    _gen_oas_streaming(agent_spec, spec_dict)
    _gen_oas_callback(agent_spec, spec_dict)

    validate(spec_dict)
    return spec_dict