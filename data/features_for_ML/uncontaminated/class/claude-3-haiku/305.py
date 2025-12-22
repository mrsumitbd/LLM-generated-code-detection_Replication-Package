class TrainingConfig:
    """Training configuration."""

    def __init__(self, learning_rate: float, batch_size: int, num_epochs: int, model_save_path: str):
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.model_save_path = model_save_path

    def __str__(self):
        return f"Learning Rate: {self.learning_rate}, Batch Size: {self.batch_size}, Epochs: {self.num_epochs}, Model Save Path: {self.model_save_path}"

    def __repr__(self):
        return f"TrainingConfig(learning_rate={self.learning_rate}, batch_size={self.batch_size}, num_epochs={self.num_epochs}, model_save_path='{self.model_save_path}')"