class CodeIOConfig:
    """Configuration for CodeI/O reasoning task generation"""

    def __init__(
        self,
        num_samples: int = 100,
        max_code_length: int = 1000,
        max_input_length: int = 500,
        max_output_length: int = 500,
        languages: list = None,
        difficulty_levels: list = None,
        include_edge_cases: bool = True,
        timeout_seconds: int = 5,
        seed: int = None,
    ):
        self.num_samples = num_samples
        self.max_code_length = max_code_length
        self.max_input_length = max_input_length
        self.max_output_length = max_output_length
        self.languages = languages or ["python", "javascript", "java"]
        self.difficulty_levels = difficulty_levels or ["easy", "medium", "hard"]
        self.include_edge_cases = include_edge_cases
        self.timeout_seconds = timeout_seconds
        self.seed = seed

    def validate(self) -> None:
        if self.num_samples <= 0:
            raise ValueError("num_samples must be positive")
        if self.max_code_length <= 0:
            raise ValueError("max_code_length must be positive")
        if self.max_input_length <= 0:
            raise ValueError("max_input_length must be positive")
        if self.max_output_length <= 0:
            raise ValueError("max_output_length must be positive")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if not self.languages:
            raise ValueError("languages list cannot be empty")
        if not self.difficulty_levels:
            raise ValueError("difficulty_levels list cannot be empty")
        if self.seed is not None and self.seed < 0:
            raise ValueError("seed must be non-negative")