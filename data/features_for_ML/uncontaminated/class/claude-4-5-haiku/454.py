class RottenOrangesConfig:
    """Configuration for Rotten Oranges dataset generation"""

    def __init__(
        self,
        grid_height: int = 10,
        grid_width: int = 10,
        num_rotten: int = 2,
        num_fresh: int = 5,
        seed: int = None,
    ):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.num_rotten = num_rotten
        self.num_fresh = num_fresh
        self.seed = seed

    def validate(self):
        if self.grid_height <= 0:
            raise ValueError("grid_height must be positive")
        if self.grid_width <= 0:
            raise ValueError("grid_width must be positive")
        if self.num_rotten < 0:
            raise ValueError("num_rotten must be non-negative")
        if self.num_fresh < 0:
            raise ValueError("num_fresh must be non-negative")
        
        max_cells = self.grid_height * self.grid_width
        total_oranges = self.num_rotten + self.num_fresh
        
        if total_oranges > max_cells:
            raise ValueError(
                f"Total oranges ({total_oranges}) exceeds grid capacity ({max_cells})"
            )
        
        if self.num_rotten == 0 and self.num_fresh > 0:
            raise ValueError("Must have at least one rotten orange if fresh oranges exist")
        
        if self.seed is not None and self.seed < 0:
            raise ValueError("seed must be non-negative")