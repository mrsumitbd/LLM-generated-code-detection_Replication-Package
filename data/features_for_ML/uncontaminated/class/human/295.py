from typing import Dict, List, Optional, Any, Set, Tuple, Generator

class EmbeddingProvider:
    """Base class for embedding providers."""
    
    async def embed_documents(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError
    
    async def close(self):
        """Cleanup resources."""
        pass