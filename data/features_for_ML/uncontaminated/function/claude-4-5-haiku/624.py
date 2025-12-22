def loss(log_alpha: jnp.ndarray) -> jnp.ndarray:
    return jnp.sum(jnp.nn.softplus(log_alpha))