import ast
import os
from typing import Dict, Set

def collect_tasks(root_dir: str, agents: Set[str]) -> Dict[str, str]:
    """
    Parses all Python modules in the given directory and collects task-agent mappings.

    Args:
        root_dir (str): Path to the codebase directory
        agents (set[str]): Set of all known agent names

    Returns:
        dict[str, str]: A dictionary mapping task names to agent names
    """
    task_map: Dict[str, str] = {}

    # Helper to extract agent name from a decorator
    def _extract_agent(decorator: ast.AST) -> str | None:
        if isinstance(decorator, ast.Call):
            # Decorator is a call, e.g., @task(agent="foo")
            for kw in decorator.keywords:
                if kw.arg == "agent":
                    if isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                        return kw.value.value
        return None

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    source = f.read()
                tree = ast.parse(source, filename=file_path)
            except (SyntaxError, UnicodeDecodeError):
                # Skip files that can't be parsed
                continue

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    for deco in node.decorator_list:
                        agent_name = _extract_agent(deco)
                        if agent_name and agent_name in agents:
                            task_map[node.name] = agent_name
                            # Once found, no need to check other decorators for this node
                            break

    return task_map