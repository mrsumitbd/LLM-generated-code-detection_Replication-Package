import numpy as np
from typing import Any, Literal, Union
from numpy.typing import NDArray
import types

def is_constant_(
    a: NDArray[Any] | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | NDArray[np.bool] | types.CupyArray | types.DaskArray:
    if axis is None:
        return np.all(a == a.flat[0])
    else:
        return np.all(a == a.take(0, axis=axis), axis=axis)