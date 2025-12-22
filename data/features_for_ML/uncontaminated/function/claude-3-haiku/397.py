import numpy as np
from typing import Any, Optional
from .types import ShapeType, ArrayLike

def python_to_array(
    val: Any, expected_shape: ShapeType, expected_dtype: Optional[str]
) -> ArrayLike:
    """Convert a Python object to a NumPy array."""
    if isinstance(val, (list, tuple, np.ndarray)):
        arr = np.array(val, dtype=expected_dtype)
        if expected_shape is not None:
            arr = np.reshape(arr, expected_shape)
        return arr
    elif isinstance(val, (int, float, bool)):
        return np.array([val], dtype=expected_dtype)
    else:
        raise TypeError(f"Cannot convert {type(val)} to a NumPy array.")