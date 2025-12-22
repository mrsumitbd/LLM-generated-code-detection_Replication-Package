from typing import Tuple, Any
from .models import Operation

def _find_collection_response(op: Operation) -> Tuple[int, Any]:
    """
    Walks through defined operation responses and finds the first
    that is of a collection type (e.g. List[SomeSchema])
    """
    for response_code, response in op.responses.items():
        if hasattr(response.content, '__origin__') and response.content.__origin__ == list:
            return response_code, response.content.__args__[0]
    return 200, None