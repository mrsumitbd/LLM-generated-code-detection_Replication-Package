from __future__ import annotations

import numpy as np
import types
from typing import Any, Literal

def is_constant(
    x: np.ndarray | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | np.ndarray | types.CupyArray | types.DaskArray:
    """Check whether values in array are constant.

    Parameters
    ----------
    x
        Array to check.
    axis
        Axis to reduce over.

    Returns
    -------
    If ``axis`` is :data:`None`, return if all values were constant.
    Else returns a boolean array with :data:`True` representing constant columns/rows.

    Example
    -------
    >>> import numpy as np
    >>> x = np.array([
    ...     [0, 1, 2],
    ...     [0, 0, 0],
    ... ])
    >>> is_constant(x)
    False
    >>> is_constant(x, axis=0)
    array([ True, False, False])
    >>> is_constant(x, axis=1)
    array([False,  True])

    """
    # Helper to get the array in the right backend
    def _to_backend(arr):
        if isinstance(arr, types.CSBase):
            # Convert sparse to dense
            return arr.toarray()
        return arr

    # Determine backend
    if isinstance(x, types.CSBase):
        backend = "sparse"
    elif isinstance(x, types.CupyArray):
        backend = "cupy"
    elif isinstance(x, types.DaskArray):
        backend = "dask"
    else:
        backend = "numpy"

    # Convert to appropriate array
    arr = _to_backend(x)

    # Handle empty arrays
    if arr.size == 0:
        if axis is None:
            return True
        else:
            # Return an array of True with shape along the other axis
            shape = arr.shape[1 - axis] if axis is not None else 0
            if backend == "numpy":
                return np.ones(shape, dtype=bool)
            elif backend == "cupy":
                import cupy as cp
                return cp.ones(shape, dtype=bool)
            else:  # dask
                import dask.array as da
                return da.ones(shape, dtype=bool)

    # Build reference for comparison
    if axis is None:
        # Compare all elements to the first element
        if backend == "numpy":
            ref = arr.flat[0]
            return np.all(arr == ref)
        elif backend == "cupy":
            import cupy as cp
            ref = arr.flat[0]
            return cp.all(arr == ref)
        else:  # dask
            import dask.array as da
            ref = arr.flat[0]
            return da.all(arr == ref).compute()
    else:
        # Compare along the specified axis
        if backend == "numpy":
            if axis == 0:
                ref = arr[0, :]
                return np.all(arr == ref, axis=0)
            else:  # axis == 1
                ref = arr[:, 0][:, None]
                return np.all(arr == ref, axis=1)
        elif backend == "cupy":
            import cupy as cp
            if axis == 0:
                ref = arr[0, :]
                return cp.all(arr == ref, axis=0)
            else:
                ref = arr[:, 0][:, None]
                return cp.all(arr == ref, axis=1)
        else:  # dask
            import dask.array as da
            if axis == 0:
                ref = arr[0, :]
                return da.all(arr == ref, axis=0)
            else:
                ref = arr[:, 0][:, None]
                return da.all(arr == ref, axis=1)