class ArgsConfig:
    """Configuration for GR00T model fine-tuning."""
    
    def __init__(self, model_name='GR00T', num_epochs=10, learning_rate=0.001, batch_size=32):
        self.model_name = model_name
        self.num_epochs = num_epochs
        self.learning_rate = learning_rate
        self.batch_size = batch_size

    def display_config(self):
        print(f"Model Name: {self.model_name}")
        print(f"Number of Epochs: {self.num_epochs}")
        print(f"Learning Rate: {self.learning_rate}")
        print(f"Batch Size: {self.batch_size}")

# Example usage:
# config = ArgsConfig()
# config.display_config()