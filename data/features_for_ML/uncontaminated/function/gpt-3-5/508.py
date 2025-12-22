from typing import Union, Sequence
import jax
from jax import numpy as jnp
from saiunit import Quantity

def ifftn(
    a: Union[Quantity, jax.typing.ArrayLike],
    s: Sequence[int] | None = None,
    axes: Sequence[int] | None = None,
    norm: str | None = None
) -> Union[Quantity, jax.typing.ArrayLike]:
    return jnp.fft.ifftn(a, s=s, axes=axes, norm=norm)