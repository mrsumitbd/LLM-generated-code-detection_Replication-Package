import os
import importlib

def parse_all_graph_instances_in_directory(
    root_directory,
    graph_class_fqcn,
    command_class_fqn,
    add_conditional_edges_method_name,
    add_node_method_name,
    global_functions,
    global_variables,
):
    graph_instances = []
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.py'):
                file_path = os.path.join(dirpath, filename)
                module_name = os.path.splitext(os.path.basename(file_path))[0]
                module = importlib.import_module(f'{os.path.relpath(dirpath, root_directory).replace(os.path.sep, ".")}.{module_name}')
                graph_class = getattr(module, graph_class_fqcn.split('.')[-1])
                command_class = getattr(module, command_class_fqn.split('.')[-1])
                add_conditional_edges_method = getattr(graph_class, add_conditional_edges_method_name)
                add_node_method = getattr(graph_class, add_node_method_name)

                for global_function in global_functions:
                    setattr(module, global_function.__name__, global_function)

                for global_variable, value in global_variables.items():
                    setattr(module, global_variable, value)

                graph_instance = graph_class()
                graph_instances.append(graph_instance)

    return graph_instances