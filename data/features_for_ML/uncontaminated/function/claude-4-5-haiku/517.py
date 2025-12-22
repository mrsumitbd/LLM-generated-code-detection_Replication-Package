def bind_tool(
    name: str,
    description: str,
    params: list[ToolParam],
    result_limit: int,
    query: LogicalPlan
) -> UserDefinedTool:
    """Create a tool from a query and a set of parameters.

    Raises PlanError if the logical plan contains unresolved parameters that are not in the tool parameters.
    """
    # Extract parameter names from the tool parameters
    param_names = {param.name for param in params}
    
    # Find all unresolved parameters in the logical plan
    unresolved_params = set()
    
    def collect_unresolved(plan: LogicalPlan) -> None:
        """Recursively collect unresolved parameters from the plan."""
        if hasattr(plan, 'unresolved_params'):
            unresolved_params.update(plan.unresolved_params)
        
        # Check children if they exist
        if hasattr(plan, 'children'):
            for child in plan.children:
                collect_unresolved(child)
        elif hasattr(plan, 'child'):
            collect_unresolved(plan.child)
        elif hasattr(plan, 'left') and hasattr(plan, 'right'):
            collect_unresolved(plan.left)
            collect_unresolved(plan.right)
    
    collect_unresolved(query)
    
    # Check if there are any unresolved parameters not in tool parameters
    unresolved_not_in_params = unresolved_params - param_names
    if unresolved_not_in_params:
        from sqlglot.errors import PlanError
        raise PlanError(
            f"Unresolved parameters in query: {unresolved_not_in_params}"
        )
    
    # Create and return the UserDefinedTool
    return UserDefinedTool(
        name=name,
        description=description,
        params=params,
        result_limit=result_limit,
        query=query
    )