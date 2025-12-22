def _get_function_output_type(function: Function, tool_execution_config: dict[str, ToolExecutionConfig]) -> type:
    """Get the output type of a function based on its return annotation."""
    import inspect
    from typing import get_type_hints
    
    # Try to get type hints from the function
    try:
        type_hints = get_type_hints(function)
        if 'return' in type_hints:
            return type_hints['return']
    except Exception:
        pass
    
    # Fall back to inspecting the function signature
    sig = inspect.signature(function)
    if sig.return_annotation != inspect.Signature.empty:
        return sig.return_annotation
    
    # Default to Any if no return type is specified
    from typing import Any
    return Any