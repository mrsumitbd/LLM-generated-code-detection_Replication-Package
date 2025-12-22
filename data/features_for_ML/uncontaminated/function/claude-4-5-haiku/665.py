def sin(
    x: Union[jax.typing.ArrayLike, Quantity],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    """
    Compute the sine of the input elements.

    Parameters
    ----------
    x : array_like, Quantity
      Input array or Quantity.
    unit_to_scale : Unit, optional
      The unit to scale the ``x``.

    Returns
    -------
    out : jax.Array
      Output array.
    """
    if isinstance(x, Quantity):
        if unit_to_scale is None:
            unit_to_scale = x.unit
        x_scaled = x.to(unit_to_scale).value
    else:
        x_scaled = x
    
    return jnp.sin(x_scaled)