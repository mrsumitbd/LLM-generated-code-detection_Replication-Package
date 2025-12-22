def is_constant(
    x: NDArray[Any] | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | NDArray[np.bool] | types.CupyArray | types.DaskArray:
    if axis is None:
        return np.all(x == x[0])
    else:
        return np.all(x == x[:, 0], axis=axis) if axis == 1 else np.all(x == x[0, :], axis=axis)