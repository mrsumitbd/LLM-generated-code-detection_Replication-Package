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
    component_tag = f"[{component}] " if component else ""
    return f"{component_tag}[{error_type.value}] {message}"