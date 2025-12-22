from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Type, TypeVar

T = TypeVar("T", bound="TrainingConfig")


@dataclass
class TrainingConfig:
    """Training configuration."""

    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 10
    optimizer: str = "adam"
    loss: str = "categorical_crossentropy"
    metrics: List[str] = field(default_factory=lambda: ["accuracy"])
    early_stopping: bool = False
    patience: int = 5
    lr_scheduler: Optional[str] = None
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.learning_rate, (float, int)) or self.learning_rate <= 0:
            raise ValueError("learning_rate must be a positive number")
        if not isinstance(self.batch_size, int) or self.batch_size <= 0:
            raise ValueError("batch_size must be a positive integer")
        if not isinstance(self.epochs, int) or self.epochs <= 0:
            raise ValueError("epochs must be a positive integer")
        if not isinstance(self.optimizer, str) or not self.optimizer:
            raise ValueError("optimizer must be a non-empty string")
        if not isinstance(self.loss, str) or not self.loss:
            raise ValueError("loss must be a non-empty string")
        if not isinstance(self.metrics, list) or not all(isinstance(m, str) for m in self.metrics):
            raise ValueError("metrics must be a list of strings")
        if not isinstance(self.early_stopping, bool):
            raise ValueError("early_stopping must be a boolean")
        if not isinstance(self.patience, int) or self.patience < 0:
            raise ValueError("patience must be a non-negative integer")
        if self.lr_scheduler is not None and not isinstance(self.lr_scheduler, str):
            raise ValueError("lr_scheduler must be a string or None")
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("seed must be an integer or None")

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the configuration."""
        return asdict(self)

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a TrainingConfig instance from a dictionary."""
        return cls(**data)

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update the configuration with values from a dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.validate()

    @classmethod
    def from_json_file(cls: Type[T], path: str) -> T:
        """Load configuration from a JSON file."""
        if not os.path.isfile(path):
            raise FileNotFoundError(f"No such file: {path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def to_json_file(self, path: str) -> None:
        """Save configuration to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    def __repr__(self) -> str:
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"