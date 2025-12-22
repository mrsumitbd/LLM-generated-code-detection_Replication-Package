from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .proto import EqualityComparisonExprProto, EqualityComparisonOperatorProto
    from .expr import EqualityComparisonExpr, EqualityComparisonOperator
    from .serde import SerdeContext

def _deserialize_equality_comparison_expr(
    logical_proto: "EqualityComparisonExprProto", context: "SerdeContext"
) -> "EqualityComparisonExpr":
    """
    Deserialize an equality comparison expression from its protobuf representation.

    Parameters
    ----------
    logical_proto : EqualityComparisonExprProto
        The protobuf message containing the serialized equality comparison expression.
    context : SerdeContext
        The serialization/deserialization context used to deserialize nested expressions.

    Returns
    -------
    EqualityComparisonExpr
        The deserialized equality comparison expression object.
    """
    # Deserialize the left and right operands recursively.
    left_expr = context.deserialize_expr(logical_proto.left_expr)
    right_expr = context.deserialize_expr(logical_proto.right_expr)

    # Map the protobuf operator enum to the internal enum.
    proto_op = logical_proto.operator
    if proto_op == "EQ":
        op = "EQ"
    elif proto_op == "NEQ":
        op = "NEQ"
    else:
        raise ValueError(f"Unsupported equality comparison operator: {proto_op}")

    # Construct and return the EqualityComparisonExpr instance.
    return EqualityComparisonExpr(left=left_expr, right=right_expr, operator=op)