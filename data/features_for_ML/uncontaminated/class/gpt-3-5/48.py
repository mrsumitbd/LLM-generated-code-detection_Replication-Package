class SpiralMatrixConfig:
    """Configuration for Spiral Matrix dataset generation"""

    def __init__(self, rows, cols, start_value):
        self.rows = rows
        self.cols = cols
        self.start_value = start_value

    def validate(self):
        if not isinstance(self.rows, int) or self.rows <= 0:
            raise ValueError("Number of rows must be a positive integer")
        if not isinstance(self.cols, int) or self.cols <= 0:
            raise ValueError("Number of columns must be a positive integer")
        if not isinstance(self.start_value, int):
            raise ValueError("Start value must be an integer")