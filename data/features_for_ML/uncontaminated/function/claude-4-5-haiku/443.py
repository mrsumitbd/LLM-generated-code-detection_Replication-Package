def disqualify_leafs(node: GradedTaskNode) -> GradedTaskNode:
    """
    Sets all leaf scores to 0 and explanations to 'Disqualified'.
    Should be separately followed by `update_all_grades` to propagate the changes.
    """
    if not node.children:
        node.score = 0
        node.explanation = 'Disqualified'
    else:
        for child in node.children:
            disqualify_leafs(child)
    
    return node