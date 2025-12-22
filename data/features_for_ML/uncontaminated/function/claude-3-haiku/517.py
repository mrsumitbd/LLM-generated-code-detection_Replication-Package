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
    tool_params = {param.name: param for param in params}
    unresolved_params = query.get_unresolved_parameters()

    for param in unresolved_params:
        if param not in tool_params:
            raise PlanError(f"Unresolved parameter '{param}' not found in tool parameters.")

    return UserDefinedTool(
        name=name,
        description=description,
        params=params,
        result_limit=result_limit,
        query=query
    )