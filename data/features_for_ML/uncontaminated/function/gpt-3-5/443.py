def disqualify_leafs(node: GradedTaskNode) -> GradedTaskNode:
    if not node.children:
        node.score = 0
        node.explanation = 'Disqualified'
    else:
        for child in node.children:
            disqualify_leafs(child)
    return node