class OptimizationConfig:
    def __init__(self, algorithm='gradient_descent', learning_rate=0.01, max_iterations=1000):
        self.algorithm = algorithm
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate

    def set_max_iterations(self, max_iterations):
        self.max_iterations = max_iterations

    def get_algorithm(self):
        return self.algorithm

    def get_learning_rate(self):
        return self.learning_rate

    def get_max_iterations(self):
        return self.max_iterations

# Example usage:
# config = OptimizationConfig()
# print(config.get_algorithm())  # Output: gradient_descent
# config.set_algorithm('adam')
# print(config.get_algorithm())  # Output: adam