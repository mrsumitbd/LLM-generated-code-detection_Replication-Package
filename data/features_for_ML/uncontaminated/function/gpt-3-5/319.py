def collect_tasks(root_dir: str, agents: set[str]) -> dict[str, str]:
    import os
    import ast

    task_agent_mapping = {}

    def extract_task_agent_from_file(file_path):
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Call) and decorator.func.id == 'task' and decorator.args:
                            task_name = node.name
                            for arg in decorator.args:
                                if isinstance(arg, ast.Str):
                                    agent_name = arg.s
                                    if agent_name in agents:
                                        task_agent_mapping[task_name] = agent_name

    for root, _, files in os.walk(root_dir):
        for file_name in files:
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                extract_task_agent_from_file(file_path)

    return task_agent_mapping