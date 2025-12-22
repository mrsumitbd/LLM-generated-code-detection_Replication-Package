class SpiralMatrixConfig:
    """Configuration for Spiral Matrix dataset generation"""

    def __init__(self, size, start=1, step=1, direction="clockwise"):
        self.size = size
        self.start = start
        self.step = step
        self.direction = direction

    def validate(self):
        # Validate size
        if not isinstance(self.size, int):
            raise TypeError(f"size must be an integer, got {type(self.size).__name__}")
        if self.size <= 0:
            raise ValueError("size must be a positive integer")

        # Validate start
        if not isinstance(self.start, int):
            raise TypeError(f"start must be an integer, got {type(self.start).__name__}")

        # Validate step
        if not isinstance(self.step, int):
            raise TypeError(f"step must be an integer, got {type(self.step).__name__}")
        if self.step == 0:
            raise ValueError("step cannot be zero")

        # Validate direction
        if not isinstance(self.direction, str):
            raise TypeError(f"direction must be a string, got {type(self.direction).__name__}")
        if self.direction.lower() not in {"clockwise", "counterclockwise"}:
            raise ValueError("direction must be either 'clockwise' or 'counterclockwise'")