from typing import Optional

class RotateMatrixConfig:
    """Configuration for Rotate Matrix dataset generation"""

    min_n: int = 2  # Minimum size of the matrix
    max_n: int = 10  # Maximum size of the matrix
    min_rotations: int = 0  # Minimum number of rotations
    max_rotations: int = 10  # Maximum number of rotations (90 degrees each)

    size: int = 500  # Virtual dataset size
    seed: Optional[int] = None

    def validate(self):
        """Validate configuration parameters"""
        assert 2 <= self.min_n <= self.max_n, "min_n and max_n must be between 2 and 10"
        assert 0 <= self.min_rotations <= self.max_rotations, "min_rotations must be between 0 and max_rotations"