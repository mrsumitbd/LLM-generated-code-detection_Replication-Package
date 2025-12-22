import os
import importlib.util
import sys
from types import ModuleType
from typing import Any, Dict, List, Tuple


def _load_module_from_path(module_name: str, file_path: str) -> ModuleType:
    """Load a module from a given file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _find_class_in_module(module: ModuleType, class_name: str):
    """Return the class object with the given name from the module, or None."""
    return getattr(module, class_name, None)


def parse_all_graph_instances_in_directory(
    root_directory: str,
    graph_class_fqcn: str,
    command_class_fqn: str,
    add_conditional_edges_method_name: str,
    add_node_method_name: str,
    global_functions: Dict[str, Any],
    global_variables: Dict[str, Any],
) -> List[Any]:
    """
    Walk through all Python files in `root_directory`, import them, and instantiate
    objects of the class specified by `graph_class_fqcn`.  The function will call
    the methods named by `add_node_method_name` and
    `add_conditional_edges_method_name` on each instance if they exist.

    Parameters
    ----------
    root_directory : str
        Directory to search for Python files.
    graph_class_fqcn : str
        Fully qualified class name of the graph class (e.g. "mypkg.mymodule.MyGraph").
    command_class_fqn : str
        Fully qualified class name of a command class (unused in this implementation).
    add_conditional_edges_method_name : str
        Name of the method to add conditional edges.
    add_node_method_name : str
        Name of the method to add nodes.
    global_functions : dict
        Mapping of function names to callables to be injected into the module's globals.
    global_variables : dict
        Mapping of variable names to values to be injected into the module's globals.

    Returns
    -------
    List[Any]
        List of instantiated graph objects.
    """
    # Extract the class name from the fully qualified name
    if "." in graph_class_fqcn:
        graph_class_name = graph_class_fqcn.split(".")[-1]
    else:
        graph_class_name = graph_class_fqcn

    graph_instances: List[Any] = []

    # Walk through the directory tree
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            file_path = os.path.join(dirpath, filename)

            # Create a unique module name based on the file path
            rel_path = os.path.relpath(file_path, root_directory)
            module_name = rel_path.replace(os.sep, "_").rstrip(".py")

            try:
                module = _load_module_from_path(module_name, file_path)
            except Exception:
                # Skip files that cannot be imported
                continue

            # Inject global functions and variables into the module's globals
            module_globals = module.__dict__
            module_globals.update(global_functions)
            module_globals.update(global_variables)

            # Find the graph class in the module
            cls = _find_class_in_module(module, graph_class_name)
            if cls is None:
                continue

            # Instantiate the graph
            try:
                graph_instance = cls()
            except Exception:
                continue

            # Call add_node_method_name if it exists
            add_node_method = getattr(graph_instance, add_node_method_name, None)
            if callable(add_node_method):
                try:
                    add_node_method()
                except Exception:
                    pass

            # Call add_conditional_edges_method_name if it exists
            add_conditional_method = getattr(
                graph_instance, add_conditional_edges_method_name, None
            )
            if callable(add_conditional_method):
                try:
                    add_conditional_method()
                except Exception:
                    pass

            graph_instances.append(graph_instance)

    return graph_instances