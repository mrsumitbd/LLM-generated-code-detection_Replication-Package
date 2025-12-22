class RottenOrangesConfig:
    """Configuration for Rotten Oranges dataset generation"""

    def __init__(self, rows, cols, num_rotten, num_fresh):
        self.rows = rows
        self.cols = cols
        self.num_rotten = num_rotten
        self.num_fresh = num_fresh

    def validate(self):
        if not isinstance(self.rows, int) or self.rows <= 0:
            raise ValueError("Number of rows must be a positive integer")
        if not isinstance(self.cols, int) or self.cols <= 0:
            raise ValueError("Number of columns must be a positive integer")
        if not isinstance(self.num_rotten, int) or self.num_rotten < 0:
            raise ValueError("Number of rotten oranges must be a non-negative integer")
        if not isinstance(self.num_fresh, int) or self.num_fresh < 0:
            raise ValueError("Number of fresh oranges must be a non-negative integer")