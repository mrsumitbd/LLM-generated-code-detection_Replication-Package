import json
from typing import Any

# Assume ActionType enum and CodeExecutionResult are defined in the same package.
# Import them; if they are in a different module, adjust the import accordingly.
try:
    from .action import ActionType
except Exception:
    try:
        from action import ActionType
    except Exception:
        # Fallback: define a minimal ActionType for parsing purposes
        from enum import Enum
        class ActionType(Enum):
            CONTINUE = "continue"
            STOP = "stop"
            ERROR = "error"

def _parse_action_content(content: str, result: Any, partial: bool = False) -> None:
    """
    Parses the content within action_response tags and populates the result object.

    Args:
        content (str): The content between <action_response> and </action_response> tags.
        result (CodeExecutionResult): The result object to populate.
        partial (bool): Whether this is a partial parse (incomplete action_response).

    Raises:
        ValueError: If an invalid ActionType is encountered.
    """
    # Strip surrounding whitespace
    content = content.strip()
    if not content:
        return

    # Try JSON first
    parsed: dict[str, Any] | None = None
    try:
        parsed = json.loads(content)
    except Exception:
        # Not JSON; fall back to simple key:value parsing
        parsed = {}
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, val = line.split(":", 1)
                parsed[key.strip().lower()] = val.strip()
            else:
                # If line has no colon, treat entire line as output
                parsed.setdefault("output", "")
                parsed["output"] += line + "\n"

    # Helper to set attribute if present
    def set_attr(attr: str, value: Any) -> None:
        if hasattr(result, attr):
            setattr(result, attr, value)

    # Process action_type
    if "action_type" in parsed:
        raw_type = parsed["action_type"]
        try:
            # Try to match enum by name or value
            if isinstance(raw_type, str):
                # First try by name (case-insensitive)
                try:
                    action = ActionType[raw_type.upper()]
                except KeyError:
                    # Then try by value
                    action = ActionType(raw_type.lower())
            else:
                action = ActionType(raw_type)
        except Exception:
            raise ValueError(f"Invalid ActionType: {raw_type}") from None
        set_attr("action_type", action)

    # Process output
    if "output" in parsed:
        set_attr("output", parsed["output"])

    # Process error
    if "error" in parsed:
        set_attr("error", parsed["error"])

    # If partial and missing action_type, we don't raise error
    if not partial and "action_type" not in parsed:
        raise ValueError("Missing action_type in action_response content")