def _handle_get(app: Any, args: List[str], manager: Any) -> None:
    # Get model for a specific profile
    if not args:
        print("Error: profile name required")
        return
    
    profile_name = args[0]
    
    try:
        model = manager.get(profile_name)
        if model is None:
            print(f"Error: profile '{profile_name}' not found")
        else:
            print(model)
    except Exception as e:
        print(f"Error: {e}")