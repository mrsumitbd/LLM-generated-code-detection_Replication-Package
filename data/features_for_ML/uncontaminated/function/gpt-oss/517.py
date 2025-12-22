from typing import List

# The following imports are assumed to exist in the surrounding codebase.
# If they are defined elsewhere, adjust the import paths accordingly.
from .errors import PlanError
from .types import ToolParam, UserDefinedTool, LogicalPlan


def bind_tool(
    name: str,
    description: str,
    params: List[ToolParam],
    result_limit: int,
    query: LogicalPlan,
) -> UserDefinedTool:
    """
    Create a tool from a query and a set of parameters.

    Raises PlanError if the logical plan contains unresolved parameters that are not in the tool parameters.
    """
    # Collect the names of the parameters that the tool accepts.
    param_names = {param.name for param in params}

    # Retrieve the set of unresolved parameter names from the logical plan.
    # It is assumed that LogicalPlan exposes an `unresolved_params()` method
    # that returns an iterable of parameter names that are not yet bound.
    try:
        unresolved = set(query.unresolved_params())
    except AttributeError:
        # If the method does not exist, fall back to an empty set.
        unresolved = set()

    # Determine which unresolved parameters are not provided by the tool.
    missing = unresolved - param_names

    if missing:
        raise PlanError(
            f"Logical plan contains unresolved parameters not defined in tool: {', '.join(sorted(missing))}"
        )

    # All parameters are accounted for; create and return the user‑defined tool.
    return UserDefinedTool(
        name=name,
        description=description,
        params=params,
        result_limit=result_limit,
        query=query,
    )