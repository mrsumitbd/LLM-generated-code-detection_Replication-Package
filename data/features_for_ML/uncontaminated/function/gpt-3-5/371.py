def _transform_plan(node: LogicalPlan) -> None:
    # Transform expressions attached to this plan node
    if node is None:
        return
    for child in node.children:
        _transform_plan(child)
    if node.expressions:
        for expression in node.expressions:
            # Perform transformation on the expression here
            pass