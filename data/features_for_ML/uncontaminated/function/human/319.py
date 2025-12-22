import ast
from agentic_radar.analysis.utils import walk_python_files
from agentic_radar.analysis.crewai.parsing.yaml_config import (
    collect_task_agents_from_config,
)

def collect_tasks(root_dir: str, agents: set[str]) -> dict[str, str]:
    """Parses all Python modules in the given directory and collects task-agent mappings.

    Args:
        root_dir (str): Path to the codebase directory
        agents (set[str]): Set of all known agent names

    Returns:
        dict[str, str]: A dictionary mapping task names to agent names
    """
    task_agent_mapping: dict[str, str] = {}

    yaml_file_to_task_agents_mapping = collect_task_agents_from_config(root_dir)

    for file in walk_python_files(root_dir):
        with open(file, "r") as f:
            try:
                tree = ast.parse(f.read())
            except Exception as e:
                print(f"Cannot parse Python module: {file}. Error: {e}")
                continue
            tasks_visitor = TasksVisitor(agents=agents)
            tasks_visitor.visit(tree)
            task_agent_mapping |= tasks_visitor.task_agent_mapping

            # Add task-agent mapping from YAML config files
            for found_config_path in tasks_visitor.yaml_config_paths:
                for (
                    config_path,
                    yaml_task_agent_mapping,
                ) in yaml_file_to_task_agents_mapping.items():
                    if found_config_path not in config_path:
                        continue
                    task_agent_mapping = yaml_task_agent_mapping | task_agent_mapping

    return task_agent_mapping