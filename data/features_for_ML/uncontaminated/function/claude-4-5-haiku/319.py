def collect_tasks(root_dir: str, agents: set[str]) -> dict[str, str]:
    """Parses all Python modules in the given directory and collects task-agent mappings.

    Args:
        root_dir (str): Path to the codebase directory
        agents (set[str]): Set of all known agent names

    Returns:
        dict[str, str]: A dictionary mapping task names to agent names
    """
    import os
    import ast
    
    task_agent_mapping = {}
    
    # Walk through all files in the root directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # Only process Python files
            if filename.endswith('.py'):
                filepath = os.path.join(dirpath, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Parse the Python file
                    tree = ast.parse(content)
                    
                    # Look for function definitions and class definitions
                    for node in ast.walk(tree):
                        # Check for function definitions with decorators
                        if isinstance(node, ast.FunctionDef):
                            for decorator in node.decorator_list:
                                # Check if decorator references an agent
                                decorator_name = None
                                
                                if isinstance(decorator, ast.Name):
                                    decorator_name = decorator.id
                                elif isinstance(decorator, ast.Attribute):
                                    # Handle cases like module.agent_name
                                    if isinstance(decorator.value, ast.Name):
                                        decorator_name = decorator.attr
                                elif isinstance(decorator, ast.Call):
                                    # Handle decorator calls
                                    if isinstance(decorator.func, ast.Name):
                                        decorator_name = decorator.func.id
                                    elif isinstance(decorator.func, ast.Attribute):
                                        decorator_name = decorator.func.attr
                                
                                if decorator_name and decorator_name in agents:
                                    task_agent_mapping[node.name] = decorator_name
                        
                        # Check for class definitions with decorators
                        elif isinstance(node, ast.ClassDef):
                            for decorator in node.decorator_list:
                                decorator_name = None
                                
                                if isinstance(decorator, ast.Name):
                                    decorator_name = decorator.id
                                elif isinstance(decorator, ast.Attribute):
                                    if isinstance(decorator.value, ast.Name):
                                        decorator_name = decorator.attr
                                elif isinstance(decorator, ast.Call):
                                    if isinstance(decorator.func, ast.Name):
                                        decorator_name = decorator.func.id
                                    elif isinstance(decorator.func, ast.Attribute):
                                        decorator_name = decorator.func.attr
                                
                                if decorator_name and decorator_name in agents:
                                    task_agent_mapping[node.name] = decorator_name
                
                except (SyntaxError, UnicodeDecodeError, IOError):
                    # Skip files that can't be parsed
                    continue
    
    return task_agent_mapping