import jax.numpy as jnp
from typing import Union, Sequence, Tuple
from saiunit.fft.utils import _fft_helper

def ifftn(
    a: Union[Quantity, jax.typing.ArrayLike],
    s: Shape | None = None,
    axes: Sequence[int] | None = None,
    norm: str | None = None
) -> Union[Quantity, jax.typing.ArrayLike]:
    return _fft_helper(a, s, axes, norm, inverse=True)