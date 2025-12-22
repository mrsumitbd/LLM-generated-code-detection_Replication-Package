from __future__ import annotations

import types
from typing import Any, Literal

import numpy as np

# Import optional backends if available
try:
    import cupy as cp
except Exception:  # pragma: no cover
    cp = None

try:
    import dask.array as da
except Exception:  # pragma: no cover
    da = None

# The NDArray type hint is used only for static typing
try:
    from numpy.typing import NDArray
except Exception:  # pragma: no cover
    NDArray = Any


def _is_constant_numpy(a: np.ndarray, axis: Literal[0, 1] | None) -> np.ndarray | bool:
    """Check constancy for a NumPy array."""
    if axis is None:
        # All elements equal to the first element
        return np.all(a == a.flat[0])
    if axis == 0:
        # Check each column
        return np.all(a == a[0, :], axis=0)
    if axis == 1:
        # Check each row
        return np.all(a == a[:, 0], axis=1)
    raise ValueError("axis must be 0, 1, or None")


def _is_constant_cupy(a: Any, axis: Literal[0, 1] | None) -> Any:
    """Check constancy for a CuPy array."""
    if cp is None:
        raise RuntimeError("CuPy is not available")
    if axis is None:
        return cp.all(a == a.flat[0])
    if axis == 0:
        return cp.all(a == a[0, :], axis=0)
    if axis == 1:
        return cp.all(a == a[:, 0], axis=1)
    raise ValueError("axis must be 0, 1, or None")


def _is_constant_dask(a: Any, axis: Literal[0, 1] | None) -> Any:
    """Check constancy for a Dask array."""
    if da is None:
        raise RuntimeError("Dask is not available")
    if axis is None:
        return da.all(a == a.flat[0])
    if axis == 0:
        return da.all(a == a[0, :], axis=0)
    if axis == 1:
        return da.all(a == a[:, 0], axis=1)
    raise ValueError("axis must be 0, 1, or None")


def is_constant_(
    a: NDArray[Any] | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | NDArray[np.bool] | types.CupyArray | types.DaskArray:  # pragma: no cover
    """
    Return whether the array `a` is constant along the specified `axis`.

    Parameters
    ----------
    a : array-like
        Input array. Can be a NumPy array, a CSBase instance, a CuPy array,
        or a Dask array.
    axis : {0, 1, None}, optional
        Axis along which to check constancy. If ``None`` (default), the
        entire array must be constant. If ``0``, each column must be
        constant. If ``1``, each row must be constant.

    Returns
    -------
    bool or array of bools
        If ``axis`` is ``None``, a single boolean is returned. Otherwise,
        an array of booleans is returned, one per column (``axis=0``) or
        row (``axis=1``). The return type matches the backend of the
        input array.
    """
    # NumPy array
    if isinstance(a, np.ndarray):
        return _is_constant_numpy(a, axis)

    # CuPy array
    if cp is not None and isinstance(a, cp.ndarray):
        return _is_constant_cupy(a, axis)

    # Dask array
    if da is not None and isinstance(a, da.Array):
        return _is_constant_dask(a, axis)

    # CSBase (fallback to NumPy semantics)
    if isinstance(a, types.CSBase):
        # Convert to NumPy array for comparison
        arr = np.asarray(a)
        return _is_constant_numpy(arr, axis)

    # Fallback: try to convert to NumPy array
    try:
        arr = np.asarray(a)
        return _is_constant_numpy(arr, axis)
    except Exception as exc:  # pragma: no cover
        raise TypeError(f"Unsupported array type: {type(a)!r}") from exc