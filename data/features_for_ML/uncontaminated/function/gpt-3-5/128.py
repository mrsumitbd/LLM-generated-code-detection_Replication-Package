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
    import importlib

    def load_module(module_name):
        return importlib.import_module(module_name)

    def get_class_from_fqcn(fqcn):
        parts = fqcn.split('.')
        module_name = '.'.join(parts[:-1])
        class_name = parts[-1]
        module = load_module(module_name)
        return getattr(module, class_name)

    def parse_graph_instance(graph_instance_path):
        graph_class = get_class_from_fqcn(graph_class_fqcn)
        command_class = get_class_from_fqcn(command_class_fqn)
        graph_instance = graph_class()
        command_instance = command_class()
        for function_name in global_functions:
            setattr(command_instance, function_name, globals()[function_name])
        for variable_name in global_variables:
            setattr(command_instance, variable_name, globals()[variable_name])
        add_conditional_edges_method = getattr(graph_instance, add_conditional_edges_method_name)
        add_node_method = getattr(graph_instance, add_node_method_name)
        with open(graph_instance_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('add_conditional_edges'):
                    add_conditional_edges_method(*line.split()[1:])
                elif line.startswith('add_node'):
                    add_node_method(*line.split()[1:])
        return graph_instance

    graph_instances = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.txt'):
                graph_instance_path = os.path.join(root, file)
                graph_instance = parse_graph_instance(graph_instance_path)
                graph_instances.append(graph_instance)

    return graph_instances