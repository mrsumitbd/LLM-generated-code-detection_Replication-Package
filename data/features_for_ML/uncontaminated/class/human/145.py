from typing import Any, Optional

class NumberFormatConfig:
    """Configuration for Count Bits dataset generation"""

    min_num_candidates: int = 2  # Minimum number of candidates
    max_num_candidates: int = 5  # Maximum number of candidates
    min_n: float = 1_000  # Lower bound for the numbers
    max_n: float = 1_000_000_000  # Upper bound for the numbers
    max_delta: float = 10.0

    size: int = 500  # Virtual dataset size
    seed: Optional[int] = None

    def validate(self):
        """Validate configuration parameters"""
        assert 2 <= self.min_num_candidates, "min_num_candidates must be at least 2"
        assert (
            self.min_num_candidates <= self.max_num_candidates
        ), "min_num_candidates must be less than max_num_candidates"
        assert 1 <= self.min_n, "min_n must be at least 1"
        assert self.min_n < self.max_n, "min_n must be less than max_n"
        assert 0 < self.max_delta, "max_delta must be greater than 0"