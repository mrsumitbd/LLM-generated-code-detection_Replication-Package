import numpy as np
from typing import Callable, Iterable, List, Tuple, Dict, Any, Optional, Union


class OptimizationConfig:
    """Configuration for mathematical optimization."""

    def __init__(
        self,
        objective: Optional[Callable[[np.ndarray], float]] = None,
        constraints: Optional[Iterable[Callable[[np.ndarray], bool]]] = None,
        bounds: Optional[Iterable[Tuple[Optional[float], Optional[float]]]] = None,
        method: str = "L-BFGS-B",
        options: Optional[Dict[str, Any]] = None,
        tolerance: float = 1e-6,
        max_iter: int = 1000,
        verbose: bool = False,
    ) -> None:
        self.objective = objective
        self.constraints = list(constraints) if constraints is not None else []
        self.bounds = list(bounds) if bounds is not None else None
        self.method = method
        self.options = options or {}
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.verbose = verbose
        self._validate()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def _validate(self) -> None:
        if self.objective is not None and not callable(self.objective):
            raise TypeError("objective must be callable or None")
        if not isinstance(self.constraints, list):
            raise TypeError("constraints must be a list of callables")
        for c in self.constraints:
            if not callable(c):
                raise TypeError("each constraint must be callable")
        if self.bounds is not None:
            if not isinstance(self.bounds, list):
                raise TypeError("bounds must be a list of (lower, upper) tuples")
            for b in self.bounds:
                if (
                    not isinstance(b, tuple)
                    or len(b) != 2
                    or (b[0] is not None and not isinstance(b[0], (int, float)))
                    or (b[1] is not None and not isinstance(b[1], (int, float)))
                ):
                    raise ValueError(
                        "each bound must be a tuple of (lower, upper) where each is a float or None"
                    )
        if not isinstance(self.method, str):
            raise TypeError("method must be a string")
        if not isinstance(self.options, dict):
            raise TypeError("options must be a dictionary")
        if not isinstance(self.tolerance, (float, int)):
            raise TypeError("tolerance must be a float")
        if not isinstance(self.max_iter, int):
            raise TypeError("max_iter must be an integer")
        if not isinstance(self.verbose, bool):
            raise TypeError("verbose must be a boolean")

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"objective={self.objective!r}, "
            f"constraints={self.constraints!r}, "
            f"bounds={self.bounds!r}, "
            f"method={self.method!r}, "
            f"options={self.options!r}, "
            f"tolerance={self.tolerance!r}, "
            f"max_iter={self.max_iter!r}, "
            f"verbose={self.verbose!r})"
        )

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the configuration."""
        return {
            "objective": self.objective,
            "constraints": self.constraints,
            "bounds": self.bounds,
            "method": self.method,
            "options": self.options,
            "tolerance": self.tolerance,
            "max_iter": self.max_iter,
            "verbose": self.verbose,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OptimizationConfig":
        """Create an instance from a dictionary."""
        return cls(
            objective=data.get("objective"),
            constraints=data.get("constraints"),
            bounds=data.get("bounds"),
            method=data.get("method", "L-BFGS-B"),
            options=data.get("options"),
            tolerance=data.get("tolerance", 1e-6),
            max_iter=data.get("max_iter", 1000),
            verbose=data.get("verbose", False),
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------
    def apply_to(self, x0: np.ndarray) -> Dict[str, Any]:
        """
        Run the optimization using scipy.optimize.minimize with the current configuration.
        Returns the result dictionary.
        """
        import scipy.optimize

        if self.objective is None:
            raise ValueError("objective function is not defined")

        result = scipy.optimize.minimize(
            fun=self.objective,
            x0=x0,
            method=self.method,
            bounds=self.bounds,
            constraints=self.constraints,
            options={
                "ftol": self.tolerance,
                "maxiter": self.max_iter,
                **self.options,
            },
        )
        if self.verbose:
            print(result)
        return result