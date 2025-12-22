def _parse_action_content(content: str, result: CodeExecutionResult, partial: bool = False) -> None:
    """
    Parses the content within action_response tags and populates the result object.

    Args:
        content (str): The content between <action_response> and </action_response> tags.
        result (CodeExecutionResult): The result object to populate.
        partial (bool): Whether this is a partial parse (incomplete action_response).

    Raises:
        ValueError: If an invalid ActionType is encountered.
    """
    import re
    from enum import Enum
    
    # Parse action_type
    action_type_match = re.search(r'<action_type>(.*?)</action_type>', content, re.DOTALL)
    if action_type_match:
        action_type_str = action_type_match.group(1).strip()
        try:
            # Try to convert string to ActionType enum
            result.action_type = ActionType[action_type_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid ActionType: {action_type_str}")
    
    # Parse action_input
    action_input_match = re.search(r'<action_input>(.*?)</action_input>', content, re.DOTALL)
    if action_input_match:
        result.action_input = action_input_match.group(1).strip()
    
    # Parse action_output
    action_output_match = re.search(r'<action_output>(.*?)</action_output>', content, re.DOTALL)
    if action_output_match:
        result.action_output = action_output_match.group(1).strip()
    
    # Parse is_error
    is_error_match = re.search(r'<is_error>(.*?)</is_error>', content, re.DOTALL)
    if is_error_match:
        is_error_str = is_error_match.group(1).strip().lower()
        result.is_error = is_error_str in ('true', '1', 'yes')
    
    # Set partial flag
    result.partial = partial