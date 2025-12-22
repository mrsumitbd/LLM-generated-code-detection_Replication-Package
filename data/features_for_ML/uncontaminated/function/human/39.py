from .._validation import validate_axis
from typing import Any, Literal
import numpy as np
from numpy.typing import DTypeLike, NDArray
from .. import types
from ._is_constant import is_constant_

def is_constant(
    x: NDArray[Any] | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | NDArray[np.bool] | types.CupyArray | types.DaskArray:
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
    from ._is_constant import is_constant_

    validate_axis(x.ndim, axis)
    return is_constant_(x, axis=axis)