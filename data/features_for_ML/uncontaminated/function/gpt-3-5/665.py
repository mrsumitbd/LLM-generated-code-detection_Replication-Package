from typing import Union, Optional
import jax
from jax import numpy as jnp
from pint import Quantity, Unit

def sin(
    x: Union[jax.typing.ArrayLike, Quantity],
    unit_to_scale: Optional[Unit] = None,
) -> jax.Array:
    if isinstance(x, Quantity):
        if unit_to_scale is not None:
            x = x.to(unit_to_scale).magnitude
        else:
            x = x.magnitude
    return jnp.sin(x)