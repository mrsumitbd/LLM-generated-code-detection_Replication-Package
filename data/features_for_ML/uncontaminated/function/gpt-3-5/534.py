def _handle_get(app: Any, args: List[str], manager: Any) -> None:
    profile_id = args[0]
    model = manager.get_model(profile_id)
    if model:
        print(model)
    else:
        print(f"Model for profile {profile_id} not found.")