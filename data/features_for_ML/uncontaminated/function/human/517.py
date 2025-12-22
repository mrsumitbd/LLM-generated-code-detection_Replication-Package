from collections import defaultdict
from fenic.core._logical_plan import walker
from fenic.core._logical_plan.expressions.basic import UnresolvedLiteralExpr
from fenic.core._logical_plan.plans.base import LogicalPlan
from fenic.core.error import PlanError
from fenic.core.mcp.types import (
    BoundToolParam,
    TableFormat,
    ToolParam,
    UserDefinedTool,
)

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
    unresolved_exprs: list[UnresolvedLiteralExpr] = [
        expr for expr in walker.find_expressions(query, lambda expr: isinstance(expr, UnresolvedLiteralExpr))
    ]

    unresolved_exprs_grouped = defaultdict(list)
    for expr in unresolved_exprs:
        unresolved_exprs_grouped[expr.parameter_name].append(expr)
    unresolved_exprs_by_name = {expr.parameter_name: expr for expr in unresolved_exprs}
    for _, unresolved_exprs in unresolved_exprs_grouped.items():
        if not all(unresolved_expr == unresolved_exprs[0] for unresolved_expr in unresolved_exprs):
            raise PlanError(
                "All unresolved expressions with the same parameter name must have the same configuration values"
            )

    params = {param.name: param for param in params}
    missing_params = unresolved_exprs_by_name.keys() - params.keys()
    if missing_params:
        raise PlanError(f"Tool does not have ToolParam(s) registered for the following placeholders: {missing_params}")
    extra_params = params.keys() - unresolved_exprs_by_name.keys()
    if extra_params:
        logger.warning(f"Extra parameters: {extra_params}")

    resolved_params: list[BoundToolParam] = []
    for unresolved_expr_name, unresolved_expr in unresolved_exprs_by_name.items():
        tool_param_model = params[unresolved_expr_name]
        # Validate allowed values if default present and non-None
        if (
            tool_param_model.allowed_values is not None
            and tool_param_model.has_default
            and tool_param_model.default_value is not None
        ):
            if tool_param_model.default_value not in tool_param_model.allowed_values:
                raise PlanError(
                    f"Default value {tool_param_model.default_value} is not in the allowed values {tool_param_model.allowed_values}"
                )
            # Ensure allowed values are homogeneous with the default's Python type
            if not all(isinstance(value, type(tool_param_model.default_value)) for value in tool_param_model.allowed_values):
                raise PlanError(
                    f"Allowed values {tool_param_model.allowed_values} must all be the same type as the default value {type(tool_param_model.default_value).__name__}"
                )

        resolved_params.append(
            BoundToolParam(
                name=tool_param_model.name,
                description=tool_param_model.description,
                data_type=unresolved_expr.data_type,
                required=tool_param_model.required,
                has_default=tool_param_model.has_default,
                default_value=tool_param_model.default_value,
                allowed_values=tool_param_model.allowed_values,
            )
        )

    return UserDefinedTool(
        name=name,
        description=description,
        params=resolved_params,
        _parameterized_view=query,
        max_result_limit=result_limit,
    )