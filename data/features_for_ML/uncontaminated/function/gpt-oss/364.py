from typing import Any, Tuple, get_origin, get_args
from collections.abc import Sequence

def _find_collection_response(op: "Operation") -> Tuple[int, Any]:
    """
    Walks through defined operation responses and finds the first
    that is of a collection type (e.g. List[SomeSchema])
    """
    # Helper to determine if a schema represents a collection
    def _is_collection(schema: Any) -> bool:
        # OpenAPI schema dict
        if isinstance(schema, dict):
            if schema.get("type") == "array":
                return True
            # Some libraries use "items" to indicate array
            if "items" in schema:
                return True
        # Typing constructs
        origin = get_origin(schema)
        if origin in (list, List, Sequence, tuple, set, frozenset):
            return True
        # Some libraries use typing.List alias
        if getattr(schema, "__origin__", None) in (list, List, Sequence, tuple, set, frozenset):
            return True
        return False

    # Iterate over responses sorted by status code (numeric if possible)
    try:
        sorted_codes = sorted(
            op.responses.keys(),
            key=lambda c: int(c) if isinstance(c, (str, int)) and str(c).isdigit() else c,
        )
    except Exception:
        sorted_codes = list(op.responses.keys())

    for code in sorted_codes:
        resp = op.responses.get(code)
        if not resp:
            continue
        # Response may have content mapping media types to media objects
        content = getattr(resp, "content", {})
        if not content:
            continue
        for media_type in content.values():
            schema = getattr(media_type, "schema", None)
            if schema is None:
                continue
            if _is_collection(schema):
                return int(code), schema
    # If no collection found, return None or raise
    raise ValueError("No collection response found in operation")