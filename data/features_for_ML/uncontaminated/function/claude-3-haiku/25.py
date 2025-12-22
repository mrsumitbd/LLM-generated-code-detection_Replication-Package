import json
from typing import Dict, Any

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
    try:
        action_data = json.loads(content)
        action_type = action_data.get("type")

        if action_type == "display":
            result.display_content = action_data.get("content", "")
        elif action_type == "result":
            result.result = action_data.get("content", "")
        elif action_type == "error":
            result.error = action_data.get("content", "")
        elif action_type == "partial":
            result.partial_response = action_data.get("content", "")
        else:
            raise ValueError(f"Invalid ActionType: {action_type}")

        result.is_complete = not partial
    except (ValueError, KeyError):
        # Handle any errors during parsing
        result.error = "Error parsing action content"
        result.is_complete = not partial