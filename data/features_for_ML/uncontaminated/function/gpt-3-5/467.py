from typing import Union, Tuple
import jax
from numpy import ndarray
from astropy.units import Quantity

def reshape(
    a: Union[jax.Array, Quantity],
    shape: Union[int, Tuple[int, ...]],
    order: str = 'C'
) -> Union[jax.Array, Quantity]:
    return jax.numpy.reshape(a, shape, order=order)