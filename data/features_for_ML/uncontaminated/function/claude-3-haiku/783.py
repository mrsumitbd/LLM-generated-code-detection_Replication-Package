def evaluate_name(
    name: ast.Name,
    state: Dict[str, Any],
    static_tools: Dict[str, Callable],
    custom_tools: Dict[str, Callable],
    authorized_imports: List[str],
) -> Any:
    if name.id in state:
        return state[name.id]
    elif name.id in static_tools:
        return static_tools[name.id]
    elif name.id in custom_tools:
        return custom_tools[name.id]
    elif name.id in authorized_imports:
        try:
            module = importlib.import_module(name.id)
            return module
        except ImportError:
            raise ValueError(f"Unauthorized import: {name.id}")
    else:
        raise NameError(f"Name '{name.id}' is not defined")