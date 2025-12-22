class EmbeddingProvider:
    """Base class for embedding providers."""
    
    def __init__(self, embedding_dim):
        self.embedding_dim = embedding_dim
        
    def get_embedding(self, word):
        raise NotImplementedError("Subclasses must implement this method")