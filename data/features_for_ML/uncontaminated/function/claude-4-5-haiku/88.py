def module_checker(class_name: str) -> None:
    """
    Checks if required config plugins are present before running the ARES pipeline.

    This function verifies the presence of a specified plugin before proceeding with the ARES pipeline execution.

    :param class_name: The name of the plugin to check for.
    """
    import importlib
    import sys
    
    try:
        # Try to import the module/class
        parts = class_name.rsplit('.', 1)
        
        if len(parts) == 1:
            # It's just a class name, try to import from builtins or current namespace
            if class_name not in dir(__builtins__):
                raise ImportError(f"Plugin '{class_name}' not found")
        else:
            # It's a module path with class name
            module_name, class_attr = parts
            try:
                module = importlib.import_module(module_name)
                if not hasattr(module, class_attr):
                    raise ImportError(f"Plugin '{class_name}' not found in module '{module_name}'")
            except ImportError as e:
                raise ImportError(f"Cannot import plugin '{class_name}': {str(e)}")
    
    except ImportError as e:
        print(f"Error: Required plugin '{class_name}' is not available. {str(e)}")
        sys.exit(1)