import jax.numpy as jnp
from jax import grad, jit, vmap
from jax.scipy.optimize import minimize

class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers

    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        return jnp.max(jnp.abs(jnp.dot(self.hypers.data, latent_h_values)))

    def run_optimization(self):
        initial_guess = jnp.zeros(self.hypers.data.shape[1])
        result = minimize(self._objective_fn, initial_guess, method='L-BFGS-B')
        return result.x