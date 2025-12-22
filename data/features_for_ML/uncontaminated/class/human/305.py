
class TrainingConfig:
    """Training configuration."""
    model: str
    max_retries: int = 3
    retry_delay: int = 1
    similarity_threshold: float = 0.5
    max_examples: int = 512
    batch_size: int = 4