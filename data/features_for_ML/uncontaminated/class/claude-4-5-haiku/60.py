import argparse
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ArgsConfig:
    """Configuration for GR00T model fine-tuning."""
    
    # Model configuration
    model_name: str = field(default="gr00t", metadata={"help": "Name of the model to use"})
    model_path: Optional[str] = field(default=None, metadata={"help": "Path to the model checkpoint"})
    
    # Training configuration
    learning_rate: float = field(default=1e-4, metadata={"help": "Learning rate for training"})
    batch_size: int = field(default=32, metadata={"help": "Batch size for training"})
    num_epochs: int = field(default=3, metadata={"help": "Number of training epochs"})
    warmup_steps: int = field(default=500, metadata={"help": "Number of warmup steps"})
    weight_decay: float = field(default=0.01, metadata={"help": "Weight decay for optimizer"})
    
    # Data configuration
    train_data_path: Optional[str] = field(default=None, metadata={"help": "Path to training data"})
    val_data_path: Optional[str] = field(default=None, metadata={"help": "Path to validation data"})
    test_data_path: Optional[str] = field(default=None, metadata={"help": "Path to test data"})
    max_seq_length: int = field(default=512, metadata={"help": "Maximum sequence length"})
    
    # Output configuration
    output_dir: str = field(default="./output", metadata={"help": "Output directory for results"})
    save_steps: int = field(default=500, metadata={"help": "Save checkpoint every N steps"})
    eval_steps: int = field(default=500, metadata={"help": "Evaluate every N steps"})
    
    # Hardware configuration
    device: str = field(default="cuda", metadata={"help": "Device to use (cuda or cpu)"})
    num_workers: int = field(default=4, metadata={"help": "Number of data loading workers"})
    
    # Logging configuration
    logging_steps: int = field(default=100, metadata={"help": "Log every N steps"})
    seed: int = field(default=42, metadata={"help": "Random seed"})
    
    # Fine-tuning specific
    freeze_backbone: bool = field(default=False, metadata={"help": "Whether to freeze the backbone"})
    lora_rank: int = field(default=8, metadata={"help": "LoRA rank for parameter-efficient fine-tuning"})
    lora_alpha: int = field(default=16, metadata={"help": "LoRA alpha for scaling"})
    
    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "ArgsConfig":
        """Create ArgsConfig from argparse Namespace."""
        return cls(**vars(args))
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "ArgsConfig":
        """Create ArgsConfig from dictionary."""
        return cls(**config_dict)
    
    def to_dict(self) -> dict:
        """Convert ArgsConfig to dictionary."""
        return {
            "model_name": self.model_name,
            "model_path": self.model_path,
            "learning_rate": self.learning_rate,
            "batch_size": self.batch_size,
            "num_epochs": self.num_epochs,
            "warmup_steps": self.warmup_steps,
            "weight_decay": self.weight_decay,
            "train_data_path": self.train_data_path,
            "val_data_path": self.val_data_path,
            "test_data_path": self.test_data_path,
            "max_seq_length": self.max_seq_length,
            "output_dir": self.output_dir,
            "save_steps": self.save_steps,
            "eval_steps": self.eval_steps,
            "device": self.device,
            "num_workers": self.num_workers,
            "logging_steps": self.logging_steps,
            "seed": self.seed,
            "freeze_backbone": self.freeze_backbone,
            "lora_rank": self.lora_rank,
            "lora_alpha": self.lora_alpha,
        }
    
    def get_parser(self) -> argparse.ArgumentParser:
        """Get argparse parser with all configuration options."""
        parser = argparse.ArgumentParser(description="GR00T model fine-tuning configuration")
        
        parser.add_argument("--model_name", type=str, default=self.model_name)
        parser.add_argument("--model_path", type=str, default=self.model_path)
        parser.add_argument("--learning_rate", type=float, default=self.learning_rate)
        parser.add_argument("--batch_size", type=int, default=self.batch_size)
        parser.add_argument("--num_epochs", type=int, default=self.num_epochs)
        parser.add_argument("--warmup_steps", type=int, default=self.warmup_steps)
        parser.add_argument("--weight_decay", type=float, default=self.weight_decay)
        parser.add_argument("--train_data_path", type=str, default=self.train_data_path)
        parser.add_argument("--val_data_path", type=str, default=self.val_data_path)
        parser.add_argument("--test_data_path", type=str, default=self.test_data_path)
        parser.add_argument("--max_seq_length", type=int, default=self.max_seq_length)
        parser.add_argument("--output_dir", type=str, default=self.output_dir)
        parser.add_argument("--save_steps", type=int, default=self.save_steps)
        parser.add_argument("--eval_steps", type=int, default=self.eval_steps)
        parser.add_argument("--device", type=str, default=self.device)
        parser.add_argument("--num_workers", type=int, default=self.num_workers)
        parser.add_argument("--logging_steps", type=int, default=self.logging_steps)
        parser.add_argument("--seed", type=int, default=self.seed)
        parser.add_argument("--freeze_backbone", action="store_true", default=self.freeze_backbone)
        parser.add_argument("--lora_rank", type=int, default=self.lora_rank)
        parser.add_argument("--lora_alpha", type=int, default=self.lora_alpha)
        
        return parser


if __name__ == "__main__":
    config = ArgsConfig()
    print(config)
    print(config.to_dict())