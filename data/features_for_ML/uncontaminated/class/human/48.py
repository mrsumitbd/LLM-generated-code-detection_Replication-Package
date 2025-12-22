from typing import Any, Optional

class SpiralMatrixConfig:
    """Configuration for Spiral Matrix dataset generation"""

    min_n: int = 2  # Minimum number of rows/cols in the matrix
    max_n: int = 10  # Maximum number of rows/cols in the matrix

    size: int = 500  # Virtual dataset size
    seed: Optional[int] = None

    def validate(self):
        """Validate configuration parameters"""
        assert 2 <= self.min_n <= self.max_n, "min_n must be between 2 and max_n"