from typing import Any

# Import the necessary classes and helper functions.
# These imports assume the surrounding package structure.
# Adjust the import paths if they differ in your project.
try:
    from .proto import JsonContainsExprProto
    from .serde_context import SerdeContext
    from .expr import JsonContainsExpr
    from .expr_deserializer import _deserialize_expr
except Exception:  # pragma: no cover
    # Fallback imports for environments where relative imports fail.
    from proto import JsonContainsExprProto
    from serde_context import SerdeContext
    from expr import JsonContainsExpr
    from expr_deserializer import _deserialize_expr


def _deserialize_json_contains_expr(
    logical_proto: JsonContainsExprProto, context: SerdeContext
) -> JsonContainsExpr:
    """
    Deserialize a JsonContainsExprProto into a JsonContainsExpr.

    The proto is expected to contain at least a `json_expr` field and a
    `key_expr` field.  An optional `value_expr` field may also be present.
    Each sub‑expression is deserialized using the provided context.

    Parameters
    ----------
    logical_proto : JsonContainsExprProto
        The protobuf representation of the expression.
    context : SerdeContext
        Context used for deserializing nested expressions.

    Returns
    -------
    JsonContainsExpr
        The deserialized expression object.
    """
    # Deserialize the JSON expression part.
    json_expr = _deserialize_expr(logical_proto.json_expr, context)

    # Deserialize the key expression part.
    key_expr = _deserialize_expr(logical_proto.key_expr, context)

    # Deserialize the optional value expression part, if present.
    value_expr: Any | None = None
    if getattr(logical_proto, "HasField", lambda f: False)("value_expr"):
        value_expr = _deserialize_expr(logical_proto.value_expr, context)

    # Construct and return the JsonContainsExpr instance.
    return JsonContainsExpr(json_expr, key_expr, value_expr)