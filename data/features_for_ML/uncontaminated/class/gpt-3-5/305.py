class TrainingConfig:
    def __init__(self, batch_size, learning_rate, num_epochs):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.num_epochs = num_epochs

    def display_config(self):
        print(f"Batch Size: {self.batch_size}")
        print(f"Learning Rate: {self.learning_rate}")
        print(f"Number of Epochs: {self.num_epochs}")

# Example usage:
# config = TrainingConfig(batch_size=32, learning_rate=0.001, num_epochs=10)
# config.display_config()