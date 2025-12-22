from typing import Union
import jax
from jax import numpy as jnp
from jax.lax import dot

def triangular_solve(
    a: Union[jnp.ndarray, jax.typing.ArrayLike],
    b: Union[jnp.ndarray, jax.typing.ArrayLike],
    left_side: bool = False, lower: bool = False,
    transpose_a: bool = False, conjugate_a: bool = False,
    unit_diagonal: bool = False,
) -> jnp.ndarray:
    if transpose_a:
        a = jnp.swapaxes(a, -1, -2)
    if conjugate_a:
        a = jnp.conj(a)
    if lower:
        a = jnp.tril(a) if unit_diagonal else jnp.tril(a, -1)
    else:
        a = jnp.triu(a) if unit_diagonal else jnp.triu(a, 1)

    if left_side:
        x = jnp.linalg.solve(a, b)
    else:
        x = jnp.linalg.solve(a.T, b.T).T

    return x