import jax
import jax.numpy as jnp
from jax.scipy.optimize import minimize
from typing import Callable
import numpy as np


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    """

    def __init__(self, hypers: 'Hyperparameters'):
        self.hypers = hypers
        self.result = None
        self.optimal_h = None
        
    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        """
        Compute the maximum overlap integral for a given step function.
        
        Args:
            latent_h_values: The values of the step function at grid points
            
        Returns:
            The maximum overlap integral
        """
        # Ensure values are within valid bounds
        h_values = jnp.clip(latent_h_values, 0, 1)
        
        # Compute overlaps between consecutive step function values
        # The overlap integral is approximated by the sum of products
        overlaps = []
        
        for i in range(len(h_values) - 1):
            overlap = h_values[i] * h_values[i + 1]
            overlaps.append(overlap)
        
        if len(overlaps) == 0:
            return jnp.array(0.0)
        
        overlaps = jnp.array(overlaps)
        max_overlap = jnp.max(overlaps)
        
        return max_overlap
    
    def run_optimization(self):
        """
        Run the optimization to find the step function that minimizes
        the maximum overlap integral.
        """
        # Initialize the step function values
        n_steps = getattr(self.hypers, 'n_steps', 10)
        initial_h = jnp.ones(n_steps) * 0.5
        
        # Define the objective function for optimization
        def objective(x):
            return self._objective_fn(x)
        
        # Run optimization
        self.result = minimize(
            objective,
            initial_h,
            method='L-BFGS-B',
            options={'maxiter': 1000}
        )
        
        # Store the optimal step function
        self.optimal_h = jnp.clip(self.result.x, 0, 1)
        
        return self.optimal_h