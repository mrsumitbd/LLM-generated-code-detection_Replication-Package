from typing import Any, Callable, ForwardRef, List, Set
from pydantic._internal._typing_extra import eval_type_lenient as evaluate_forwardref
from ninja.types import DictStrAny

def make_forwardref(annotation: str, globalns: DictStrAny) -> Any:
    # NOTE: in future versions of pydantic, the import may be changed to:
    # from pydantic._internal._typing_extra import try_eval_type
    # usage:
    # result, _ = try_eval_type(forward_ref, globalns, globalns)
    forward_ref = ForwardRef(annotation)
    return evaluate_forwardref(forward_ref, globalns, globalns)