def _transform_plan(node: LogicalPlan) -> None:
    # Transform expressions attached to this plan node
    for expr in node.expressions:
        expr.transform()

    # Transform child plan nodes
    for child in node.children:
        _transform_plan(child)