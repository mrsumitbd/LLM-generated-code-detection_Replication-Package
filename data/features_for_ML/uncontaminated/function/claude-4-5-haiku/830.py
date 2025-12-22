def create_error_message(
    error_type: ErrorType, message: str, component: str = ""
) -> str:
    """
    Creates a standardized error message with proper tagging.

    Format: [COMPONENT] [ERROR_TYPE] message

    Args:
        error_type: Type of error from ErrorType enum
        message: Detailed error message
        component: Component name (e.g., "PLANNER", "AGENT_REACT")

    Returns:
        Formatted error message string
    """
    parts = []
    
    if component:
        parts.append(f"[{component}]")
    
    parts.append(f"[{error_type.value}]")
    parts.append(message)
    
    return " ".join(parts)