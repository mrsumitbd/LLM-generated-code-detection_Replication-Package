class CodeIOConfig:
    """Configuration for CodeI/O reasoning task generation"""

    def __init__(
        self,
        input_file: str = "input.txt",
        output_file: str = "output.txt",
        timeout: int = 5,
        memory_limit: int = 256,
        language: str = "python",
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.language = language

    def validate(self) -> None:
        if not isinstance(self.input_file, str) or not self.input_file:
            raise ValueError("input_file must be a non-empty string")
        if not isinstance(self.output_file, str) or not self.output_file:
            raise ValueError("output_file must be a non-empty string")
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            raise ValueError("timeout must be a positive integer")
        if not isinstance(self.memory_limit, int) or self.memory_limit <= 0:
            raise ValueError("memory_limit must be a positive integer")
        allowed_langs = {"python", "cpp", "java", "javascript", "c", "c++"}
        if not isinstance(self.language, str) or self.language.lower() not in allowed_langs:
            raise ValueError(f"language must be one of {allowed_langs}")