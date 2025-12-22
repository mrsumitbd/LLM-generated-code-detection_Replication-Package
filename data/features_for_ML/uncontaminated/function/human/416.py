from agent_factory.instructions import AGENT_CODE_TEMPLATE
from agent_factory.utils import prepare_python_code, validate_dependencies
from agent_factory.utils.mcpd_utils import export_mcpd_config_artifacts

def prepare_agent_artifacts(agent_factory_outputs: dict[str, str]) -> dict[str, str]:
    """Prepares the agent outputs (based on AgentFactoryOutputs)
    for saving by filling in the code generation templates
    and gathering (Python) tool files.
    """
    artifacts_to_save = {}

    agent_code = AGENT_CODE_TEMPLATE.format(**agent_factory_outputs)
    valid_agent_code = prepare_python_code(agent_code)
    artifacts_to_save["agent.py"] = valid_agent_code.code

    artifacts_to_save["README.md"] = agent_factory_outputs["readme"]

    dependencies = set()
    # Identify and read tool files
    for tool_file in TOOLS_DIR.iterdir():
        if tool_file.is_file() and (tool_file.stem in agent_code or tool_file.name == "__init__.py"):
            if tool_file.suffix != ".py":
                continue
            tool_code = tool_file.read_text(encoding="utf-8")
            dependencies.update(extract_requirements_from_string(tool_code))
            artifacts_to_save[f"tools/{tool_file.name}"] = tool_code

    dependencies.update(extract_requirements_from_string(valid_agent_code.code))  # type: ignore
    dependencies_list = list(dependencies)
    validated_dependencies = validate_dependencies(agent_factory_outputs["tools"], dependencies_list)
    artifacts_to_save["requirements.txt"] = validated_dependencies

    cli_args_str = agent_factory_outputs.get("cli_args", "")
    artifacts_to_save["agent_parameters.json"] = parse_cli_args_to_params_json(cli_args_str)

    mcpd_artifacts = export_mcpd_config_artifacts(agent_factory_outputs)
    artifacts_to_save.update(mcpd_artifacts)

    # Add a .gitignore file for ignoring secrets
    artifacts_to_save[".gitignore"] = "*secrets*.dev.toml\n!secrets.prod.toml"

    return artifacts_to_save