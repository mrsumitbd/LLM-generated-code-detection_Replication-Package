class RotateMatrixConfig:
    """Configuration for Rotate Matrix dataset generation"""

    def __init__(self, matrix_size, num_rotations, noise_level=0.0, seed=None):
        self.matrix_size = matrix_size
        self.num_rotations = num_rotations
        self.noise_level = noise_level
        self.seed = seed

    def validate(self):
        if not isinstance(self.matrix_size, int) or self.matrix_size <= 0:
            raise ValueError("matrix_size must be a positive integer")
        if not isinstance(self.num_rotations, int) or self.num_rotations <= 0:
            raise ValueError("num_rotations must be a positive integer")
        if not isinstance(self.noise_level, (int, float)) or self.noise_level < 0 or self.noise_level > 1:
            raise ValueError("noise_level must be a float between 0 and 1")
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("seed must be an integer or None")