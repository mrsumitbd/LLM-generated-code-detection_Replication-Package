def _transform_plan(node: LogicalPlan) -> None:
    # Transform expressions attached to this plan node
    if hasattr(node, 'expressions') and node.expressions:
        for i, expr in enumerate(node.expressions):
            if isinstance(expr, Expression):
                node.expressions[i] = _transform_expression(expr)
    
    # Recursively transform child nodes
    if hasattr(node, 'children') and node.children:
        for child in node.children:
            if isinstance(child, LogicalPlan):
                _transform_plan(child)
    
    # Handle specific plan node types with expression fields
    if hasattr(node, 'predicate') and node.predicate:
        if isinstance(node.predicate, Expression):
            node.predicate = _transform_expression(node.predicate)
    
    if hasattr(node, 'condition') and node.condition:
        if isinstance(node.condition, Expression):
            node.condition = _transform_expression(node.condition)
    
    if hasattr(node, 'join_condition') and node.join_condition:
        if isinstance(node.join_condition, Expression):
            node.join_condition = _transform_expression(node.join_condition)
    
    if hasattr(node, 'group_by') and node.group_by:
        for i, expr in enumerate(node.group_by):
            if isinstance(expr, Expression):
                node.group_by[i] = _transform_expression(expr)
    
    if hasattr(node, 'order_by') and node.order_by:
        for i, expr in enumerate(node.order_by):
            if isinstance(expr, Expression):
                node.order_by[i] = _transform_expression(expr)