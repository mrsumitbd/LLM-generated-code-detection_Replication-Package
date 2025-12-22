from typing import Any

# Try to import a real expression transformer if available.
# If not, fall back to an identity function.
try:
    from .expression import transform_expr  # type: ignore
except Exception:  # pragma: no cover
    def transform_expr(expr: Any) -> Any:  # noqa: D401
        """Identity fallback for expression transformation."""
        return expr


def _transform_plan(node: Any) -> None:
    """
    Recursively transform all expressions attached to a logical plan node.

    The function looks for common expression attributes (`expressions`,
    `exprs`, `expr`) on the node and applies `transform_expr` to each
    expression.  It then recurses into any child nodes found in a
    `children` attribute.

    Parameters
    ----------
    node : Any
        A logical plan node.  The function mutates the node in place.
    """
    # --- Transform expressions on this node --------------------------------
    expr_attrs = ("expressions", "exprs", "expr")
    for attr in expr_attrs:
        if hasattr(node, attr):
            value = getattr(node, attr)
            if isinstance(value, list):
                # Replace each expression in the list.
                setattr(node, attr, [transform_expr(e) for e in value])
            else:
                # Single expression.
                setattr(node, attr, transform_expr(value))

    # --- Recurse into child nodes ------------------------------------------
    if hasattr(node, "children"):
        for child in getattr(node, "children"):
            _transform_plan(child)