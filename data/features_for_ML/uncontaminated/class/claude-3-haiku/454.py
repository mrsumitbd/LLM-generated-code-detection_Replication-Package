class RottenOrangesConfig:
    """Configuration for Rotten Oranges dataset generation"""

    def __init__(self, num_rows: int, num_cols: int, num_fresh: int, num_rotten: int, seed: int = None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.num_fresh = num_fresh
        self.num_rotten = num_rotten
        self.seed = seed

    def validate(self):
        if self.num_rows <= 0 or self.num_cols <= 0:
            raise ValueError("Number of rows and columns must be positive integers.")
        if self.num_fresh < 0 or self.num_rotten < 0:
            raise ValueError("Number of fresh and rotten oranges must be non-negative integers.")
        if self.num_fresh + self.num_rotten > self.num_rows * self.num_cols:
            raise ValueError("Total number of oranges cannot exceed the grid size.")
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("Seed must be an integer or None.")