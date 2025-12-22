from typing import Optional

class RottenOrangesConfig:
    """Configuration for Rotten Oranges dataset generation"""

    min_n: int = 10  # Minimum size of the matrix
    max_n: int = 30  # Maximum size of the matrix
    p_oranges: float = 0.85  # Percent of grid cells populated with oranges
    p_rotten: float = 0.1  # Percent of oranges that are initially rotten

    size: int = 500  # Virtual dataset size
    seed: Optional[int] = None

    def validate(self):
        """Validate configuration parameters"""
        assert 2 <= self.min_n, "min_n must be at least 2"
        assert self.min_n <= self.max_n, "min_n must be less than or equal to max_n"
        assert 0 < self.p_oranges <= 1, "p_oranges must be between 0 and 1"
        assert 0 < self.p_rotten <= 1, "p_rotten must be between 0 and 1"