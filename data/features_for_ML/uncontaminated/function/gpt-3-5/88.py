def module_checker(class_name: str) -> None:
    import importlib
    try:
        importlib.import_module(class_name)
        print(f"Plugin {class_name} is present.")
    except ModuleNotFoundError:
        print(f"Plugin {class_name} is missing. Please install the required plugin before running the ARES pipeline.")