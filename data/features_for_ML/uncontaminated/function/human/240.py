from fenic._gen.protos.logical_plan.v1.enums_pb2 import Operator as OperatorProto
from fenic.core._logical_plan.expressions.base import Operator
from fenic.core._logical_plan.expressions.arithmetic import ArithmeticExpr
from fenic.core._serde.proto.serde_context import SerdeContext
from fenic.core._serde.proto.types import (
    ArithmeticExprProto,
    BooleanExprProto,
    EqualityComparisonExprProto,
    LogicalExprProto,
    NumericComparisonExprProto,
)

def _deserialize_arithmetic_expr(
    logical_proto: ArithmeticExprProto, context: SerdeContext
) -> ArithmeticExpr:
    """Deserialize an arithmetic expression."""
    return ArithmeticExpr(
        left=context.deserialize_logical_expr(SerdeContext.LEFT, logical_proto.left),
        right=context.deserialize_logical_expr(SerdeContext.RIGHT, logical_proto.right),
        op=context.deserialize_enum_value("operator", Operator, OperatorProto, logical_proto.operator),
    )