from typing import Dict, List, Any, Set

def extract_semantic_patterns(text: str) -> Dict[str, Any]:
    """
    Main entry point for extracting semantic patterns from code.
    Returns structured pattern data suitable for Qdrant metadata.
    """
    registry = get_registry()

    # Extract patterns
    patterns = registry.extract_patterns(text)

    # Get high-level categories
    categories = registry.categorize_patterns(patterns)

    # Flatten for storage
    pattern_list = []
    for category, pattern_ids in patterns.items():
        for pattern_id in pattern_ids:
            pattern_list.append(f"{category}.{pattern_id}")

    return {
        "patterns": pattern_list[:50],  # Limit for storage
        "pattern_categories": list(categories.keys()),
        "has_patterns": len(pattern_list) > 0
    }