class GCGConfig:  # pylint: disable=too-many-instance-attributes
    """
    Configuration dataclass for the GCG attack parameters
    """
    
    def __init__(
        self,
        num_steps: int = 500,
        batch_size: int = 32,
        num_tokens: int = 20,
        learning_rate: float = 0.1,
        topk: int = 256,
        seed: int = 42,
        use_prefix_cache: bool = True,
        use_cache: bool = True,
        model_name: str = "gpt2",
        device: str = "cuda",
        dtype: str = "float32",
        loss_type: str = "ce",
        target_weight: float = 1.0,
        control_weight: float = 0.0,
        regularization: float = 0.0,
        early_stopping: bool = False,
        early_stopping_patience: int = 10,
        early_stopping_threshold: float = 0.01,
        log_interval: int = 10,
        save_interval: int = 100,
        save_dir: str = "./results",
        verbose: bool = True,
    ):
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.num_tokens = num_tokens
        self.learning_rate = learning_rate
        self.topk = topk
        self.seed = seed
        self.use_prefix_cache = use_prefix_cache
        self.use_cache = use_cache
        self.model_name = model_name
        self.device = device
        self.dtype = dtype
        self.loss_type = loss_type
        self.target_weight = target_weight
        self.control_weight = control_weight
        self.regularization = regularization
        self.early_stopping = early_stopping
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_threshold = early_stopping_threshold
        self.log_interval = log_interval
        self.save_interval = save_interval
        self.save_dir = save_dir
        self.verbose = verbose
    
    def __repr__(self) -> str:
        attrs = ", ".join(
            f"{k}={v!r}" for k, v in self.__dict__.items()
        )
        return f"GCGConfig({attrs})"
    
    def to_dict(self) -> dict:
        return self.__dict__.copy()
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "GCGConfig":
        return cls(**config_dict)