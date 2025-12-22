from dataclasses import dataclass

@dataclass
class GCGConfig:
    """
    Configuration dataclass for the GCG attack parameters
    """
    num_iterations: int
    learning_rate: float
    momentum: float
    epsilon: float
    max_norm: float
    targeted: bool
    confidence: float
    abort_early: bool
    binary_search_steps: int
    initial_const: float
    batch_size: int
    clip_min: float
    clip_max: float