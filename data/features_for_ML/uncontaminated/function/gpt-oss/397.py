from typing import Any, Optional, Tuple, Union

import numpy as np
from numpy.typing import ArrayLike

# ShapeType is assumed to be a tuple of ints or None values
ShapeType = Union[Tuple[Optional[int], ...], Tuple[int, ...]]


def python_to_array(
    val: Any, expected_shape: ShapeType, expected_dtype: Optional[str]
) -> ArrayLike:
    """Convert a Python object to a NumPy array and validate shape and dtype.

    Parameters
    ----------
    val : Any
        The input Python object to convert.
    expected_shape : ShapeType
        The expected shape of the resulting array. Each element can be an
        integer or ``None``. ``None`` means that dimension is flexible.
    expected_dtype : Optional[str]
        The expected NumPy dtype as a string (e.g., ``'float64'``). If
        ``None`` no dtype check is performed.

    Returns
    -------
    ArrayLike
        The converted NumPy array.

    Raises
    ------
    ValueError
        If the resulting array does not match the expected shape or dtype.
    """
    # Convert to a NumPy array (preserve dtype if already an array)
    arr = np.asarray(val)

    # Validate shape
    if expected_shape is not None:
        if len(arr.shape) != len(expected_shape):
            raise ValueError(
                f"Shape mismatch: expected {expected_shape}, got {arr.shape}"
            )
        for idx, (dim, exp_dim) in enumerate(zip(arr.shape, expected_shape)):
            if exp_dim is not None and dim != exp_dim:
                raise ValueError(
                    f"Shape mismatch at axis {idx}: expected {exp_dim}, got {dim}"
                )

    # Validate dtype
    if expected_dtype is not None:
        expected = np.dtype(expected_dtype)
        if arr.dtype != expected:
            raise ValueError(
                f"Dtype mismatch: expected {expected}, got {arr.dtype}"
            )

    return arr