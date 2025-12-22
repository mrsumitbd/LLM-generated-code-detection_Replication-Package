import jax.numpy as jnp

def loss(log_alpha: jnp.ndarray) -> jnp.ndarray:
    """
    Compute a simple loss for the log_alpha parameter.
    This implementation returns the negative mean of log_alpha,
    which can be used to encourage larger values of alpha.
    """
    return -jnp.mean(log_alpha)