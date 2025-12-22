from typing import Any, Dict, Mapping

def make_forwardref(annotation: str, globalns: Mapping[str, Any]) -> Any:
    try:
        result = eval(annotation, globalns, globalns)
    except (NameError, TypeError):
        result = ForwardRef(annotation)
    return result

class ForwardRef:
    def __init__(self, annotation: str):
        self.__forward_arg__ = annotation

    def __eq__(self, other):
        if isinstance(other, ForwardRef):
            return self.__forward_arg__ == other.__forward_arg__
        elif hasattr(other, '__forward_arg__'):
            return self.__forward_arg__ == other.__forward_arg__
        return False

    def __hash__(self):
        return hash(self.__forward_arg__)

    def __repr__(self):
        return f'ForwardRef({self.__forward_arg__!r})'