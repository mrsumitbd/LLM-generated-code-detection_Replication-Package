import numpy as np
from .. import types
from typing import Any, Literal, TypeVar
from numpy.typing import NDArray

def is_constant_(
    a: NDArray[Any] | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | NDArray[np.bool] | types.CupyArray | types.DaskArray:  # pragma: no cover
    raise NotImplementedError