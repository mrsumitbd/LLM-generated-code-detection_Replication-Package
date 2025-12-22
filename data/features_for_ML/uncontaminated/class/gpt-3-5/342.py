class CheckpointConfig:
    def __init__(self, enable_checkpoint, folder, interval_type, interval, model_weights_only=False, export_dtype='float32', async_mode='disabled', create_seed_checkpoint=False):
        self.enable_checkpoint = enable_checkpoint
        self.folder = folder
        self.interval_type = interval_type
        self.interval = interval
        self.model_weights_only = model_weights_only
        self.export_dtype = export_dtype
        self.async_mode = async_mode
        self.create_seed_checkpoint = create_seed_checkpoint

    def __str__(self):
        return f"CheckpointConfig(enable_checkpoint={self.enable_checkpoint}, folder='{self.folder}', interval_type='{self.interval_type}', interval={self.interval}, model_weights_only={self.model_weights_only}, export_dtype='{self.export_dtype}', async_mode='{self.async_mode}', create_seed_checkpoint={self.create_seed_checkpoint})"

# Example usage:
config = CheckpointConfig(enable_checkpoint=True, folder='/path/to/checkpoints', interval_type='step', interval=1000)
print(config)