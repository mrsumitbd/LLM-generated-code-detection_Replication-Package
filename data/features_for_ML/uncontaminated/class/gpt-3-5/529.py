class RotateMatrixConfig:
    """Configuration for Rotate Matrix dataset generation"""

    def __init__(self, input_size, output_size, max_rotation):
        self.input_size = input_size
        self.output_size = output_size
        self.max_rotation = max_rotation

    def validate(self):
        if not isinstance(self.input_size, int) or self.input_size <= 0:
            raise ValueError("Input size must be a positive integer")
        if not isinstance(self.output_size, int) or self.output_size <= 0:
            raise ValueError("Output size must be a positive integer")
        if not isinstance(self.max_rotation, int) or self.max_rotation < 0:
            raise ValueError("Max rotation must be a non-negative integer")