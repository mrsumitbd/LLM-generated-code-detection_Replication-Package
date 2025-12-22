from typing import Union
import jax.numpy as jnp
from pint import Quantity

def reshape(
    a: Union[jax.Array, Quantity],
    shape: Union[int, tuple],
    order: str = 'C'
) -> Union[jax.Array, Quantity]:
    if isinstance(a, Quantity):
        return a.to_base_units().magnitude.reshape(shape, order=order) * a.units
    else:
        return jnp.reshape(a, shape, order=order)