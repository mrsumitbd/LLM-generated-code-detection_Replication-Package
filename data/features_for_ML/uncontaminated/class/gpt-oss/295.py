import abc
from typing import List, Dict, Any


class EmbeddingProvider(abc.ABC):
    """Base class for embedding providers.

    Subclasses must implement the :meth:`embed` method which returns a
    numeric embedding for a single string.  The base class provides a
    simple caching mechanism and a convenience method for embedding
    batches of strings.
    """

    def __init__(self) -> None:
        """Create a new provider with an empty cache."""
        self._cache: Dict[str, List[float]] = {}

    @abc.abstractmethod
    def embed(self, text: str) -> List[float]:
        """Return an embedding vector for *text*.

        Parameters
        ----------
        text : str
            The input string to embed.

        Returns
        -------
        List[float]
            The embedding vector.
        """
        raise NotImplementedError

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Return embeddings for a batch of strings.

        Parameters
        ----------
        texts : List[str]
            The list of input strings.

        Returns
        -------
        List[List[float]]
            A list of embedding vectors corresponding to *texts*.
        """
        embeddings: List[List[float]] = []
        for text in texts:
            if text in self._cache:
                embeddings.append(self._cache[text])
            else:
                emb = self.embed(text)
                self._cache[text] = emb
                embeddings.append(emb)
        return embeddings

    def clear_cache(self) -> None:
        """Clear the internal embedding cache."""
        self._cache.clear()