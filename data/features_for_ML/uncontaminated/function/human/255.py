from fenic.core._logical_plan.expressions.text import (
    ArrayJoinExpr,
    ByteLengthExpr,
    ChunkCharacterSet,
    ChunkLengthFunction,
    ConcatExpr,
    ContainsAnyExpr,
    ContainsExpr,
    CountTokensExpr,
    EndsWithExpr,
    FuzzyRatioExpr,
    FuzzyTokenSetRatioExpr,
    FuzzyTokenSortRatioExpr,
    ILikeExpr,
    JinjaExpr,
    LikeExpr,
    RecursiveTextChunkExpr,
    RecursiveTextChunkExprConfiguration,
    RegexpSplitExpr,
    ReplaceExpr,
    RLikeExpr,
    SplitPartExpr,
    StartsWithExpr,
    StringCasingExpr,
    StripCharsExpr,
    StrLengthExpr,
    TextChunkExpr,
    TextChunkExprConfiguration,
    TextractExpr,
    TsParseExpr,
)
from fenic.core._serde.proto.serde_context import SerdeContext
from fenic.core._serde.proto.types import (
    ArrayJoinExprProto,
    ByteLengthExprProto,
    ChunkCharacterSetProto,
    ChunkLengthFunctionProto,
    ConcatExprProto,
    ContainsAnyExprProto,
    ContainsExprProto,
    CountTokensExprProto,
    EndsWithExprProto,
    FuzzyRatioExprProto,
    FuzzySimilarityMethodProto,
    FuzzyTokenSetRatioExprProto,
    FuzzyTokenSortRatioExprProto,
    ILikeExprProto,
    JinjaExprProto,
    LikeExprProto,
    LogicalExprProto,
    RecursiveTextChunkExprProto,
    RegexpSplitExprProto,
    ReplaceExprProto,
    RLikeExprProto,
    SplitPartExprProto,
    StartsWithExprProto,
    StringCasingExprProto,
    StripCharsExprProto,
    StrLengthExprProto,
    TextChunkExprProto,
    TextractExprProto,
    TsParseExprProto,
)

def _serialize_split_part_expr(
    logical: SplitPartExpr, context: SerdeContext
) -> LogicalExprProto:
    """Serialize a split part expression."""
    return LogicalExprProto(
        split_part=SplitPartExprProto(
            expr=context.serialize_logical_expr("expr", logical.expr),
            delimiter=context.serialize_logical_expr("delimiter", logical.delimiter),
            part_number=context.serialize_logical_expr(
                "part_number", logical.part_number
            ),
        )
    )