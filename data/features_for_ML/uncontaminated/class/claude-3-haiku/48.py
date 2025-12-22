class SpiralMatrixConfig:
    """Configuration for Spiral Matrix dataset generation"""

    def __init__(self, rows: int, cols: int, start_value: int, step: int):
        self.rows = rows
        self.cols = cols
        self.start_value = start_value
        self.step = step

    def validate(self):
        if self.rows <= 0 or self.cols <= 0:
            raise ValueError("Rows and columns must be positive integers.")
        if self.start_value < 0:
            raise ValueError("Start value must be a non-negative integer.")
        if self.step <= 0:
            raise ValueError("Step must be a positive integer.")