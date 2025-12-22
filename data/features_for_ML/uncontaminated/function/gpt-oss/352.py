import json
from typing import Optional

# Assume PromptData is defined elsewhere in the module.
# If not, this import will fail and the function will not be usable.
try:
    from .prompt_data import PromptData  # Adjust import path as needed
except Exception:
    # Fallback: define a minimal PromptData for type checking purposes
    from dataclasses import dataclass

    @dataclass
    class PromptData:
        prompt: str
        completion: str
        # Add other fields if necessary

def _parse_jsonl_line(
    line: str,
    line_num: int,
    task_logger=None
) -> Optional[PromptData]:
    """
    Parse a single JSONL line into PromptData.

    Args:
        line: The JSONL line to parse
        line_num: Line number for error reporting
        task_logger: Optional logger for this task

    Returns:
        PromptData object or None if parsing fails
    """
    # Strip whitespace and ignore empty lines
    stripped = line.strip()
    if not stripped:
        return None

    try:
        data = json.loads(stripped)
    except json.JSONDecodeError as exc:
        if task_logger:
            task_logger.warning(
                f"Line {line_num}: JSON decode error: {exc.msg} (line {exc.lineno} col {exc.colno})"
            )
        return None

    if not isinstance(data, dict):
        if task_logger:
            task_logger.warning(
                f"Line {line_num}: Expected JSON object, got {type(data).__name__}"
            )
        return None

    try:
        # Attempt to create PromptData from the dict
        prompt_data = PromptData(**data)
    except TypeError as exc:
        # Missing required fields or unexpected fields
        if task_logger:
            task_logger.warning(
                f"Line {line_num}: Failed to instantiate PromptData: {exc}"
            )
        return None
    except Exception as exc:
        # Catch any other unexpected errors
        if task_logger:
            task_logger.warning(
                f"Line {line_num}: Unexpected error creating PromptData: {exc}"
            )
        return None

    return prompt_data