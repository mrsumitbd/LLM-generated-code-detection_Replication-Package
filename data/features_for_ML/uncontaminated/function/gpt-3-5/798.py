from typing import Union, Tuple
import jax
from jax import numpy as jnp
from numpy import ndarray
from pint import Quantity

def rot90(
    m: Union[jax.typing.ArrayLike, Quantity],
    k: int = 1,
    axes: Tuple[int, int] = (0, 1)
) -> Union[jax.Array, Quantity]:
    
    def _rot90(m, k, axes):
        axes = list(axes)
        if axes[0] < 0:
            axes[0] += m.ndim
        if axes[1] < 0:
            axes[1] += m.ndim
        if axes[0] == axes[1] or axes[0] >= m.ndim or axes[1] >= m.ndim:
            raise ValueError("Axes must be different and valid.")
        
        if k % 4 == 0:
            return m
        if k % 4 == 2:
            return jnp.flip(jnp.flip(m, axes[0]), axes[1])
        
        axes = tuple(axes)
        perm = [i for i in range(m.ndim) if i not in axes]
        perm = axes[0], *perm, axes[1]
        m = jnp.transpose(m, perm)
        m = jnp.flip(m, axes[1])
        return m if k % 4 == 1 else jnp.flip(m, axes[0])
    
    if isinstance(m, Quantity):
        return Quantity(_rot90(m.magnitude, k, axes), m.units)
    return _rot90(m, k, axes)