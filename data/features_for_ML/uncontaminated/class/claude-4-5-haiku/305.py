class TrainingConfig:
    """Training configuration."""
    
    def __init__(
        self,
        learning_rate: float = 1e-4,
        batch_size: int = 32,
        num_epochs: int = 10,
        weight_decay: float = 0.01,
        warmup_steps: int = 0,
        max_grad_norm: float = 1.0,
        gradient_accumulation_steps: int = 1,
        seed: int = 42,
        device: str = "cpu",
        mixed_precision: str = "no",
        logging_steps: int = 100,
        save_steps: int = 500,
        eval_steps: int = 500,
        save_total_limit: int = 3,
        load_best_model_at_end: bool = True,
        metric_for_best_model: str = "loss",
        greater_is_better: bool = False,
        resume_from_checkpoint: str = None,
        output_dir: str = "./output",
        overwrite_output_dir: bool = False,
        remove_unused_columns: bool = True,
        dataloader_pin_memory: bool = True,
        dataloader_num_workers: int = 0,
        dataloader_drop_last: bool = False,
        label_smoothing_factor: float = 0.0,
        optim: str = "adamw_torch",
        adam_beta1: float = 0.9,
        adam_beta2: float = 0.999,
        adam_epsilon: float = 1e-8,
        lr_scheduler_type: str = "linear",
        num_warmup_steps: int = 0,
        num_training_steps: int = None,
    ):
        """Initialize training configuration.
        
        Args:
            learning_rate: Learning rate for optimizer
            batch_size: Batch size for training
            num_epochs: Number of training epochs
            weight_decay: Weight decay for optimizer
            warmup_steps: Number of warmup steps
            max_grad_norm: Maximum gradient norm for clipping
            gradient_accumulation_steps: Number of steps to accumulate gradients
            seed: Random seed
            device: Device to use (cpu or cuda)
            mixed_precision: Mixed precision training mode
            logging_steps: Steps between logging
            save_steps: Steps between saving checkpoints
            eval_steps: Steps between evaluations
            save_total_limit: Maximum number of checkpoints to keep
            load_best_model_at_end: Whether to load best model at end
            metric_for_best_model: Metric to use for best model selection
            greater_is_better: Whether higher metric values are better
            resume_from_checkpoint: Path to checkpoint to resume from
            output_dir: Output directory for checkpoints
            overwrite_output_dir: Whether to overwrite output directory
            remove_unused_columns: Whether to remove unused columns
            dataloader_pin_memory: Whether to pin memory in dataloader
            dataloader_num_workers: Number of workers for dataloader
            dataloader_drop_last: Whether to drop last incomplete batch
            label_smoothing_factor: Label smoothing factor
            optim: Optimizer type
            adam_beta1: Adam beta1 parameter
            adam_beta2: Adam beta2 parameter
            adam_epsilon: Adam epsilon parameter
            lr_scheduler_type: Learning rate scheduler type
            num_warmup_steps: Number of warmup steps
            num_training_steps: Total number of training steps
        """
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.weight_decay = weight_decay
        self.warmup_steps = warmup_steps
        self.max_grad_norm = max_grad_norm
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.seed = seed
        self.device = device
        self.mixed_precision = mixed_precision
        self.logging_steps = logging_steps
        self.save_steps = save_steps
        self.eval_steps = eval_steps
        self.save_total_limit = save_total_limit
        self.load_best_model_at_end = load_best_model_at_end
        self.metric_for_best_model = metric_for_best_model
        self.greater_is_better = greater_is_better
        self.resume_from_checkpoint = resume_from_checkpoint
        self.output_dir = output_dir
        self.overwrite_output_dir = overwrite_output_dir
        self.remove_unused_columns = remove_unused_columns
        self.dataloader_pin_memory = dataloader_pin_memory
        self.dataloader_num_workers = dataloader_num_workers
        self.dataloader_drop_last = dataloader_drop_last
        self.label_smoothing_factor = label_smoothing_factor
        self.optim = optim
        self.adam_beta1 = adam_beta1
        self.adam_beta2 = adam_beta2
        self.adam_epsilon = adam_epsilon
        self.lr_scheduler_type = lr_scheduler_type
        self.num_warmup_steps = num_warmup_steps
        self.num_training_steps = num_training_steps
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return self.__dict__.copy()
    
    def to_json_string(self) -> str:
        """Convert configuration to JSON string."""
        import json
        return json.dumps(self.to_dict(), indent=2)
    
    def save_pretrained(self, save_directory: str) -> None:
        """Save configuration to a directory."""
        import os
        import json
        
        os.makedirs(save_directory, exist_ok=True)
        config_file = os.path.join(save_directory, "training_config.json")
        
        with open(config_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def from_pretrained(cls, save_directory: str) -> "TrainingConfig":
        """Load configuration from a directory."""
        import os
        import json
        
        config_file = os.path.join(save_directory, "training_config.json")
        
        with open(config_file, "r") as f:
            config_dict = json.load(f)
        
        return cls(**config_dict)
    
    def __repr__(self) -> str:
        """String representation of configuration."""
        return f"TrainingConfig({self.to_json_string()})"