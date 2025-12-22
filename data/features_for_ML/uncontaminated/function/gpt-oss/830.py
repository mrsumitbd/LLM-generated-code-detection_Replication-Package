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
    # Use the enum name for the error type tag
    error_tag = f"[{error_type.name}]"

    # Build component tag if provided
    if component:
        component_tag = f"[{component}] "
    else:
        component_tag = ""

    # Assemble the final message
    return f"{component_tag}{error_tag} {message}"