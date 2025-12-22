from __future__ import annotations

import random
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

# pylint: disable=too-many-instance-attributes
@dataclass
class GCGConfig:
    """
    Configuration dataclass for the GCG attack parameters.
    """

    # Core attack parameters
    model: Any
    loss_fn: Callable[[Any, Any], Any]
    target_label: Optional[int] = None
    num_steps: int = 100
    step_size: float = 0.01
    max_iter: int = 1000
    epsilon: float = 0.3
    random_start: bool = True
    clip_min: float = 0.0
    clip_max: float = 1.0

    # Device and precision
    device: str = "cpu"
    use_cuda: bool = False
    use_fp16: bool = False
    use_fp32: bool = True
    use_fp64: bool = False

    # Optimization settings
    optimizer: str = "sgd"  # or "adam"
    lr: float = 0.01
    momentum: float = 0.9
    beta1: float = 0.9
    beta2: float = 0.999
    eps: float = 1e-8
    weight_decay: float = 0.0
    lr_schedule: Optional[Callable[[int], float]] = None

    # Regularization and constraints
    clip_norm: Optional[float] = None
    grad_clip_value: Optional[float] = None
    grad_norm_value: Optional[float] = None

    # Early stopping and monitoring
    early_stop: bool = False
    early_stop_patience: int = 10
    early_stop_threshold: float = 1e-4

    # Logging and verbosity
    verbose: bool = False
    log_interval: int = 10

    # Miscellaneous
    seed: Optional[int] = None
    random_state: Optional[random.Random] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Resolve device
        if self.use_cuda:
            self.device = "cuda"
        else:
            self.device = "cpu"

        # Set random state
        if self.seed is not None:
            self.random_state = random.Random(self.seed)
        else:
            self.random_state = random

        # Validate optimizer
        if self.optimizer.lower() not in {"sgd", "adam"}:
            raise ValueError(f"Unsupported optimizer: {self.optimizer}")

        # Ensure epsilon is non-negative
        if self.epsilon < 0:
            raise ValueError("epsilon must be non-negative")

        # Ensure clip bounds are valid
        if self.clip_min > self.clip_max:
            raise ValueError("clip_min must be <= clip_max")

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a dictionary representation of the configuration.
        """
        cfg = asdict(self)
        # Remove non-serializable objects
        cfg.pop("model", None)
        cfg.pop("loss_fn", None)
        cfg.pop("random_state", None)
        return cfg

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"