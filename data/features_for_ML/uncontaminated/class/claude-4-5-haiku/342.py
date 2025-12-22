class CheckpointConfig:
    """
    fsdp2 checkpoint config

    Attributes:
        enable_checkpoint (bool): Whether to enable checkpointing
        folder (str): The folder to store the checkpoints
        interval_type (str): Checkpointing interval unit of measurement ['step', 'seconds']
        interval (int): Checkpointing interval, in steps or seconds depending on --checkpoint.interval_type
        model_weights_only (bool): When model_weights_only=True, only model weights will be saved at the end of training.
                With this, checkpoints can be loaded using `torch.load(..., weights_only=True)` after conversion.
                When model_weights_only=False, the full checkpoint will be saved.
                A full checkpoint includes model, optimizer and train_state, which can be used to resume training.
                The default value is false.
        export_dtype (str): Converts to the specified precision when training completes and model_weights_only=true.
                Currently supports float32, float16, and bfloat16.
                The default value is float32.
        async_mode (str): Which async checkpoint mode to use. Currently there are 3 different modes.
                1. "disabled": synchronized checkpointing will be used.
                2. "async": torch.distributed.checkpoint.async_save will be used.
                3. "async_with_pinned_mem": this option utilizes a dedicated pinned memory
                   space and creates a separate process for faster GPU->CPU transfer
                   performance and eliminating GIL contention. The cost is increased CPU
                   memory usage. If insufficient CPU memory is available, performance may
                   degrade due to memory paging. For most users, "async" should suffice as
                   the performance overhead is typically small (on the order of tens of
                   seconds) compared to checkpointing frequency. This mode can be employed
                   to pursue near-zero checkpointing times (e.g., < 1 second) given
                   appropriate hardware support such as ample CPU memory and fast PCIe.

                "disabled" is the default mode.
        create_seed_checkpoint (bool): Initializes the full model without applying parallelisms, and then saves it as a seed checkpoint.
                Note: requires user to call train.py without specifying any parallelisms, e.g. NGPU=1.
                Could be implemented as a separate script, but this way shares more code.
    """

    def __init__(
        self,
        enable_checkpoint: bool = False,
        folder: str = "",
        interval_type: str = "step",
        interval: int = 1,
        model_weights_only: bool = False,
        export_dtype: str = "float32",
        async_mode: str = "disabled",
        create_seed_checkpoint: bool = False,
    ):
        self.enable_checkpoint = enable_checkpoint
        self.folder = folder
        self.interval_type = interval_type
        self.interval = interval
        self.model_weights_only = model_weights_only
        self.export_dtype = export_dtype
        self.async_mode = async_mode
        self.create_seed_checkpoint = create_seed_checkpoint