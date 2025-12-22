from typing import Any

def is_constant(
    x: NDArray[Any] | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | NDArray[np.bool] | types.CupyArray | types.DaskArray:
    
    import numpy as np
    import cupy as cp
    import dask.array as da
    
    def _is_constant(arr):
        return np.all(arr == arr.flat[0])
    
    if axis is None:
        return _is_constant(x)
    
    if isinstance(x, np.ndarray):
        x = np.asarray(x)
    elif isinstance(x, cp.ndarray):
        x = cp.asarray(x)
    elif isinstance(x, da.Array):
        x = x.compute()
    
    if axis == 0:
        return np.array([_is_constant(x[:, i]) for i in range(x.shape[1])])
    elif axis == 1:
        return np.array([_is_constant(x[i, :]) for i in range(x.shape[0])])
    else:
        raise ValueError("Invalid axis value. Please provide axis as 0, 1, or None.")