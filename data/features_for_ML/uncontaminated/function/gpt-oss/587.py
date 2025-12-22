from typing import List, Dict, Any

def check_analysis_performed(messages: List[Dict[str, Any]], lookback: int = 15) -> bool:
    """
    Check if any analysis tools were used in recent messages.

    Args:
        messages: List of conversation messages
        lookback: Number of recent messages to check

    Returns:
        True if analysis tools were used (read, ls, analyze_ml_performance)
    """
    # Tools we consider as analysis tools
    analysis_tools = {"read", "ls", "analyze_ml_performance"}

    # Only look at the last `lookback` messages
    recent_msgs = messages[-lookback:]

    for msg in recent_msgs:
        # Check for tool calls (OpenAI chat format)
        tool_calls = msg.get("tool_calls") or msg.get("function_calls") or msg.get("functions")
        if tool_calls:
            for call in tool_calls:
                # Some APIs use 'name', others 'function', 'name'
                name = None
                if isinstance(call, dict):
                    name = call.get("name") or call.get("function") or call.get("name")
                if name in analysis_tools:
                    return True

        # Fallback: check content for tool invocation patterns
        content = msg.get("content", "")
        if isinstance(content, str):
            for tool in analysis_tools:
                # Simple pattern: tool(...)
                if f"{tool}(" in content:
                    return True

    return False