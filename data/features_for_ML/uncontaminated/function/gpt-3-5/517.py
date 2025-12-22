def bind_tool(name: str, description: str, params: list[ToolParam], result_limit: int, query: LogicalPlan) -> UserDefinedTool:
    unresolved_params = query.get_unresolved_params()
    for param in unresolved_params:
        if param not in params:
            raise PlanError(f"Unresolved parameter '{param}' not found in tool parameters")
    return UserDefinedTool(name, description, params, result_limit, query)