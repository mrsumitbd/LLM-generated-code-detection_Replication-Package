from typing import Annotated, Any, Literal, Optional, Union, get_args
import numpy as np

def python_to_array(
    val: Any, expected_shape: ShapeType, expected_dtype: Optional[str]
) -> ArrayLike:
    """Convert a Python object to a NumPy array."""
    val = np.asarray(val, order="C")
    if not np.issubdtype(val.dtype, np.number) and not np.issubdtype(
        val.dtype, np.bool_
    ):
        raise ValueError(
            f"Could not convert object to numeric NumPy array (got dtype: {val.dtype})"
        )
    return _coerce_shape_dtype(val, expected_shape, expected_dtype)