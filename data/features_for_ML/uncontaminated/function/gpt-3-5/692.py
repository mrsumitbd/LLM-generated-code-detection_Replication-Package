from typing import Union, Optional, Tuple
import jax
from jax import numpy as jnp
from numpy import nanpercentile as np_nanpercentile
from pint import Quantity

def nanpercentile(
    a: Union[jax.Array, Quantity],
    q: jax.typing.ArrayLike,
    axis: Optional[Union[int, Tuple[int]]] = None,
    method: str = 'linear',
    keepdims: Optional[bool] = False,
) -> jax.Array:
    if isinstance(a, Quantity):
        a = a.magnitude
    if isinstance(q, Quantity):
        q = q.magnitude
    if axis is not None and isinstance(axis, Tuple):
        axis = tuple(axis)
    return jnp.asarray(np_nanpercentile(a, q, axis=axis, method=method, keepdims=keepdims))