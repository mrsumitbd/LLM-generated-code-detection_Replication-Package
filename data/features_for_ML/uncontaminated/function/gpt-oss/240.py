from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import the concrete expression classes only for type checking.
    from .expr import (
        ArithmeticExpr,
        ConstantExpr,
        VariableExpr,
        BinaryExpr,
        UnaryExpr,
    )
    from .proto import ArithmeticExprProto
    from .serde import SerdeContext


def _deserialize_arithmetic_expr(
    logical_proto: "ArithmeticExprProto", context: "SerdeContext"
) -> "ArithmeticExpr":
    """
    Deserialize an arithmetic expression from its protobuf representation.

    The protobuf is expected to have one of the following fields set:
        * `value`      – a numeric constant
        * `variable`   – a variable name
        * `op`         – a binary operator with `left` and `right` sub‑expressions
        * `unary_op`   – a unary operator with an `operand` sub‑expression

    The function recursively deserializes sub‑expressions and constructs the
    corresponding concrete expression objects.
    """
    # Constant expression
    if getattr(logical_proto, "HasField", lambda f: False)("value"):
        return ConstantExpr(logical_proto.value)

    # Variable expression
    if getattr(logical_proto, "HasField", lambda f: False)("variable"):
        return VariableExpr(logical_proto.variable)

    # Binary expression
    if getattr(logical_proto, "HasField", lambda f: False)("op"):
        left = _deserialize_arithmetic_expr(logical_proto.left, context)
        right = _deserialize_arithmetic_expr(logical_proto.right, context)
        return BinaryExpr(logical_proto.op, left, right)

    # Unary expression
    if getattr(logical_proto, "HasField", lambda f: False)("unary_op"):
        operand = _deserialize_arithmetic_expr(logical_proto.operand, context)
        return UnaryExpr(logical_proto.unary_op, operand)

    raise ValueError(
        f"Unsupported arithmetic expression proto: {logical_proto!r}"
    )