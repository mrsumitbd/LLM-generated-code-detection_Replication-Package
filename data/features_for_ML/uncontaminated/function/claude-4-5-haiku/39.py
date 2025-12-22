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
    if isinstance(x, types.CSBase):
        x_array = x.toarray()
    else:
        x_array = x
    
    if axis is None:
        if isinstance(x_array, types.DaskArray):
            return (x_array == x_array.flatten()[0]).all().compute()
        else:
            return bool((x_array == x_array.flat[0]).all())
    else:
        if isinstance(x_array, types.DaskArray):
            return (x_array == x_array.take([0], axis=axis)) .all(axis=axis)
        else:
            indices = [slice(None)] * x_array.ndim
            indices[axis] = 0
            first_slice = x_array[tuple(indices)]
            if axis == 0:
                return (x_array == first_slice).all(axis=0)
            else:
                return (x_array == first_slice[:, None]).all(axis=1)