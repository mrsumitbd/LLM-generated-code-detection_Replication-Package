class RetrievalConfig:
    """Configuration for BM25 retrieval parameters"""
    
    def __init__(
        self,
        k1: float = 1.5,
        b: float = 0.75,
        epsilon: float = 0.25,
    ):
        """
        Initialize RetrievalConfig with BM25 parameters.
        
        Args:
            k1: Controls term frequency saturation point (default: 1.5)
            b: Controls how much effect document length has on relevance (default: 0.75)
            epsilon: Controls IDF lower bound (default: 0.25)
        """
        self.k1 = k1
        self.b = b
        self.epsilon = epsilon
    
    def __repr__(self) -> str:
        return f"RetrievalConfig(k1={self.k1}, b={self.b}, epsilon={self.epsilon})"
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            "k1": self.k1,
            "b": self.b,
            "epsilon": self.epsilon,
        }
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "RetrievalConfig":
        """Create RetrievalConfig from dictionary"""
        return cls(
            k1=config_dict.get("k1", 1.5),
            b=config_dict.get("b", 0.75),
            epsilon=config_dict.get("epsilon", 0.25),
        )