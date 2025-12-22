def list_providers() -> List[Dict[str, Any]]:
    providers = [
        {'name': 'Provider1', 'is_default': True},
        {'name': 'Provider2', 'is_default': False},
        {'name': 'Provider3', 'is_default': False}
    ]
    return providers