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
    k = k % 4
    m = jnp.asarray(m)
    axes = tuple(axes)
    if len(axes) != 2 or axes[0] == axes[1] or min(axes) < 0 or max(axes) >= m.ndim:
        raise ValueError("Invalid axes")
    if k == 0:
        return m
    elif k == 1:
        return jnp.transpose(m, axes=(0, 1, *[i for i in range(2, m.ndim) if i not in axes])).swapaxes(axes[0], axes[1])
    elif k == 2:
        return m[..., ::-1, ::-1]
    else:
        return jnp.transpose(m, axes=(0, 1, *[i for i in range(2, m.ndim) if i not in axes])).swapaxes(axes[0], axes[1])[::-1, ::-1, ...]