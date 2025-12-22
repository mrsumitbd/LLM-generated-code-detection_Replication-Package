class NumberFormatConfig:
    """Configuration for Count Bits dataset generation"""

    def __init__(self, num_bits, min_value, max_value):
        self.num_bits = num_bits
        self.min_value = min_value
        self.max_value = max_value

    def validate(self):
        if not isinstance(self.num_bits, int) or self.num_bits <= 0:
            raise ValueError("num_bits must be a positive integer")
        if not isinstance(self.min_value, int) or not isinstance(self.max_value, int):
            raise ValueError("min_value and max_value must be integers")
        if self.min_value >= self.max_value:
            raise ValueError("min_value must be less than max_value")