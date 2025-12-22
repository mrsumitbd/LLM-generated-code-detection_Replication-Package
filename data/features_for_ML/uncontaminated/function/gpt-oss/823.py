from typing import List, Dict
import re
import string

def _tokenize(text: str) -> List[str]:
    """Simple whitespace tokenizer that removes punctuation."""
    return [
        token.strip(string.punctuation)
        for token in text.split()
        if token.strip(string.punctuation)
    ]

def _truncate_to_tokens(text: str, max_tokens: int) -> str:
    tokens = _tokenize(text)
    if len(tokens) <= max_tokens:
        return text
    return " ".join(tokens[:max_tokens])

def build_search_index(messages: List[Dict], patterns: List[Dict], errors: List[Dict]) -> str:
    """
    Build 500-token search index optimized for keyword matching.

    Opus structure:
    - User request (exact words)
    - Solution type + tools used
    - Files modified + operation types
    - Primary keywords (3-5 specific terms)
    """
    # 1. User request
    user_request = ""
    for msg in messages:
        if msg.get("role") == "user":
            user_request = msg.get("content", "").strip()
            break

    # 2. Solution type + tools used
    solution_info = ""
    if patterns:
        # Assume first pattern contains 'type' and 'tools'
        pat = patterns[0]
        sol_type = pat.get("type", "")
        tools = pat.get("tools", [])
        if isinstance(tools, list):
            tools_str = ", ".join(tools)
        else:
            tools_str = str(tools)
        solution_info = f"{sol_type} using {tools_str}".strip()

    # 3. Files modified + operation types
    files_ops = []
    for err in errors:
        file_name = err.get("file") or err.get("filename") or ""
        operation = err.get("operation") or err.get("op") or ""
        if file_name and operation:
            files_ops.append(f"{file_name} ({operation})")
    files_ops_str = "; ".join(files_ops)

    # 4. Primary keywords (3-5 specific terms)
    # Simple heuristic: take first 5 non-stop words from user request
    stopwords = {
        "the", "and", "a", "an", "to", "in", "for", "of", "on", "with", "by",
        "is", "are", "was", "were", "be", "been", "has", "have", "it", "this",
        "that", "from", "as", "at", "or", "but", "if", "else", "when", "then",
        "so", "such", "into", "into", "out", "up", "down", "over", "under",
    }
    words = [
        w.strip(string.punctuation).lower()
        for w in user_request.split()
        if w.strip(string.punctuation).lower() not in stopwords
    ]
    primary_keywords = ", ".join(words[:5])

    # Assemble opus
    opus_parts = [
        f"User request: {user_request}",
        f"Solution: {solution_info}",
        f"Files modified: {files_ops_str}",
        f"Primary keywords: {primary_keywords}",
    ]
    opus = "\n".join(opus_parts)

    # Truncate to 500 tokens
    return _truncate_to_tokens(opus, 500)