from typing import Callable, Optional

def get_activation_function(activation_function: str, inverse=False) -> Callable:
    if not inverse:
        return ACTIVATION_DICT[activation_function]
    else:
        return INVERSE_ACTIVATION_DICT[activation_function]