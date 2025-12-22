def triangular_solve(
    a: Union[Quantity, jax.typing.ArrayLike],
    b: Union[Quantity, jax.typing.ArrayLike],
    left_side: bool = False, lower: bool = False,
    transpose_a: bool = False, conjugate_a: bool = False,
    unit_diagonal: bool = False,
) -> Quantity | jax.Array:
    if left_side:
        if transpose_a:
            a = jnp.swapaxes(a, -2, -1)
        if conjugate_a:
            a = jnp.conj(a)
        if lower:
            a = jnp.tril(a)
        else:
            a = jnp.triu(a)
        if unit_diagonal:
            a = a + jnp.eye(a.shape[-1], dtype=a.dtype)
        return jnp.linalg.solve(a, b)
    else:
        if transpose_a:
            a = jnp.swapaxes(a, -2, -1)
        if conjugate_a:
            a = jnp.conj(a)
        if lower:
            a = jnp.tril(a)
        else:
            a = jnp.triu(a)
        if unit_diagonal:
            a = a + jnp.eye(a.shape[-1], dtype=a.dtype)
        return jnp.linalg.solve(a.swapaxes(-2, -1), b.swapaxes(-2, -1)).swapaxes(-2, -1)