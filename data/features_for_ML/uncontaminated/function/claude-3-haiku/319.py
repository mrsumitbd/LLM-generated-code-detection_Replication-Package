import os
import ast
from typing import Set, Dict

def collect_tasks(root_dir: str, agents: Set[str]) -> Dict[str, str]:
    """Parses all Python modules in the given directory and collects task-agent mappings.

    Args:
        root_dir (str): Path to the codebase directory
        agents (set[str]): Set of all known agent names

    Returns:
        dict[str, str]: A dictionary mapping task names to agent names
    """
    task_agent_mapping = {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as file:
                    try:
                        tree = ast.parse(file.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                for decorator in node.decorator_list:
                                    if isinstance(decorator, ast.Call) and hasattr(decorator.func, 'id') and decorator.func.id == 'task':
                                        task_name = node.name
                                        for arg in decorator.args:
                                            if isinstance(arg, ast.Constant) and arg.value in agents:
                                                agent_name = arg.value
                                                task_agent_mapping[task_name] = agent_name
                                                break
                    except (SyntaxError, UnicodeDecodeError):
                        pass

    return task_agent_mapping