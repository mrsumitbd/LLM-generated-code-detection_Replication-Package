def triangular_solve(
    a: Union[Quantity, jax.typing.ArrayLike],
    b: Union[Quantity, jax.typing.ArrayLike],
    left_side: bool = False, lower: bool = False,
    transpose_a: bool = False, conjugate_a: bool = False,
    unit_diagonal: bool = False,
) -> Quantity | jax.Array:
    import jax.numpy as jnp
    from jax import lax
    
    # Handle Quantity types
    a_unit = None
    b_unit = None
    
    if isinstance(a, Quantity):
        a_unit = a.unit
        a = a.magnitude
    
    if isinstance(b, Quantity):
        b_unit = b.unit
        b = b.magnitude
    
    # Perform the triangular solve
    result = lax.triangular_solve(
        a,
        b,
        left_side=left_side,
        lower=lower,
        transpose_a=transpose_a,
        conjugate_a=conjugate_a,
        unit_diagonal=unit_diagonal,
    )
    
    # Handle unit conversion if needed
    if b_unit is not None and a_unit is not None:
        # Result has units of b_unit / a_unit
        result = Quantity(result, b_unit / a_unit)
    elif b_unit is not None:
        result = Quantity(result, b_unit)
    elif a_unit is not None:
        result = Quantity(result, 1 / a_unit)
    
    return result