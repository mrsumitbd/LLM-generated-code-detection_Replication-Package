class OptimizationConfig:
    """Configuration for mathematical optimization."""

    def __init__(self, method, max_iterations=100, tolerance=1e-6, verbose=False):
        self.method = method
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.verbose = verbose

    def __str__(self):
        return f"Optimization Config: method={self.method}, max_iterations={self.max_iterations}, tolerance={self.tolerance}, verbose={self.verbose}"

    def __repr__(self):
        return f"OptimizationConfig(method='{self.method}', max_iterations={self.max_iterations}, tolerance={self.tolerance}, verbose={self.verbose})"

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")

    def copy(self):
        return OptimizationConfig(
            method=self.method,
            max_iterations=self.max_iterations,
            tolerance=self.tolerance,
            verbose=self.verbose
        )