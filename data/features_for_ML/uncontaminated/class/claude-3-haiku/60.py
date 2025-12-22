class ArgsConfig:
    """Configuration for GR00T model fine-tuning."""

    def __init__(
        self,
        model_name: str = "gr00t-base",
        data_dir: str = "data/",
        output_dir: str = "outputs/",
        max_seq_length: int = 128,
        train_batch_size: int = 32,
        eval_batch_size: int = 32,
        learning_rate: float = 2e-5,
        num_train_epochs: int = 3,
        warmup_steps: int = 0,
        weight_decay: float = 0.0,
        adam_epsilon: float = 1e-8,
        max_grad_norm: float = 1.0,
        seed: int = 42,
        do_train: bool = True,
        do_eval: bool = True,
        do_predict: bool = True,
        overwrite_output_dir: bool = False,
        use_fp16: bool = False,
        fp16_opt_level: str = "O1",
    ):
        self.model_name = model_name
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.max_seq_length = max_seq_length
        self.train_batch_size = train_batch_size
        self.eval_batch_size = eval_batch_size
        self.learning_rate = learning_rate
        self.num_train_epochs = num_train_epochs
        self.warmup_steps = warmup_steps
        self.weight_decay = weight_decay
        self.adam_epsilon = adam_epsilon
        self.max_grad_norm = max_grad_norm
        self.seed = seed
        self.do_train = do_train
        self.do_eval = do_eval
        self.do_predict = do_predict
        self.overwrite_output_dir = overwrite_output_dir
        self.use_fp16 = use_fp16
        self.fp16_opt_level = fp16_opt_level