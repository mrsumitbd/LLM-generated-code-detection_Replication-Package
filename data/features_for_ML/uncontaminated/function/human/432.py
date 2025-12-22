from fenic.core._logical_plan.expressions.json import (
    JqExpr,
    JsonContainsExpr,
    JsonTypeExpr,
)
from fenic.core._serde.proto.types import (
    JqExprProto,
    JsonContainsExprProto,
    JsonTypeExprProto,
    LogicalExprProto,
)
from fenic.core._serde.proto.serde_context import SerdeContext

def _deserialize_json_contains_expr(
    logical_proto: JsonContainsExprProto, context: SerdeContext
) -> JsonContainsExpr:
    return JsonContainsExpr(
        expr=context.deserialize_logical_expr(SerdeContext.EXPR, logical_proto.expr),
        value=logical_proto.value,
    )