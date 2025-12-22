import jax.numpy as jnp
from jax import jit
from typing import Union, Optional
from pint import Quantity
from pint.unit import Unit

def atan(
    x: Union[Quantity, jax.typing.ArrayLike],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    r"""Elementwise arc tangent: :math:`\mathrm{atan}(x)`."""
    if isinstance(x, Quantity):
        x = x.magnitude
    result = jnp.arctan(x)
    if unit_to_scale is not None:
        result = result * unit_to_scale
    return result