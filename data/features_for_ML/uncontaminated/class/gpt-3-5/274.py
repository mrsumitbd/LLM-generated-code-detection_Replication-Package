class CodeIOConfig:
    """Configuration for CodeI/O reasoning task generation"""

    def __init__(self, input_size: int, output_size: int, max_value: int):
        self.input_size = input_size
        self.output_size = output_size
        self.max_value = max_value

    def validate(self) -> None:
        if not isinstance(self.input_size, int) or not isinstance(self.output_size, int) or not isinstance(self.max_value, int):
            raise ValueError("Input size, output size, and max value must be integers")
        if self.input_size <= 0 or self.output_size <= 0 or self.max_value <= 0:
            raise ValueError("Input size, output size, and max value must be greater than 0")