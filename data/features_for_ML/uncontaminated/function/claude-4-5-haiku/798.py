def rot90(
    m: Union[jax.typing.ArrayLike, Quantity],
    k: int = 1,
    axes: Tuple[int, int] = (0, 1)
) -> Union[
    jax.Array, Quantity]:
    """
    Rotate an array by 90 degrees in the plane specified by axes.

    Rotation direction is from the first towards the second axis.

    Parameters
    ----------
    m : array_like, Quantity
      Array of two or more dimensions.
    k : integer
      Number of times the array is rotated by 90 degrees.
    axes : (2,) array_like
      The array is rotated in the plane defined by the axes.
      Axes must be different.

    Returns
    -------
    y : ndarray, Quantity
      A rotated view of `m`.

      This is a quantity if `m` is a quantity.
    """
    is_quantity = isinstance(m, Quantity)
    arr = m.magnitude if is_quantity else m
    
    arr = jnp.asarray(arr)
    
    # Normalize k to 0-3 range
    k = k % 4
    
    # Normalize axes
    axes = tuple(axes)
    if axes[0] == axes[1]:
        raise ValueError("axes must be different")
    
    # Normalize negative axes
    ndim = arr.ndim
    axes = tuple(ax % ndim if ax < 0 else ax for ax in axes)
    
    # Perform k rotations
    for _ in range(k):
        # Swap the two axes
        arr = jnp.swapaxes(arr, axes[0], axes[1])
        # Reverse along the first axis
        slices = [slice(None)] * arr.ndim
        slices[axes[0]] = slice(None, None, -1)
        arr = arr[tuple(slices)]
    
    if is_quantity:
        return Quantity(arr, m.units)
    return arr