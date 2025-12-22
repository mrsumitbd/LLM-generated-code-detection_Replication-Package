def is_constant_(
    a: NDArray[Any] | types.CSBase | types.CupyArray | types.DaskArray,
    /,
    *,
    axis: Literal[0, 1] | None = None,
) -> bool | NDArray[np.bool] | types.CupyArray | types.DaskArray:
    if isinstance(a, types.CSBase):
        if axis is None:
            return bool(a.nnz <= 1)
        else:
            result = np.zeros(a.shape[1 - axis], dtype=bool)
            if axis == 0:
                for i in range(a.shape[1]):
                    col = a.getcol(i)
                    result[i] = col.nnz <= 1
            else:
                for i in range(a.shape[0]):
                    row = a.getrow(i)
                    result[i] = row.nnz <= 1
            return result
    
    if isinstance(a, types.CupyArray):
        import cupy as cp
        if axis is None:
            return cp.all(a == a.flat[0])
        else:
            return cp.all(a == cp.expand_dims(a.take([0], axis=axis), axis=axis), axis=axis)
    
    if isinstance(a, types.DaskArray):
        import dask.array as da
        if axis is None:
            first_elem = a.flat[0]
            return da.all(a == first_elem)
        else:
            first_slice = a.take([0], axis=axis)
            expanded = da.expand_dims(first_slice, axis=axis)
            return da.all(a == expanded, axis=axis)
    
    if axis is None:
        first_elem = a.flat[0]
        return bool(np.all(a == first_elem))
    else:
        first_slice = np.take(a, [0], axis=axis)
        expanded = np.expand_dims(first_slice, axis=axis)
        return np.all(a == expanded, axis=axis)