def disqualify_leafs(node: GradedTaskNode) -> GradedTaskNode:
    """
    Sets all leaf scores to 0 and explanations to 'Disqualified'.
    Should be separately followed by `update_all_grades` to propagate the changes.
    """
    # Helper to determine if a node is a leaf
    def is_leaf(n):
        # If the node has a 'children' attribute and it's a non-empty iterable, it's not a leaf
        children = getattr(n, "children", None)
        if children is None:
            return True
        try:
            # Try to iterate over children
            return len(children) == 0
        except Exception:
            # If children is not a sequence, treat as leaf
            return True

    # Recursive traversal
    if is_leaf(node):
        # Set score to 0
        if hasattr(node, "score"):
            node.score = 0
        # Set explanation
        if hasattr(node, "explanation"):
            node.explanation = "Disqualified"
    else:
        # Recurse into children
        children = getattr(node, "children", [])
        for child in children:
            disqualify_leafs(child)

    return node