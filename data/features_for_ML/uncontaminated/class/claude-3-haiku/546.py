class RetrievalConfig:
    """Configuration for BM25 retrieval parameters"""

    def __init__(self, k1: float = 1.2, b: float = 0.75, epsilon: float = 1e-8):
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon

    def __str__(self):
        return f"RetrievalConfig(k1={self.k1}, b={self.b}, epsilon={self.epsilon})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, RetrievalConfig):
            return False
        return (
            self.k1 == other.k1
            and self.b == other.b
            and self.epsilon == other.epsilon
        )

    def __hash__(self):
        return hash((self.k1, self.b, self.epsilon))