class RetrievalConfig:
    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b

    def set_k1(self, k1):
        self.k1 = k1

    def set_b(self, b):
        self.b = b

    def get_k1(self):
        return self.k1

    def get_b(self):
        return self.b

# Example usage:
# config = RetrievalConfig()
# print(config.get_k1())  # Output: 1.5
# print(config.get_b())   # Output: 0.75
# config.set_k1(2.0)
# config.set_b(0.8)
# print(config.get_k1())  # Output: 2.0
# print(config.get_b())   # Output: 0.8