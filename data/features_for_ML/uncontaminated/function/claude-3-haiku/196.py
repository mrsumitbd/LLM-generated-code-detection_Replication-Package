def help():
    """
    Displays a list of available functions and their descriptions.
    
    Returns:
        None
    """
    import builtins
    
    print("Available functions:")
    for name, obj in vars(builtins).items():
        if callable(obj) and not name.startswith("_"):
            print(f"{name}(): {obj.__doc__ or 'No description available.'}")