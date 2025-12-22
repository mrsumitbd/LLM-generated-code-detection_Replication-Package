class SpiralMatrixConfig:
    """Configuration for Spiral Matrix dataset generation"""

    def __init__(self, n: int = 5, direction: str = 'clockwise', start_pos: str = 'top-left', fill_value: int = 1):
        """
        Initialize SpiralMatrixConfig.
        
        Args:
            n: Size of the matrix (n x n)
            direction: Direction of spiral ('clockwise' or 'counterclockwise')
            start_pos: Starting position ('top-left', 'top-right', 'bottom-left', 'bottom-right')
            fill_value: Starting value for filling the spiral
        """
        self.n = n
        self.direction = direction
        self.start_pos = start_pos
        self.fill_value = fill_value

    def validate(self):
        """Validate the configuration parameters"""
        if not isinstance(self.n, int) or self.n <= 0:
            raise ValueError("n must be a positive integer")
        
        if self.direction not in ('clockwise', 'counterclockwise'):
            raise ValueError("direction must be 'clockwise' or 'counterclockwise'")
        
        if self.start_pos not in ('top-left', 'top-right', 'bottom-left', 'bottom-right'):
            raise ValueError("start_pos must be one of: 'top-left', 'top-right', 'bottom-left', 'bottom-right'")
        
        if not isinstance(self.fill_value, int):
            raise ValueError("fill_value must be an integer")