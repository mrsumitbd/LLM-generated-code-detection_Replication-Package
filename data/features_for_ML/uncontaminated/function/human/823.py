from typing import Dict, List, Any, Tuple, Optional

def build_search_index(messages: List[Dict], patterns: List[Dict], errors: List[Dict]) -> str:
    """
    Build 500-token search index optimized for keyword matching.

    Opus structure:
    - User request (exact words)
    - Solution type + tools used
    - Files modified + operation types
    - Primary keywords (3-5 specific terms)
    """
    parts = []

    # Extract user requests (exclude tool_result noise AND meta commands)
    user_requests = []
    for i, msg in enumerate(messages):
        msg_data = get_message_data(msg)
        if msg_data.get("role") == "user":
            content = str(msg_data.get("content", ""))
            # Skip tool results, meta commands, and system messages
            if (len(content) > 50 and
                "tool_result" not in content and
                "tool_use_id" not in content and
                "<command-name>" not in content and
                "Caveat:" not in content and
                "<local-command" not in content):
                user_requests.append(content[:200])
                if len(user_requests) >= 2:  # Top 2 requests
                    break

    if user_requests:
        parts.append("## User Request")
        for req in user_requests:
            parts.append(req)
        parts.append("")

    # Edit patterns
    if patterns:
        parts.append("## Solution Pattern")
        for p in patterns[:3]:  # Top 3 patterns
            file_short = p["file"].split("/")[-1] if "/" in p["file"] else p["file"]
            parts.append(f"{p['operation_type']}: {file_short}")
            parts.append(f"  {p['pattern_description']}")
        parts.append("")

    # Unresolved errors only
    unresolved = [e for e in errors if not e.get("resolved", True)]
    if unresolved:
        parts.append("## Active Issues")
        for err in unresolved[:2]:
            parts.append(err["error_text"][:100])
        parts.append("")

    return "\n".join(parts)