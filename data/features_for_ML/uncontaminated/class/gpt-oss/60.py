import argparse
import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class ArgsConfig:
    """Configuration for GR00T model fine‑tuning."""

    # Model and data
    model_name_or_path: str = "gr00t-base"
    train_file: Optional[str] = None
    eval_file: Optional[str] = None

    # Training hyper‑parameters
    learning_rate: float = 5e-5
    per_device_train_batch_size: int = 8
    per_device_eval_batch_size: int = 8
    num_train_epochs: int = 3
    weight_decay: float = 0.0
    gradient_accumulation_steps: int = 1
    fp16: bool = False

    # Logging & saving
    output_dir: str = "./results"
    logging_steps: int = 500
    save_steps: int = 500
    evaluation_strategy: str = "steps"  # "no", "steps", or "epoch"
    save_total_limit: Optional[int] = None

    # Miscellaneous
    seed: int = 42
    push_to_hub: bool = False
    hub_model_id: Optional[str] = None
    hub_token: Optional[str] = None

    @staticmethod
    def parse_args() -> "ArgsConfig":
        """Parse command‑line arguments into an ArgsConfig instance."""
        parser = argparse.ArgumentParser(description="GR00T fine‑tuning arguments")
        parser.add_argument("--model_name_or_path", type=str, default="gr00t-base")
        parser.add_argument("--train_file", type=str, default=None)
        parser.add_argument("--eval_file", type=str, default=None)
        parser.add_argument("--learning_rate", type=float, default=5e-5)
        parser.add_argument("--per_device_train_batch_size", type=int, default=8)
        parser.add_argument("--per_device_eval_batch_size", type=int, default=8)
        parser.add_argument("--num_train_epochs", type=int, default=3)
        parser.add_argument("--weight_decay", type=float, default=0.0)
        parser.add_argument("--gradient_accumulation_steps", type=int, default=1)
        parser.add_argument("--fp16", action="store_true")
        parser.add_argument("--output_dir", type=str, default="./results")
        parser.add_argument("--logging_steps", type=int, default=500)
        parser.add_argument("--save_steps", type=int, default=500)
        parser.add_argument(
            "--evaluation_strategy",
            type=str,
            default="steps",
            choices=["no", "steps", "epoch"],
        )
        parser.add_argument("--save_total_limit", type=int, default=None)
        parser.add_argument("--seed", type=int, default=42)
        parser.add_argument("--push_to_hub", action="store_true")
        parser.add_argument("--hub_model_id", type=str, default=None)
        parser.add_argument("--hub_token", type=str, default=None)

        args = parser.parse_args()
        return ArgsConfig(**vars(args))

    def to_dict(self) -> dict:
        """Return a dictionary representation of the configuration."""
        return asdict(self)

    def save_json(self, path: str) -> None:
        """Save the configuration to a JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def from_json(cls, path: str) -> "ArgsConfig":
        """Load a configuration from a JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.train_file is None and self.eval_file is None:
            raise ValueError("At least one of train_file or eval_file must be provided.")
        if self.save_total_limit is not None and self.save_total_limit <= 0:
            raise ValueError("save_total_limit must be a positive integer if set.")