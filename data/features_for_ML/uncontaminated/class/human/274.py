from typing import Any, Optional

class CodeIOConfig:
    """Configuration for CodeI/O reasoning task generation"""

    seed: Optional[int] = None
    size: int = 500
    input_prediction_probability: float = 0.5
    difficulty: Optional[int] = None

    def validate(self) -> None:
        """Validate configuration parameters"""
        assert 0.0 <= self.input_prediction_probability <= 1.0, "input_prediction_probability must be in [0, 1]"
        if self.difficulty is not None:
            assert 1 <= self.difficulty <= 10, "difficulty must be in [1, 10]"