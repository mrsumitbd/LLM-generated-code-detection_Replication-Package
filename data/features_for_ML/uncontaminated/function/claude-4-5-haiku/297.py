def make_forwardref(annotation: str, globalns: DictStrAny) -> Any:
    from typing import ForwardRef
    
    forward_ref = ForwardRef(annotation, is_argument=False)
    try:
        return forward_ref._evaluate(globalns, globalns, frozenset())
    except (NameError, AttributeError):
        return forward_ref