class RotateMatrixConfig:
    """Configuration for Rotate Matrix dataset generation"""

    def __init__(self, matrix_size: int = 4, rotation_angle: int = 90, 
                 num_samples: int = 100, seed: int = None):
        self.matrix_size = matrix_size
        self.rotation_angle = rotation_angle
        self.num_samples = num_samples
        self.seed = seed

    def validate(self):
        if not isinstance(self.matrix_size, int) or self.matrix_size <= 0:
            raise ValueError("matrix_size must be a positive integer")
        
        if not isinstance(self.rotation_angle, int):
            raise ValueError("rotation_angle must be an integer")
        
        if self.rotation_angle % 90 != 0:
            raise ValueError("rotation_angle must be a multiple of 90")
        
        if not isinstance(self.num_samples, int) or self.num_samples <= 0:
            raise ValueError("num_samples must be a positive integer")
        
        if self.seed is not None and (not isinstance(self.seed, int) or self.seed < 0):
            raise ValueError("seed must be a non-negative integer or None")
        
        return True