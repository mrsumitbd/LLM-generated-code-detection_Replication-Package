def make_forwardref(annotation: str, globalns: DictStrAny) -> Any:
    from typing import Any
    from pydantic.typing import ForwardRef
    from pydantic._types import DictStrAny
    from pydantic._internal._typing_extra import try_eval_type

    forward_ref = ForwardRef(annotation)
    result, _ = try_eval_type(forward_ref, globalns, globalns)
    return result