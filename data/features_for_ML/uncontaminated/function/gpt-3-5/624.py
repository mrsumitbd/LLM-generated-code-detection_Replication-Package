import jax.numpy as jnp

def loss(log_alpha: jnp.ndarray) -> jnp.ndarray:
    return jnp.log1p(jnp.exp(log_alpha)) - log_alpha