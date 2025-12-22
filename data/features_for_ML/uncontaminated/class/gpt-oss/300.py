import dataclasses
from typing import Callable, Iterable, Sequence

import jax
import jax.numpy as jnp
from jax import grad, jit
from jaxopt import ScipyMinimize
import numpy as np
from scipy.optimize import Bounds


@dataclasses.dataclass
class Hyperparameters:
    """
    Hyperparameters for the ErdosOptimizer.

    Attributes
    ----------
    num_steps : int
        Number of steps in the step function h.
    domain : tuple[float, float]
        The integration domain (start, end).
    functions : Sequence[Callable[[jnp.ndarray], jnp.ndarray]]
        A sequence of functions g_i(x) whose overlap with h is to be minimized.
    bounds : tuple[float, float]
        Lower and upper bounds for the step heights.
    initial_guess : jnp.ndarray | None
        Initial guess for the step heights. If None, zeros are used.
    max_iter : int
        Maximum number of iterations for the optimizer.
    tol : float
        Tolerance for convergence.
    """

    num_steps: int = 10
    domain: tuple[float, float] = (0.0, 1.0)
    functions: Sequence[Callable[[jnp.ndarray], jnp.ndarray]] = dataclasses.field(default_factory=list)
    bounds: tuple[float, float] = (0.0, 1.0)
    initial_guess: jnp.ndarray | None = None
    max_iter: int = 1000
    tol: float = 1e-6


class ErdosOptimizer:
    """
    Finds a step function h that minimizes the maximum overlap integral.
    """

    def __init__(self, hypers: Hyperparameters):
        self.hypers = hypers
        self.num_steps = hypers.num_steps
        self.domain = hypers.domain
        self.functions = hypers.functions
        self.bounds = hypers.bounds
        self.max_iter = hypers.max_iter
        self.tol = hypers.tol

        # Pre‑compute the grid points for integration
        self._grid = jnp.linspace(
            self.domain[0], self.domain[1], self.num_steps + 1
        )
        self._dx = (self.domain[1] - self.domain[0]) / self.num_steps

        # Initial guess
        if hypers.initial_guess is None:
            self._init_guess = jnp.zeros(self.num_steps)
        else:
            self._init_guess = jnp.asarray(hypers.initial_guess)

        # Bounds for the optimizer
        self._bounds = Bounds(
            np.full(self.num_steps, self.bounds[0]),
            np.full(self.num_steps, self.bounds[1]),
        )

    @jit
    def _objective_fn(self, latent_h_values: jnp.ndarray) -> jnp.ndarray:
        """
        Compute the maximum overlap integral over all functions g_i.

        Parameters
        ----------
        latent_h_values : jnp.ndarray
            Step heights of the function h.

        Returns
        -------
        jnp.ndarray
            The maximum overlap integral (scalar).
        """
        # Build the step function values on the grid
        # h(x) is constant on each interval [x_j, x_{j+1})
        h_vals = jnp.repeat(latent_h_values, 1)  # shape (num_steps,)

        # Evaluate each function on the grid points (excluding the last point)
        max_overlap = 0.0
        for g in self.functions:
            # Evaluate g on the left endpoints of each interval
            g_vals = g(self._grid[:-1])
            # Integral approximation: sum h(x_j) * g(x_j) * dx
            overlap = jnp.sum(h_vals * g_vals) * self._dx
            max_overlap = jnp.maximum(max_overlap, overlap)

        return max_overlap

    def run_optimization(self):
        """
        Run the optimization to find the step heights that minimize the maximum overlap integral.

        Returns
        -------
        jnp.ndarray
            Optimized step heights.
        """
        # Use JAX‑opt's ScipyMinimize with the L-BFGS-B algorithm
        optimizer = ScipyMinimize(
            fun=self._objective_fn,
            method="L-BFGS-B",
            bounds=self._bounds,
            options={"maxiter": self.max_iter, "ftol": self.tol},
        )

        opt_state = optimizer.init_state(self._init_guess)
        opt_state = optimizer.run(opt_state, maxiter=self.max_iter)
        return opt_state.params