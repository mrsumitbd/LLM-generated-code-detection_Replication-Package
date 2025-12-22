def evaluate_name(
    name: ast.Name,
    state: Dict[str, Any],
    static_tools: Dict[str, Callable],
    custom_tools: Dict[str, Callable],
    authorized_imports: List[str],
) -> Any:
    var_name = name.id
    
    if var_name in state:
        return state[var_name]
    
    if var_name in static_tools:
        return static_tools[var_name]
    
    if var_name in custom_tools:
        return custom_tools[var_name]
    
    if var_name in __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__):
        builtins_dict = __builtins__ if isinstance(__builtins__, dict) else vars(__builtins__)
        return builtins_dict[var_name]
    
    raise NameError(f"name '{var_name}' is not defined")