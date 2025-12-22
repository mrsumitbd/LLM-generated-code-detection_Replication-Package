def atan(
    x: Union[Quantity, jax.typing.ArrayLike],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    r"""Elementwise arc tangent: :math:`\mathrm{atan}(x)`."""
    if isinstance(x, Quantity):
        if unit_to_scale is not None:
            raise ValueError(
                "unit_to_scale should not be specified if x is a Quantity"
            )
        return jnp.arctan(x.value)
    else:
        return jnp.arctan(x)