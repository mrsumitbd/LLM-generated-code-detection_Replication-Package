def parse_all_graph_instances_in_directory(
    root_directory,
    graph_class_fqcn,
    command_class_fqn,
    add_conditional_edges_method_name,
    add_node_method_name,
    global_functions,
    global_variables,
):
    import os
    import ast
    import importlib.util
    
    graph_instances = []
    
    # Walk through all files in the directory
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                
                try:
                    # Read and parse the Python file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    tree = ast.parse(content)
                    
                    # Load the module to get runtime objects
                    spec = importlib.util.spec_from_file_location(
                        file.replace('.py', ''),
                        file_path
                    )
                    module = importlib.util.module_from_spec(spec)
                    
                    # Set global context
                    for name, obj in global_functions.items():
                        setattr(module, name, obj)
                    for name, obj in global_variables.items():
                        setattr(module, name, obj)
                    
                    spec.loader.exec_module(module)
                    
                    # Find graph instances in the AST
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Assign):
                            # Check if this is an assignment of graph_class_fqcn
                            if isinstance(node.value, ast.Call):
                                call_node = node.value
                                
                                # Get the class name being instantiated
                                class_name = None
                                if isinstance(call_node.func, ast.Name):
                                    class_name = call_node.func.id
                                elif isinstance(call_node.func, ast.Attribute):
                                    # Handle module.ClassName
                                    parts = []
                                    current = call_node.func
                                    while isinstance(current, ast.Attribute):
                                        parts.append(current.attr)
                                        current = current.value
                                    if isinstance(current, ast.Name):
                                        parts.append(current.id)
                                    class_name = '.'.join(reversed(parts))
                                
                                # Check if it matches the graph class
                                if class_name and (class_name.endswith(graph_class_fqcn.split('.')[-1]) or 
                                                   class_name == graph_class_fqcn):
                                    # Get variable names
                                    for target in node.targets:
                                        if isinstance(target, ast.Name):
                                            var_name = target.id
                                            
                                            # Try to get the actual object from the module
                                            if hasattr(module, var_name):
                                                graph_obj = getattr(module, var_name)
                                                graph_instances.append({
                                                    'file': file_path,
                                                    'variable_name': var_name,
                                                    'object': graph_obj,
                                                    'ast_node': node
                                                })
                
                except Exception as e:
                    # Skip files that can't be parsed or loaded
                    continue
    
    return graph_instances