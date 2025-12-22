class NumberFormatConfig:
    """Configuration for Count Bits dataset generation"""

    def __init__(self, min_value: int, max_value: int, num_samples: int, seed: int = None):
        self.min_value = min_value
        self.max_value = max_value
        self.num_samples = num_samples
        self.seed = seed

    def validate(self):
        if self.min_value < 0:
            raise ValueError("Minimum value must be non-negative")
        if self.max_value <= self.min_value:
            raise ValueError("Maximum value must be greater than minimum value")
        if self.num_samples <= 0:
            raise ValueError("Number of samples must be positive")
        if self.seed is not None and (self.seed < 0 or self.seed > 2 ** 32 - 1):
            raise ValueError("Seed must be between 0 and 2^32 - 1")