def _parse_action_content(content: str, result: CodeExecutionResult, partial: bool = False) -> None:
    start_tag = '<action_response>'
    end_tag = '</action_response>'
    
    if not partial and (not content.startswith(start_tag) or not content.endswith(end_tag)):
        raise ValueError("Invalid action_response content format")
    
    content = content[len(start_tag): -len(end_tag)] if not partial else content
    
    # Parse the content and populate the result object
    # Your parsing logic here

    pass