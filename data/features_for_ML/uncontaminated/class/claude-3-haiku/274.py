class CodeIOConfig:
    """Configuration for CodeI/O reasoning task generation"""

    def __init__(self, input_format: str, output_format: str, time_limit: float, memory_limit: float):
        self.input_format = input_format
        self.output_format = output_format
        self.time_limit = time_limit
        self.memory_limit = memory_limit

    def validate(self) -> None:
        if not isinstance(self.input_format, str) or not self.input_format:
            raise ValueError("input_format must be a non-empty string")
        if not isinstance(self.output_format, str) or not self.output_format:
            raise ValueError("output_format must be a non-empty string")
        if not isinstance(self.time_limit, (int, float)) or self.time_limit <= 0:
            raise ValueError("time_limit must be a positive number")
        if not isinstance(self.memory_limit, (int, float)) or self.memory_limit <= 0:
            raise ValueError("memory_limit must be a positive number")