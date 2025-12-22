from typing import Any, AsyncGenerator, Callable, List, Optional, Tuple, Type, Union
from typing_extensions import get_args as get_collection_args
from ninja.constants import NOT_SET
from ninja.signature.details import is_collection_type
from ninja.errors import ConfigError
from ninja.operation import Operation

def _find_collection_response(op: Operation) -> Tuple[int, Any]:
    """
    Walks through defined operation responses and finds the first
    that is of a collection type (e.g. List[SomeSchema])
    """
    for code, resp_model in op.response_models.items():
        if resp_model is None or resp_model is NOT_SET:
            continue

        model = resp_model.__annotations__["response"]
        if is_collection_type(model):
            item_schema = get_collection_args(model)[0]
            return code, item_schema

    raise ConfigError(
        f'"{op.view_func}" has no collection response (e.g. response=List[SomeSchema])'
    )