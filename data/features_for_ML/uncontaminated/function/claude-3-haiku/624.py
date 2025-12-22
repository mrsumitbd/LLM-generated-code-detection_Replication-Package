import jax.numpy as jnp

def loss(log_alpha: jnp.ndarray) -> jnp.ndarray:
    alpha = jnp.exp(log_alpha)
    loss_value = -jnp.mean(jnp.log(alpha))
    return loss_value