def disqualify_leafs(node: GradedTaskNode) -> GradedTaskNode:
    """
    Sets all leaf scores to 0 and explanations to 'Disqualified'.
    Should be separately followed by `update_all_grades` to propagate the changes.
    """
    if node.is_leaf():
        disqualified_node = node.set_score(0.0)
        disqualified_node = disqualified_node.set_explanation("Submission has been disqualified")
        return disqualified_node

    new_sub_tasks = [disqualify_leafs(child) for child in node.sub_tasks]
    return node.set_sub_tasks(new_sub_tasks)