def _parse_jsonl_line(
    line: str, line_num: int, task_logger=None
) -> Optional[PromptData]:
    """Parse a single JSONL line into PromptData.

    Args:
        line: The JSONL line to parse
        line_num: Line number for error reporting
        task_logger: Optional logger for this task

    Returns:
        PromptData object or None if parsing fails
    """
    import json
    
    # Strip whitespace
    line = line.strip()
    
    # Skip empty lines
    if not line:
        return None
    
    try:
        # Parse JSON
        data = json.loads(line)
        
        # Validate required fields
        if not isinstance(data, dict):
            if task_logger:
                task_logger.warning(f"Line {line_num}: Expected JSON object, got {type(data).__name__}")
            return None
        
        # Extract fields - adjust based on PromptData structure
        # Common fields in prompt data: prompt, completion, instruction, etc.
        prompt = data.get("prompt")
        completion = data.get("completion")
        
        if prompt is None:
            if task_logger:
                task_logger.warning(f"Line {line_num}: Missing 'prompt' field")
            return None
        
        # Create PromptData object
        prompt_data = PromptData(
            prompt=str(prompt),
            completion=str(completion) if completion is not None else None
        )
        
        return prompt_data
        
    except json.JSONDecodeError as e:
        if task_logger:
            task_logger.warning(f"Line {line_num}: Invalid JSON - {str(e)}")
        return None
    except Exception as e:
        if task_logger:
            task_logger.warning(f"Line {line_num}: Error parsing line - {str(e)}")
        return None