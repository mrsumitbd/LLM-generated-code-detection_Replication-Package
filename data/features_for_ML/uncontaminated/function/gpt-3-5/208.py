def coo_matvec(mat: COO, v: jax.Array | Quantity, transpose: bool = False) -> jax.Array | Quantity:
    if transpose:
        return mat.T.dot(v)
    else:
        return mat.dot(v)